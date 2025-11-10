@echo off
echo ====================================
echo  IA Residuos - Classificacao de Residuos
echo ====================================
echo.

REM Verificar se ambiente virtual existe
if not exist "venv\" (
    echo Criando ambiente virtual...
    python -m venv venv
    echo.
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo.

REM Instalar dependencias
echo Verificando dependencias...
pip install -q -r requirements.txt
echo.

REM Verificar se modelo existe
if not exist "models\waste_classifier.pkl" (
    echo Modelo nao encontrado! Treinando...
    echo.
    python train_model.py
    echo.
    echo Pressione qualquer tecla para continuar...
    pause >nul
)

REM Executar aplicacao
echo Iniciando aplicacao Streamlit...
echo.
streamlit run app.py

