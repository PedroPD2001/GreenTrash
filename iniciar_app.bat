@echo off
chcp 65001 >nul
echo ====================================
echo  GreenTrash - Iniciando Aplicação
echo ====================================
echo.

cd /d "%~dp0"

echo Verificando dependências...
py -c "import streamlit; print('Streamlit:', streamlit.__version__)" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Erro: Streamlit não encontrado!
    echo Instalando dependências...
    py -m pip install -r requirements.txt
)

echo.
echo Iniciando aplicação Streamlit...
echo.
echo A aplicação estará disponível em:
echo http://localhost:8501
echo.
echo Pressione Ctrl+C para parar o servidor.
echo.

streamlit run app.py --server.headless true

pause

