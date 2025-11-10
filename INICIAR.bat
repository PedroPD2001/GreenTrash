@echo off
chcp 65001 >nul
title GreenTrash - Aplicacao

REM Mudar para o diretório do script
cd /d "%~dp0"

echo ====================================
echo   GreenTrash - Iniciando Aplicacao
echo ====================================
echo.
echo Diretorio: %CD%
echo.

REM Verificar se app.py existe
if not exist "app.py" (
    echo ERRO: app.py nao encontrado!
    echo Certifique-se de executar este script na pasta do projeto.
    pause
    exit /b 1
)

echo Verificando dependencias...
py -c "import streamlit" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Streamlit nao encontrado. Instalando...
    py -m pip install streamlit
)

echo.
echo Iniciando aplicacao Streamlit...
echo.
echo ====================================
echo   A aplicacao estara disponivel em:
echo   http://localhost:8501
echo ====================================
echo.
echo Pressione Ctrl+C para parar o servidor.
echo.

REM Executar Streamlit
streamlit run app.py

pause

