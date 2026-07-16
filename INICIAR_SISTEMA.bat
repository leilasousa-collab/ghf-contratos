@echo off
title GHF - Sistema de Contratos
color 0A

echo ========================================
echo   GHF - Sistema de Contratos
echo   Iniciando servidor...
echo ========================================

set PYTHON=C:\Users\leila\AppData\Local\Programs\Python\Python315\python.exe
set PROJETO=C:\Users\leila\OneDrive\docmentos\Documentos\New OpenCode Project\projeto-ghf

cd /d "%PROJETO%"

echo.
echo [1/3] Iniciando servidor Flask...
start "GHF Servidor" /B "%PYTHON%" "%PROJETO%\app.py"

echo [2/3] Aguardando servidor...
timeout /t 4 /nobreak >nul

echo [3/3] Abrindo navegador...
start "" "http://127.0.0.1:5000"

echo.
echo ========================================
echo   Servidor GHF rodando!
echo   Feche esta janela para encerrar
echo ========================================
timeout /t 5 /nobreak >nul
