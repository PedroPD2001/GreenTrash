"""
Script para treinar o modelo de classificação de resíduos.
Gera dados sintéticos e treina Random Forest.
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from src.data_generator import DataGenerator
from src.classifier import WasteClassifier


def train_model(samples_per_class=150):
    """
    Treina o modelo de classificação.
    
    Args:
        samples_per_class: Número de amostras sintéticas por classe
    """
    print("="*60)
    print("TREINAMENTO DO MODELO DE CLASSIFICAÇÃO DE RESÍDUOS")
    print("="*60)
    
    # Gerar dados sintéticos
    print("\n1. Gerando dados de treinamento...")
    generator = DataGenerator()
    X, y = generator.generate_training_data(samples_per_class=samples_per_class)
    
    print(f"\nDados gerados:")
    print(f"  - Total de amostras: {len(X)}")
    print(f"  - Features por amostra: {X.shape[1]}")
    print(f"  - Classes: {np.unique(y)}")
    
    # Dividir em treino e teste
    print("\n2. Dividindo dados em treino e teste (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"  - Amostras de treino: {len(X_train)}")
    print(f"  - Amostras de teste: {len(X_test)}")
    
    # Treinar modelo
    print("\n3. Treinando Random Forest...")
    classifier = WasteClassifier()
    classifier.train(X_train, y_train)
    
    # Avaliar no conjunto de teste
    print("\n4. Avaliando modelo no conjunto de teste...")
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
    print("\n5. Salvando modelo...")
    classifier.save_model()
    
    print("\n" + "="*60)
    print("✓ Treinamento concluído com sucesso!")
    print("="*60)
    print(f"\nModelo salvo em: {classifier.model_path}")
    print("\nExecute 'streamlit run app.py' para usar a aplicação.")


if __name__ == "__main__":
    train_model(samples_per_class=150)

