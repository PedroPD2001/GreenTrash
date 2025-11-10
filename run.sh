#!/bin/bash

echo "===================================="
echo " IA Resíduos - Classificação de Resíduos"
echo "===================================="
echo ""

# Verificar se ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
    echo ""
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate
echo ""

# Instalar dependências
echo "Verificando dependências..."
pip install -q -r requirements.txt
echo ""

# Verificar se modelo existe
if [ ! -f "models/waste_classifier.pkl" ]; then
    echo "Modelo não encontrado! Treinando..."
    echo ""
    python train_model.py
    echo ""
    echo "Pressione Enter para continuar..."
    read
fi

# Executar aplicação
echo "Iniciando aplicação Streamlit..."
echo ""
streamlit run app.py

