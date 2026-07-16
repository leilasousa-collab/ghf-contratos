@echo off
chcp 65001 >nul
title GHF - Configurar Alertas
color 0C

echo ============================================================
echo   GHF - Configuracao de Alertas
echo ============================================================
echo.
echo O sistema de alertas envia notificacoes por:
echo   - E-mail (via Gmail)
echo   - WhatsApp (link direto)
echo.
echo Para configurar o e-mail:
echo   1. Acesse: https://myaccount.google.com/apppasswords
echo   2. Gere uma senha de app
echo   3. Edite o arquivo alerts.py e preencha:
echo      - gmail_usuario: seu-email@gmail.com
echo      - gmail_senha: senha-de-app-gerada
echo.

echo Configuracao atual:
python alerts.py config
echo.

echo Opcoes:
echo   1. Testar envio de e-mail
echo   2. Ver relatorio de alertas
echo   3. Enviar alertas pendentes agora
echo   4. Sair
echo.

set /p opcao="Escolha uma opcao (1-4): "

if "%opcao%"=="1" (
    set /p email="Digite o e-mail de teste: "
    python alerts.py teste_email !email!
) else if "%opcao%"=="2" (
    python alerts.py relatorio
) else if "%opcao%"=="3" (
    python alerts.py enviar
) else (
    echo Saindo...
)

echo.
pause
