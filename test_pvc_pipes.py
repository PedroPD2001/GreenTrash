import numpy as np
from src.feature_extraction import FeatureExtractor
from src.classifier import WasteClassifier
from sklearn.metrics import precision_score, recall_score, f1_score

def test_pvc_pipes():
    print("="*60)
    print("TESTE ESPECÍFICO: CANOS/PVC")
    print("="*60)
    
    extractor = FeatureExtractor()
    classifier = WasteClassifier()
    
    if classifier.model is None:
        print("❌ Modelo não encontrado. Execute train_model_real.py primeiro.")
        return
    
    test_cases = [
        ("cano de pvc", "Reciclável"),
        ("tubo de plástico", "Reciclável"),
        ("canos de esgoto", "Reciclável"),
        ("conduíte pvc", "Reciclável"),
        ("tubulação de encanamento", "Reciclável"),
        ("conexões de pvc", "Reciclável"),
        ("cano de metal", "Reciclável"),
        ("tubo de aço", "Reciclável"),
    ]
    
    print("\nCasos de teste:")
    predictions = []
    true_labels = []
    
    for text, expected in test_cases:
        text_features = extractor.extract_text_features(text)
        visual_features = np.zeros(118)
        features = np.concatenate([visual_features, text_features])
        
        result = classifier.predict(features, text=text)
        predicted = result['classe']
        confidence = result['confianca']
        
        predictions.append(predicted)
        true_labels.append(expected)
        
        status = "✓" if predicted == expected else "✗"
        print(f"  {status} '{text}' → {predicted} (esperado: {expected}, confiança: {confidence:.1%})")
    
    print("\n" + "="*60)
    print("MÉTRICAS DO TESTE")
    print("="*60)
    
    precision = precision_score(true_labels, predictions, labels=['Reciclável'], average='micro', zero_division=0)
    recall = recall_score(true_labels, predictions, labels=['Reciclável'], average='micro', zero_division=0)
    f1 = f1_score(true_labels, predictions, labels=['Reciclável'], average='micro', zero_division=0)
    
    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1-Score: {f1:.3f}")
    
    correct = sum(1 for p, t in zip(predictions, true_labels) if p == t)
    print(f"\nAcurácia: {correct}/{len(test_cases)} ({correct/len(test_cases):.1%})")
    
    false_dangerous = sum(1 for p, t in zip(predictions, true_labels) if p == 'Perigoso' and t == 'Reciclável')
    print(f"Falsos 'Perigoso': {false_dangerous}")

if __name__ == "__main__":
    test_pvc_pipes()

