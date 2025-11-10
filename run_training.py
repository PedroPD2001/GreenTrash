"""
Script auxiliar para executar o treinamento.
Garante que está no diretório correto.
"""
import os
import sys

# Obter diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Adicionar ao path
sys.path.insert(0, script_dir)

# Executar treinamento
if __name__ == "__main__":
    from train_model_real import train_model_with_real_images
    train_model_with_real_images()

