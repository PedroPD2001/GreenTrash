"""
Script para treinar o modelo usando imagens reais da pasta assets/images.
Prioriza features visuais sobre textuais para maior acurácia.
"""

import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from src.feature_extraction import FeatureExtractor
from src.classifier import WasteClassifier


def load_images_from_folder(folder_path, class_name):
    """
    Carrega todas as imagens de uma pasta.
    
    Args:
        folder_path: Caminho da pasta
        class_name: Nome da classe
        
    Returns:
        Lista de tuplas (imagem, classe)
    """
    images = []
    if not os.path.exists(folder_path):
        print(f"⚠️ Pasta não encontrada: {folder_path}")
        return images
    
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.avif')
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(valid_extensions):
            file_path = os.path.join(folder_path, filename)
            try:
                # Ler imagem
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
    """
    Treina o modelo usando imagens reais da pasta assets/images.
    Prioriza features visuais (peso maior) sobre textuais.
    """
    print("="*60)
    print("TREINAMENTO COM IMAGENS REAIS - GreenTrash")
    print("="*60)
    
    # Mapeamento de pastas para classes
    class_mapping = {
        'organic': 'Orgânico',
        'recyclable': 'Reciclável',
        'reject': 'Rejeito',
        'dangerous': 'Perigoso'
    }
    
    # Garantir que estamos no diretório correto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Caminho base
    base_path = 'assets/images'
    
    # Carregar todas as imagens
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
    
    # Extrair features
    print("\n2. Extraindo features das imagens...")
    print("   Priorizando features visuais sobre textuais...")
    
    extractor = FeatureExtractor()
    X = []
    y = []
    
    for img, class_name in all_images:
        # Extrair features visuais (prioridade)
        visual_features = extractor.extract_visual_features(img)
        
        # Para imagens reais, usar texto vazio (priorizar visual)
        # Ou extrair texto mínimo baseado no nome da pasta
        text_features = extractor.extract_text_features("")  # Vazio para priorizar visual
        
        # Combinar features (visuais têm mais peso implícito por serem mais numerosas)
        # 118 features visuais vs 4 textuais = 96.7% visual, 3.3% textual
        combined_features = np.concatenate([visual_features, text_features])
        
        X.append(combined_features)
        y.append(class_name)
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"\nDados processados:")
    print(f"  - Total de amostras: {len(X)}")
    print(f"  - Features por amostra: {X.shape[1]} (118 visuais + 4 textuais)")
    print(f"  - Distribuição por classe:")
    for class_name in np.unique(y):
        count = np.sum(y == class_name)
        print(f"    • {class_name}: {count} imagens")
    
    # Dividir em treino e teste
    print("\n3. Dividindo dados em treino e teste (80/20)...")
    if len(X) < 10:
        # Se muito poucas imagens, usar tudo para treino
        X_train, X_test = X, X
        y_train, y_test = y, y
        print("  ⚠️ Poucas imagens. Usando todas para treino e teste.")
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    
    print(f"  - Amostras de treino: {len(X_train)}")
    print(f"  - Amostras de teste: {len(X_test)}")
    
    # Treinar modelo
    print("\n4. Treinando Random Forest...")
    print("   Modelo prioriza features visuais (118 features) sobre textuais (4 features)")
    classifier = WasteClassifier()
    classifier.train(X_train, y_train)
    
    # Avaliar no conjunto de teste
    if len(X_test) > 0:
        print("\n5. Avaliando modelo no conjunto de teste...")
        predictions = []
        for features in X_test:
            result = classifier.predict(features)
            predictions.append(result['classe'])
        
        # Relatório de classificação
        print("\n" + "="*60)
        print("RELATÓRIO DE CLASSIFICAÇÃO")
        print("="*60)
        print(classification_report(y_test, predictions, zero_division=0))
        
        # Matriz de confusão
        print("\n" + "="*60)
        print("MATRIZ DE CONFUSÃO")
        print("="*60)
        cm = confusion_matrix(y_test, predictions, labels=classifier.CLASSES)
        
        # Imprimir matriz formatada
        print("\n" + " "*15 + "Predito")
        print(" "*10 + "  ".join(f"{c[:4]:>6}" for c in classifier.CLASSES))
        print("Real")
        for i, class_name in enumerate(classifier.CLASSES):
            print(f"{class_name[:10]:>10} " + "  ".join(f"{cm[i,j]:>6}" for j in range(len(classifier.CLASSES))))
    
    # Salvar modelo
    print("\n6. Salvando modelo...")
    classifier.save_model()
    
    print("\n" + "="*60)
    print("✓ Treinamento concluído com sucesso!")
    print("="*60)
    print(f"\nModelo salvo em: {classifier.model_path}")
    print("\n📊 O modelo foi treinado priorizando features VISUAIS sobre textuais.")
    print("   Isso garante maior acurácia baseada nas imagens reais.")
    print("\nExecute 'streamlit run app.py' para usar a aplicação.")


if __name__ == "__main__":
    train_model_with_real_images()

