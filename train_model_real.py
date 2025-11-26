import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, f1_score
from src.feature_extraction import FeatureExtractor
from src.classifier import WasteClassifier
from src.data_utils import detect_duplicates, filter_low_quality, balance_classes_with_augmentation


def load_images_from_folder(folder_path, class_name):
    images = []
    if not os.path.exists(folder_path):
        print(f"⚠️ Pasta não encontrada: {folder_path}")
        return images
    
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.avif')
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(valid_extensions):
            file_path = os.path.join(folder_path, filename)
            try:
                img = cv2.imread(file_path)
                if img is not None:
                    images.append((img, class_name))
                    print(f"  ✓ {filename}")
                else:
                    print(f"  ✗ Erro ao ler: {filename}")
            except Exception as e:
                print(f"  ✗ Erro em {filename}: {e}")
    
    return images


def train_model_with_real_images():
    print("="*60)
    print("TREINAMENTO COM IMAGENS REAIS - GreenTrash")
    print("="*60)
    
    class_mapping = {
        'organic': 'Orgânico',
        'recyclable': 'Reciclável',
        'reject': 'Rejeito',
        'dangerous': 'Perigoso'
    }
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    base_path = 'assets/images'
    
    print("\n1. Carregando imagens reais...")
    all_images = []
    
    for folder_name, class_name in class_mapping.items():
        folder_path = os.path.join(base_path, folder_name)
        print(f"\n📁 Carregando {class_name} de {folder_name}/...")
        images = load_images_from_folder(folder_path, class_name)
        all_images.extend(images)
        print(f"  Total: {len(images)} imagens")
    
    if len(all_images) == 0:
        print("\n❌ Nenhuma imagem encontrada! Verifique a pasta assets/images/")
        return
    
    print(f"\n✅ Total de imagens carregadas: {len(all_images)}")
    
    print("\n2. Limpando duplicatas e imagens de baixa qualidade...")
    unique_images, duplicates = detect_duplicates(all_images)
    print(f"  - Duplicatas removidas: {len(duplicates)}")
    
    filtered_images, removed = filter_low_quality(unique_images, min_quality=0.3)
    print(f"  - Imagens de baixa qualidade removidas: {len(removed)}")
    print(f"  - Imagens válidas: {len(filtered_images)}")
    
    print("\n3. Balanceando classes com data augmentation...")
    class_counts_before = {}
    for _, label in filtered_images:
        class_counts_before[label] = class_counts_before.get(label, 0) + 1
    
    print("  Distribuição antes do balanceamento:")
    for cls, count in class_counts_before.items():
        print(f"    • {cls}: {count} imagens")
    
    balanced_images = balance_classes_with_augmentation(filtered_images)
    class_counts_after = {}
    for _, label in balanced_images:
        class_counts_after[label] = class_counts_after.get(label, 0) + 1
    
    print("\n  Distribuição após balanceamento:")
    for cls, count in class_counts_after.items():
        print(f"    • {cls}: {count} imagens")
    
    print("\n4. Extraindo features das imagens...")
    extractor = FeatureExtractor()
    X = []
    y = []
    
    for img, class_name in balanced_images:
        visual_features = extractor.extract_visual_features(img)
        text_features = extractor.extract_text_features("")
        combined_features = np.concatenate([visual_features, text_features])
        
        X.append(combined_features)
        y.append(class_name)
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"\nDados processados:")
    print(f"  - Total de amostras: {len(X)}")
    print(f"  - Features por amostra: {X.shape[1]} (118 visuais + 4 textuais)")
    
    print("\n5. Dividindo dados em treino e teste (80/20)...")
    if len(X) < 10:
        X_train, X_test = X, X
        y_train, y_test = y, y
        print("  ⚠️ Poucas imagens. Usando todas para treino e teste.")
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    
    print(f"  - Amostras de treino: {len(X_train)}")
    print(f"  - Amostras de teste: {len(X_test)}")
    
    print("\n6. Treinando Random Forest otimizado...")
    classifier = WasteClassifier()
    classifier.train(X_train, y_train, calibrate=True)
    
    if len(X_test) > 0:
        print("\n7. Avaliando modelo no conjunto de teste...")
        predictions = []
        for features in X_test:
            result = classifier.predict(features, text="")
            predictions.append(result['classe'])
        
        print("\n" + "="*60)
        print("RELATÓRIO DE CLASSIFICAÇÃO")
        print("="*60)
        print(classification_report(y_test, predictions, zero_division=0))
        
        precision = precision_score(y_test, predictions, labels=classifier.CLASSES, average=None, zero_division=0)
        recall = recall_score(y_test, predictions, labels=classifier.CLASSES, average=None, zero_division=0)
        f1 = f1_score(y_test, predictions, labels=classifier.CLASSES, average=None, zero_division=0)
        
        print("\n" + "="*60)
        print("MÉTRICAS POR CLASSE")
        print("="*60)
        print(f"{'Classe':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
        print("-" * 60)
        for i, class_name in enumerate(classifier.CLASSES):
            print(f"{class_name:<15} {precision[i]:<12.3f} {recall[i]:<12.3f} {f1[i]:<12.3f}")
        
        print("\n" + "="*60)
        print("MATRIZ DE CONFUSÃO")
        print("="*60)
        cm = confusion_matrix(y_test, predictions, labels=classifier.CLASSES)
        
        print("\n" + " "*15 + "Predito")
        print(" "*10 + "  ".join(f"{c[:4]:>6}" for c in classifier.CLASSES))
        print("Real")
        for i, class_name in enumerate(classifier.CLASSES):
            print(f"{class_name[:10]:>10} " + "  ".join(f"{cm[i,j]:>6}" for j in range(len(classifier.CLASSES))))
        
        false_dangerous = 0
        if 'Perigoso' in classifier.CLASSES:
            danger_idx = classifier.CLASSES.index('Perigoso')
            for i, true_class in enumerate(y_test):
                if true_class != 'Perigoso' and predictions[i] == 'Perigoso':
                    false_dangerous += 1
        
        print(f"\n⚠️ Falsos 'Perigoso': {false_dangerous}")
    
    print("\n8. Salvando modelo...")
    classifier.save_model()
    
    print("\n" + "="*60)
    print("✓ Treinamento concluído com sucesso!")
    print("="*60)
    print(f"\nModelo salvo em: {classifier.model_path}")
    print("\nExecute 'streamlit run app.py' para usar a aplicação.")


if __name__ == "__main__":
    train_model_with_real_images()

