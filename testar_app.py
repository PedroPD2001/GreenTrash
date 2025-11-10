"""
Teste rápido do app para verificar erros.
"""
import os
import sys

# Mudar para diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

print("Testando imports...")
try:
    from src.feature_extraction import FeatureExtractor
    from src.classifier import WasteClassifier
    print("✓ Imports OK")
except Exception as e:
    print(f"✗ Erro nos imports: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTestando inicialização...")
try:
    extractor = FeatureExtractor()
    classifier = WasteClassifier()
    print("✓ Inicialização OK")
except Exception as e:
    print(f"✗ Erro na inicialização: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ Tudo OK! O app pode ser executado.")
print("\nExecute: streamlit run app.py")

