@echo off
chcp 65001 >nul
title GreenTrash - Treinamento

cd /d "%~dp0"

echo ====================================
echo   GreenTrash - Treinamento Melhorado
echo ====================================
echo.

py train_model_real.py

pause

