@echo off
title GHF - Encerrar Sistema
color 0C

echo ========================================
echo   Encerrando servidor GHF...
echo ========================================

taskkill /F /IM python.exe >nul 2>&1

echo.
echo Servidor encerrado!
timeout /t 3 /nobreak >nul
