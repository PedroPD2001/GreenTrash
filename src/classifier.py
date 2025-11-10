"""
Módulo de classificação de resíduos usando Random Forest.
Implementa regra de segurança priorizando classe "Perigoso" em casos de incerteza.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os


class WasteClassifier:
    """Classificador de resíduos com Random Forest e regras de segurança."""
    
    CLASSES = ['Orgânico', 'Reciclável', 'Rejeito', 'Perigoso']
    
    # Limiar de confiança para priorizar "Perigoso"
    DANGER_THRESHOLD = 0.15  # Se prob(Perigoso) >= 15%, considerar
    CONFIDENCE_THRESHOLD = 0.40  # Confiança mínima geral
    
    def __init__(self, model_path='models/waste_classifier.pkl'):
        """
        Inicializa o classificador.
        
        Args:
            model_path: Caminho para o modelo treinado
        """
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Carrega modelo treinado se existir."""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                print(f"Modelo carregado de {self.model_path}")
            except Exception as e:
                print(f"Erro ao carregar modelo: {e}")
                self.model = None
        else:
            print(f"Modelo não encontrado em {self.model_path}")
            self.model = None
    
    def train(self, X, y):
        """
        Treina o modelo Random Forest.
        
        Args:
            X: Features (numpy array)
            y: Labels (numpy array ou lista)
        """
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X, y)
        print("Modelo treinado com sucesso!")
    
    def save_model(self):
        """Salva o modelo treinado."""
        if self.model is None:
            print("Nenhum modelo para salvar!")
            return
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        joblib.dump(self.model, self.model_path)
        print(f"Modelo salvo em {self.model_path}")
    
    def predict(self, features):
        """
        Prediz a classe do resíduo com regra de segurança.
        
        Args:
            features: numpy array com as features extraídas
            
        Returns:
            dict com: classe, confiança, probabilidades, explicação
        """
        if self.model is None:
            return self._fallback_prediction(features)
        
        # Garantir que features é 2D
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
        
        # Obter probabilidades
        probabilities = self.model.predict_proba(features)[0]
        
        # Aplicar regra de segurança para "Perigoso"
        predicted_class, confidence, explanation = self._apply_safety_rule(probabilities)
        
        # Criar dicionário de probabilidades
        prob_dict = {class_name: float(prob) 
                     for class_name, prob in zip(self.CLASSES, probabilities)}
        
        # Obter dica de descarte
        disposal_tip = self._get_disposal_tip(predicted_class)
        
        return {
            'classe': predicted_class,
            'confianca': float(confidence),
            'probabilidades': prob_dict,
            'explicacao': explanation,
            'dica_descarte': disposal_tip
        }
    
    def _apply_safety_rule(self, probabilities):
        """
        Aplica regra de segurança priorizando "Perigoso" em incerteza.
        
        Args:
            probabilities: array com probabilidades de cada classe
            
        Returns:
            tuple (classe, confiança, explicação)
        """
        max_prob = np.max(probabilities)
        max_idx = np.argmax(probabilities)
        predicted_class = self.CLASSES[max_idx]
        
        # Índice da classe "Perigoso"
        danger_idx = self.CLASSES.index('Perigoso')
        danger_prob = probabilities[danger_idx]
        
        # REGRA DE SEGURANÇA: Priorizar "Perigoso" se probabilidade >= 15%
        # E se a confiança geral for baixa (< 60%)
        if (danger_prob >= self.DANGER_THRESHOLD and 
            max_prob < 0.60 and 
            predicted_class != 'Perigoso'):
            
            explanation = (
                f"⚠️ Classificação ajustada para 'Perigoso' por segurança "
                f"(probabilidade: {danger_prob:.1%}). "
                f"Em caso de dúvida, trate como resíduo perigoso."
            )
            return 'Perigoso', danger_prob, explanation
        
        # Verificar confiança geral
        if max_prob < self.CONFIDENCE_THRESHOLD:
            explanation = (
                f"⚠️ Baixa confiança na classificação ({max_prob:.1%}). "
                f"Recomenda-se verificar manualmente ou fornecer mais informações."
            )
        else:
            explanation = (
                f"✓ Classificação com confiança de {max_prob:.1%}."
            )
        
        return predicted_class, max_prob, explanation
    
    def _fallback_prediction(self, features):
        """
        Predição fallback baseada apenas em features textuais.
        Usado quando modelo não está disponível.
        
        Args:
            features: numpy array com features (últimas 4 são text_scores)
            
        Returns:
            dict com resultado da classificação
        """
        # Últimas 4 features são os text_scores
        text_scores = features[-4:]
        
        if text_scores.sum() == 0:
            # Nenhuma keyword encontrada
            return {
                'classe': 'Desconhecido',
                'confianca': 0.0,
                'probabilidades': {c: 0.25 for c in self.CLASSES},
                'explicacao': '⚠️ Modelo não disponível e nenhuma palavra-chave identificada.',
                'dica_descarte': 'Consulte serviço de coleta local para orientação.'
            }
        
        # Usar text_scores como probabilidades
        max_idx = np.argmax(text_scores)
        predicted_class = self.CLASSES[max_idx]
        confidence = text_scores[max_idx]
        
        prob_dict = {class_name: float(score) 
                     for class_name, score in zip(self.CLASSES, text_scores)}
        
        explanation = (
            f"⚠️ Classificação baseada apenas em texto (modelo não disponível). "
            f"Confiança: {confidence:.1%}"
        )
        
        disposal_tip = self._get_disposal_tip(predicted_class)
        
        return {
            'classe': predicted_class,
            'confianca': float(confidence),
            'probabilidades': prob_dict,
            'explicacao': explanation,
            'dica_descarte': disposal_tip
        }
    
    def _get_disposal_tip(self, waste_class):
        """
        Retorna dica de descarte apropriada para cada classe.
        
        Args:
            waste_class: Nome da classe
            
        Returns:
            String com dica de descarte
        """
        tips = {
            'Orgânico': (
                "🌱 Descarte em lixeira marrom ou faça compostagem. "
                "Resíduos orgânicos podem virar adubo!"
            ),
            'Reciclável': (
                "♻️ Descarte em lixeira azul ou ponto de coleta seletiva. "
                "Limpe e separe para facilitar a reciclagem."
            ),
            'Rejeito': (
                "🗑️ Descarte em lixeira cinza ou preta (lixo comum). "
                "Este material não é reciclável nem compostável."
            ),
            'Perigoso': (
                "⚠️ NÃO descarte em lixo comum! "
                "Leve a ponto de coleta especial ou entrega voluntária. "
                "Resíduos perigosos contaminam o meio ambiente."
            ),
            'Desconhecido': (
                "❓ Classificação incerta. Consulte serviço de coleta local "
                "ou busque mais informações sobre o descarte adequado."
            )
        }
        
        return tips.get(waste_class, tips['Desconhecido'])

