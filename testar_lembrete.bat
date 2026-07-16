@echo off
chcp 65001 >nul
title GHF - Testar Lembrete
color 0A

echo ============================================================
echo   GHF - Testar Envio de Lembrete
echo ============================================================
echo.
echo Enviando email de teste para: dp@grupohiperfarma.far.br
echo.

"C:\Users\leila\AppData\Local\Programs\Python\Python315\python.exe" lembretes.py forcar dp@grupohiperfarma.far.br

echo.
echo Verifique a caixa de entrada do e-mail!
echo.
pause
