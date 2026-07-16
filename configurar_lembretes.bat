@echo off
chcp 65001 >nul
title GHF - Configurar Lembretes Automaticos
color 0B

echo ============================================================
echo   GHF - Configurar Lembretes Automaticos
echo ============================================================
echo.
echo O lembrete sera enviado automaticamente nos dias 1 e 15 de
echo cada mes para: dp@grupohiperfarma.far.br
echo.

REM Criar tarefa agendada
echo Criando tarefa agendada...

schtasks /create /tn "GHF Lembrete Dia 1" /tr "\"C:\Users\leila\AppData\Local\Programs\Python\Python315\python.exe\" \"C:\Users\leila\OneDrive\docmentos\Documentos\New OpenCode Project\projeto-ghf\lembretes.py\"" /sc monthly /d 1 /st 08:00 /f

schtasks /create /tn "GHF Lembrete Dia 15" /tr "\"C:\Users\leila\AppData\Local\Programs\Python\Python315\python.exe\" \"C:\Users\leila\OneDrive\docmentos\Documentos\New OpenCode Project\projeto-ghf\lembretes.py\"" /sc monthly /d 15 /st 08:00 /f

echo.
echo ============================================================
echo   LEMBRETES CONFIGURADOS!
echo ============================================================
echo.
echo Tarefas criadas:
echo   - GHF Lembrete Dia 1 (todo dia 1 as 08:00)
echo   - GHF Lembrete Dia 15 (todo dia 15 as 08:00)
echo.
echo Para verificar: schtasks /query /tn "GHF*"
echo Para remover: schtasks /delete /tn "GHF*" /f
echo.
pause
