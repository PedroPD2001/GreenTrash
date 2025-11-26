import os
import cv2
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score
from src.feature_extraction import FeatureExtractor
from src.classifier import WasteClassifier
from src.feedback_collector import FeedbackCollector
from src.data_utils import load_images_from_folder, balance_classes_with_augmentation, detect_duplicates, filter_low_quality

def retrain_with_feedback():
    print("="*60)
    print("RE-TREINAMENTO COM FEEDBACK - GreenTrash")
    print("="*60)
    
    collector = FeedbackCollector()
    feedbacks = collector.load_feedback()
    
    if len(feedbacks) == 0:
        print("\n⚠️ Nenhum feedback coletado ainda.")
        print("Execute a aplicação e forneça feedback quando solicitado.")
        return
    
    print(f"\n📊 Feedbacks coletados: {len(feedbacks)}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("\n1. Carregando dados originais...")
    base_path = 'assets/images'
    
    class_mapping = {
        'organic': 'Orgânico',
        'recyclable': 'Reciclável',
        'reject': 'Rejeito',
        'dangerous': 'Perigoso'
    }
    
    all_images = []
    for folder_name, class_name in class_mapping.items():
        folder_path = os.path.join(base_path, folder_name)
        images = load_images_from_folder(folder_path, class_name)
        all_images.extend(images)
    
    print("\n2. Processando imagens...")
    unique_images, _ = detect_duplicates(all_images)
    filtered_images, _ = filter_low_quality(unique_images)
    balanced_images = balance_classes_with_augmentation(filtered_images)
    
    extractor = FeatureExtractor()
    X_original = []
    y_original = []
    
    for img, class_name in balanced_images:
        visual_features = extractor.extract_visual_features(img)
        text_features = extractor.extract_text_features("")
        combined_features = np.concatenate([visual_features, text_features])
        X_original.append(combined_features)
        y_original.append(class_name)
    
    X_original = np.array(X_original)
    y_original = np.array(y_original)
    
    print("\n3. Adicionando dados de feedback ao conjunto de treino...")
    X_feedback = []
    y_feedback = []
    
    for fb in feedbacks:
        features = np.array(fb['features'])
        correct_label = fb['correct']
        X_feedback.append(features)
        y_feedback.append(correct_label)
    
    X_feedback = np.array(X_feedback)
    y_feedback = np.array(y_feedback)
    
    print(f"  - Amostras de feedback: {len(X_feedback)}")
    
    X_combined = np.vstack([X_original, X_feedback])
    y_combined = np.concatenate([y_original, y_feedback])
    
    print(f"  - Total de amostras: {len(X_combined)}")
    print(f"  - Originais: {len(X_original)}")
    print(f"  - Feedback: {len(X_feedback)}")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_combined, y_combined, test_size=0.2, random_state=42, stratify=y_combined
    )
    
    print("\n4. Re-treinando modelo com feedback...")
    classifier = WasteClassifier()
    classifier.train(X_train, y_train, calibrate=True)
    
    print("\n5. Avaliando modelo re-treinado...")
    predictions = []
    for features in X_test:
        result = classifier.predict(features, text="")
        predictions.append(result['classe'])
    
    print("\n" + "="*60)
    print("RELATÓRIO DE CLASSIFICAÇÃO (APÓS RE-TREINO)")
    print("="*60)
    print(classification_report(y_test, predictions, zero_division=0))
    
    precision = precision_score(y_test, predictions, labels=classifier.CLASSES, average=None, zero_division=0)
    recall = recall_score(y_test, predictions, labels=classifier.CLASSES, average=None, zero_division=0)
    f1 = f1_score(y_test, predictions, labels=classifier.CLASSES, average=None, zero_division=0)
    
    print("\n" + "="*60)
    print("MÉTRICAS POR CLASSE (APÓS RE-TREINO)")
    print("="*60)
    print(f"{'Classe':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
    print("-" * 60)
    for i, class_name in enumerate(classifier.CLASSES):
        print(f"{class_name:<15} {precision[i]:<12.3f} {recall[i]:<12.3f} {f1[i]:<12.3f}")
    
    print("\n6. Salvando modelo re-treinado...")
    classifier.save_model()
    
    print("\n" + "="*60)
    print("✓ Re-treino concluído com sucesso!")
    print("="*60)

if __name__ == "__main__":
    retrain_with_feedback()

