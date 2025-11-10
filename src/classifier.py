import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os


class WasteClassifier:
    CLASSES = ['Orgânico', 'Reciclável', 'Rejeito', 'Perigoso']
    DANGER_THRESHOLD = 0.15
    CONFIDENCE_THRESHOLD = 0.40
    
    def __init__(self, model_path='models/waste_classifier.pkl'):
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
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
        if self.model is None:
            print("Nenhum modelo para salvar!")
            return
        
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        joblib.dump(self.model, self.model_path)
        print(f"Modelo salvo em {self.model_path}")
    
    def predict(self, features):
        if self.model is None:
            return self._fallback_prediction(features)
        
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
        
        probabilities = self.model.predict_proba(features)[0]
        predicted_class, confidence, explanation = self._apply_safety_rule(probabilities)
        prob_dict = {class_name: float(prob) 
                     for class_name, prob in zip(self.CLASSES, probabilities)}
        disposal_tip = self._get_disposal_tip(predicted_class)
        
        return {
            'classe': predicted_class,
            'confianca': float(confidence),
            'probabilidades': prob_dict,
            'explicacao': explanation,
            'dica_descarte': disposal_tip
        }
    
    def _apply_safety_rule(self, probabilities):
        max_prob = np.max(probabilities)
        max_idx = np.argmax(probabilities)
        predicted_class = self.CLASSES[max_idx]
        danger_idx = self.CLASSES.index('Perigoso')
        danger_prob = probabilities[danger_idx]
        
        if (danger_prob >= self.DANGER_THRESHOLD and 
            max_prob < 0.60 and 
            predicted_class != 'Perigoso'):
            
            explanation = (
                f"⚠️ Classificação ajustada para 'Perigoso' por segurança "
                f"(probabilidade: {danger_prob:.1%}). "
                f"Em caso de dúvida, trate como resíduo perigoso."
            )
            return 'Perigoso', danger_prob, explanation
        
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
        text_scores = features[-4:]
        
        if text_scores.sum() == 0:
            return {
                'classe': 'Desconhecido',
                'confianca': 0.0,
                'probabilidades': {c: 0.25 for c in self.CLASSES},
                'explicacao': '⚠️ Modelo não disponível e nenhuma palavra-chave identificada.',
                'dica_descarte': 'Consulte serviço de coleta local para orientação.'
            }
        
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

