"""
Script de validação do sistema GreenTrash.
Verifica se todos os componentes estão funcionando corretamente.
"""

import os
import sys
import cv2
import numpy as np

print("="*60)
print("VALIDAÇÃO DO SISTEMA GreenTrash")
print("="*60)

# 1. Verificar diretório
print("\n1. Verificando diretório...")
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"   ✓ Diretório: {script_dir}")

# 2. Verificar imports
print("\n2. Verificando imports...")
try:
    from src.feature_extraction import FeatureExtractor
    from src.classifier import WasteClassifier
    print("   ✓ Imports OK")
except Exception as e:
    print(f"   ✗ Erro nos imports: {e}")
    sys.exit(1)

# 3. Verificar pastas de imagens
print("\n3. Verificando pastas de imagens...")
base_path = 'assets/images'
class_folders = ['organic', 'recyclable', 'reject', 'dangerous']
total_images = 0

for folder in class_folders:
    folder_path = os.path.join(base_path, folder)
    if os.path.exists(folder_path):
        images = [f for f in os.listdir(folder_path) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.avif'))]
        count = len(images)
        total_images += count
        print(f"   ✓ {folder}: {count} imagens")
    else:
        print(f"   ✗ Pasta não encontrada: {folder_path}")

if total_images == 0:
    print("   ⚠️ Nenhuma imagem encontrada!")
else:
    print(f"   ✓ Total: {total_images} imagens")

# 4. Testar extração de features
print("\n4. Testando extração de features...")
try:
    extractor = FeatureExtractor()
    
    # Testar features visuais (imagem sintética)
    test_image = np.zeros((256, 256, 3), dtype=np.uint8)
    test_image[:, :] = [100, 150, 200]  # Cor azul
    visual_features = extractor.extract_visual_features(test_image)
    print(f"   ✓ Features visuais: {len(visual_features)} features")
    
    # Testar features textuais
    text_features = extractor.extract_text_features("garrafa de plástico")
    print(f"   ✓ Features textuais: {len(text_features)} features")
    
    # Testar combinação
    combined = np.concatenate([visual_features, text_features])
    print(f"   ✓ Features combinadas: {len(combined)} features")
    
except Exception as e:
    print(f"   ✗ Erro na extração: {e}")
    sys.exit(1)

# 5. Verificar modelo
print("\n5. Verificando modelo...")
try:
    classifier = WasteClassifier()
    if classifier.model is not None:
        print("   ✓ Modelo carregado")
        
        # Testar predição
        test_features = np.random.rand(122)  # Features aleatórias para teste
        result = classifier.predict(test_features)
        print(f"   ✓ Predição funcionando: {result['classe']}")
    else:
        print("   ⚠️ Modelo não encontrado (execute train_model_real.py)")
except Exception as e:
    print(f"   ✗ Erro no modelo: {e}")

# 6. Verificar arquivos principais
print("\n6. Verificando arquivos principais...")
required_files = [
    'app.py',
    'train_model_real.py',
    'src/feature_extraction.py',
    'src/classifier.py',
    'requirements.txt'
]

for file in required_files:
    if os.path.exists(file):
        print(f"   ✓ {file}")
    else:
        print(f"   ✗ {file} não encontrado")

print("\n" + "="*60)
print("VALIDAÇÃO CONCLUÍDA")
print("="*60)

if total_images > 0:
    print("\n✅ Sistema pronto para uso!")
    print("\nPara treinar o modelo:")
    print("  py train_model_real.py")
    print("\nPara executar a aplicação:")
    print("  streamlit run app.py")
else:
    print("\n⚠️ Adicione imagens em assets/images/ antes de treinar")

