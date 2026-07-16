@echo off
chcp 65001 >nul
title GHF - Iniciar Sistema
color 0B

echo ============================================================
echo   GHF - Sistema de Controle de Experiencia
echo   Iniciando servidor...
echo ============================================================
echo.

REM Verificar se o banco existe
if not exist "dados\contratos.db" (
    echo Banco de dados nao encontrado!
    echo Executando instalacao primeiro...
    call instalar.bat
)

REM Verificar dependencias
python -c "import flask; import openpyxl" 2>nul
if errorlevel 1 (
    echo Dependencias nao instaladas!
    echo Executando instalacao...
    call instalar.bat
)

echo Iniciando sistema...
echo.
echo Acesse: http://localhost:5000
echo.
echo Para parar, pressione Ctrl+C
echo ============================================================
echo.

python app.py
