"""
Script para iniciar o Streamlit garantindo o diretório correto.
Execute: py start_app.py
"""
import os
import sys
import subprocess

# Obter diretório absoluto do script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

print("="*60)
print("GreenTrash - Iniciando Aplicação")
print("="*60)
print(f"\nDiretório: {script_dir}")

# Verificar se app.py existe
if not os.path.exists('app.py'):
    print("\n❌ ERRO: app.py não encontrado!")
    print(f"   Diretório atual: {os.getcwd()}")
    sys.exit(1)

print("✓ app.py encontrado")

# Verificar imports
print("\nVerificando imports...")
try:
    from src.feature_extraction import FeatureExtractor
    from src.classifier import WasteClassifier
    print("✓ Imports OK")
except Exception as e:
    print(f"✗ Erro nos imports: {e}")
    print("\nTentando continuar mesmo assim...")

print("\n" + "="*60)
print("Iniciando Streamlit...")
print("="*60)
print("\n🌐 A aplicação estará disponível em:")
print("   http://localhost:8501")
print("\n⚠️  Pressione Ctrl+C para parar o servidor")
print("\n" + "="*60 + "\n")

# Executar Streamlit
try:
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--server.port', '8501'
    ], cwd=script_dir)
except KeyboardInterrupt:
    print("\n\n✅ Aplicação encerrada pelo usuário.")
except Exception as e:
    print(f"\n❌ Erro ao executar Streamlit: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

