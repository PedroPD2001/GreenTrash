import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
import joblib
import os


class WasteClassifier:
    CLASSES = ['Orgânico', 'Reciclável', 'Rejeito', 'Perigoso']
    DANGER_THRESHOLD = 0.25
    CONFIDENCE_THRESHOLD = 0.50
    TOP2_TIE_THRESHOLD = 0.05
    
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
    
    def train(self, X, y, calibrate=True):
        base_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=25,
            min_samples_split=3,
            min_samples_leaf=1,
            max_features='sqrt',
            random_state=42,
            class_weight='balanced',
            n_jobs=-1
        )
        
        base_model.fit(X, y)
        
        if calibrate:
            self.model = CalibratedClassifierCV(base_model, method='isotonic', cv=3)
            self.model.fit(X, y)
        else:
            self.model = base_model
        
        print("Modelo treinado com sucesso!")
    
    def save_model(self):
        if self.model is None:
            print("Nenhum modelo para salvar!")
            return
        
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        joblib.dump(self.model, self.model_path)
        print(f"Modelo salvo em {self.model_path}")
    
    def predict(self, features, text=""):
        if self.model is None:
            return self._fallback_prediction(features, text)
        
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
        
        probabilities = self.model.predict_proba(features)[0]
        predicted_class, confidence, explanation, needs_feedback = self._apply_decision_rules(probabilities, text)
        prob_dict = {class_name: float(prob) 
                     for class_name, prob in zip(self.CLASSES, probabilities)}
        disposal_tip = self._get_disposal_tip(predicted_class)
        
        return {
            'classe': predicted_class,
            'confianca': float(confidence),
            'probabilidades': prob_dict,
            'explicacao': explanation,
            'dica_descarte': disposal_tip,
            'needs_feedback': needs_feedback
        }
    
    def _apply_decision_rules(self, probabilities, text=""):
        sorted_indices = np.argsort(probabilities)[::-1]
        top2_probs = probabilities[sorted_indices[:2]]
        top2_classes = [self.CLASSES[i] for i in sorted_indices[:2]]
        
        max_prob = probabilities[sorted_indices[0]]
        predicted_class = top2_classes[0]
        danger_idx = self.CLASSES.index('Perigoso')
        danger_prob = probabilities[danger_idx]
        
        needs_feedback = False
        
        if max_prob < self.CONFIDENCE_THRESHOLD:
            needs_feedback = True
            explanation = (
                f"⚠️ Baixa confiança na classificação ({max_prob:.1%}). "
                f"Por favor, confirme se a classificação está correta."
            )
            return predicted_class, max_prob, explanation, needs_feedback
        
        tie_detected = (top2_probs[0] - top2_probs[1]) < self.TOP2_TIE_THRESHOLD
        
        if tie_detected and text:
            text_lower = text.lower()
            recyclable_keywords = ['cano', 'canos', 'tubo', 'tubos', 'pvc', 'conduíte', 'conduite', 
                                 'encanamento', 'conexões', 'conexoes', 'esgoto', 'tubulação', 'tubulacao']
            dangerous_keywords = ['bateria', 'pilha', 'tinta', 'solvente', 'veneno', 'inseticida',
                                'pesticida', 'remédio', 'medicamento', 'lâmpada', 'fluorescente',
                                'termômetro', 'mercúrio', 'tóxico', 'corrosivo', 'inflamável', 'químico']
            
            recyclable_score = sum(1 for kw in recyclable_keywords if kw in text_lower)
            dangerous_score = sum(1 for kw in dangerous_keywords if kw in text_lower)
            
            if recyclable_score > 0 and 'Reciclável' in top2_classes:
                predicted_class = 'Reciclável'
                max_prob = probabilities[self.CLASSES.index('Reciclável')]
                explanation = (
                    f"✓ Classificação: {predicted_class} (confiança: {max_prob:.1%}). "
                    f"Desempate baseado em texto indicativo."
                )
                return predicted_class, max_prob, explanation, needs_feedback
        
        if predicted_class == 'Perigoso':
            if danger_prob < 0.40:
                needs_feedback = True
                explanation = (
                    f"⚠️ Classificado como 'Perigoso' com confiança moderada ({danger_prob:.1%}). "
                    f"Por favor, confirme se está correto."
                )
            else:
                explanation = (
                    f"✓ Classificação: {predicted_class} (confiança: {danger_prob:.1%}). "
                    f"Evidência forte de resíduo perigoso."
                )
        elif danger_prob >= self.DANGER_THRESHOLD and max_prob < 0.70:
            if danger_prob >= 0.30:
                needs_feedback = True
                explanation = (
                    f"⚠️ Possível resíduo perigoso detectado ({danger_prob:.1%}). "
                    f"Classificado como '{predicted_class}' mas verifique se não é perigoso."
                )
            else:
                explanation = (
                    f"✓ Classificação: {predicted_class} (confiança: {max_prob:.1%})."
                )
        else:
            explanation = (
                f"✓ Classificação: {predicted_class} (confiança: {max_prob:.1%})."
            )
        
        return predicted_class, max_prob, explanation, needs_feedback
    
    def _fallback_prediction(self, features, text=""):
        text_scores = features[-4:]
        
        if text_scores.sum() == 0:
            return {
                'classe': 'Desconhecido',
                'confianca': 0.0,
                'probabilidades': {c: 0.25 for c in self.CLASSES},
                'explicacao': '⚠️ Modelo não disponível e nenhuma palavra-chave identificada.',
                'dica_descarte': 'Consulte serviço de coleta local para orientação.',
                'needs_feedback': True
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
            'dica_descarte': disposal_tip,
            'needs_feedback': confidence < 0.6
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

