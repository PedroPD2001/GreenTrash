"""
Script para executar o Streamlit garantindo o diretório correto.
"""
import os
import sys
import subprocess

# Obter diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("="*60)
print("GreenTrash - Iniciando Aplicação")
print("="*60)
print(f"\nDiretório: {script_dir}")
print("\nVerificando arquivos...")

# Verificar arquivos necessários
required = ['app.py', 'src/feature_extraction.py', 'src/classifier.py']
all_ok = True
for file in required:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} não encontrado")
        all_ok = False

if not all_ok:
    print("\n❌ Arquivos faltando! Verifique o diretório.")
    sys.exit(1)

print("\n✅ Todos os arquivos encontrados!")
print("\nIniciando Streamlit...")
print("A aplicação estará disponível em: http://localhost:8501")
print("\nPressione Ctrl+C para parar.\n")

# Executar Streamlit
try:
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--server.port', '8501',
        '--server.headless', 'true'
    ], cwd=script_dir)
except KeyboardInterrupt:
    print("\n\nAplicação encerrada pelo usuário.")
except Exception as e:
    print(f"\n❌ Erro ao executar: {e}")
    sys.exit(1)

