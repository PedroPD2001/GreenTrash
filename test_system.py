"""
Script de teste simples para validar o sistema.
Testa classificação com diferentes entradas textuais.
"""

from src.feature_extraction import FeatureExtractor
from src.classifier import WasteClassifier


def test_classification():
    """Testa classificação com diferentes exemplos."""
    
    print("="*60)
    print("TESTE DO SISTEMA DE CLASSIFICAÇÃO")
    print("="*60)
    
    # Inicializar
    print("\n1. Inicializando componentes...")
    extractor = FeatureExtractor()
    classifier = WasteClassifier()
    
    if classifier.model is None:
        print("\n⚠️ AVISO: Modelo não treinado. Execute 'python train_model.py' primeiro.")
        print("Usando classificação fallback (apenas texto).\n")
    
    # Exemplos de teste
    test_cases = [
        ("Orgânico", "casca de banana e restos de alface"),
        ("Reciclável", "garrafa de plástico pet transparente"),
        ("Rejeito", "papel higiênico usado fralda"),
        ("Perigoso", "pilha bateria lâmpada fluorescente"),
        ("Ambíguo", "celular quebrado plástico metal"),
    ]
    
    print("2. Testando classificação...\n")
    
    for expected, text in test_cases:
        print(f"Teste: {expected}")
        print(f"Entrada: '{text}'")
        
        # Extrair features
        features = extractor.extract_combined_features(text=text)
        
        # Classificar
        result = classifier.predict(features)
        
        # Mostrar resultado
        print(f"Resultado: {result['classe']}")
        print(f"Confiança: {result['confianca']:.1%}")
        print(f"Explicação: {result['explicacao']}")
        print(f"Dica: {result['dica_descarte']}")
        
        # Verificar se está correto (só para casos não ambíguos)
        if expected != "Ambíguo":
            status = "✓" if result['classe'] == expected else "✗"
            print(f"Status: {status}")
        
        print("-" * 60)
        print()
    
    print("="*60)
    print("✓ Testes concluídos!")
    print("="*60)


if __name__ == "__main__":
    test_classification()

