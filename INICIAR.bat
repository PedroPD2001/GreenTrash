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

echo Verificando ambiente Python...
for /f "tokens=1,2" %%a in ('py -c "import struct,platform; print(struct.calcsize(\"P\")*8, platform.machine())"') do (
    set PY_BITS=%%a
    set PY_MACHINE=%%b
)
echo Python: %PY_BITS%-bit %PY_MACHINE%
if "%PY_BITS%"=="32" (
    echo AVISO: Python 32-bit detectado. scikit-image pode falhar na instalacao.
    echo A aplicacao funcionara sem recursos visuais completos.
)

echo Atualizando pip...
py -m pip install --upgrade pip >nul 2>&1

echo Instalando dependencias do requirements.txt...
py -m pip install --user -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Aviso: Falha ao instalar alguns requisitos do requirements.txt.
    echo Tentando instalar dependencias basicas sem scikit-image...
    py -m pip install --user streamlit==1.28.0 opencv-python==4.8.1.78 scikit-learn==1.3.2 numpy==1.24.3 pandas==2.1.3 Pillow==10.1.0 matplotlib==3.8.2 joblib==1.3.2
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

REM Executar Streamlit via Python launcher
py -m streamlit run app.py

pause