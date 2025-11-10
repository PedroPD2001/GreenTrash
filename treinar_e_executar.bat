@echo off
chcp 65001 >nul
echo ====================================
echo  GreenTrash - Treinamento e Execução
echo ====================================
echo.

cd /d "%~dp0"

echo 1. Treinando modelo com imagens reais...
py train_model_real.py
echo.

if %ERRORLEVEL% NEQ 0 (
    echo Erro no treinamento. Continuando mesmo assim...
    echo.
)

echo 2. Iniciando aplicação Streamlit...
echo.
streamlit run app.py

