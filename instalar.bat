@echo off
chcp 65001 >nul
title GHF - Instalacao do Sistema
color 0A

echo ============================================================
echo   GHF - Sistema de Controle de Contratos de Experiencia
echo   INSTALADOR AUTOMATICO
echo ============================================================
echo.

REM Verificar se Python esta instalado
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo AVISO: Python nao encontrado!
    echo Por favor, instale Python primeiro:
    echo https://www.python.org/downloads/
    echo.
    echo Ou execute o instalador Python que esta na pasta do projeto.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYVER=%%a
echo Python encontrado: %PYVER%
echo.

REM Verificar/Instalar pip
echo [2/5] Verificando pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Instalando pip...
    python -m ensurepip --default-pip
)
echo pip OK.
echo.

REM Instalar dependencias
echo [3/5] Instalando dependencias...
echo.
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERRO ao instalar dependencias!
    echo Tentando instalacao manual...
    python -m pip install flask
    python -m pip install openpyxl
)
echo.
echo Dependencias instaladas!
echo.

REM Criar pastas
echo [4/5] Criando estrutura de pastas...
if not exist dados mkdir dados
if not exist templates mkdir templates
if not exist static mkdir static
if not exist static\css mkdir static\css
if not exist static\js mkdir static\js
echo Pastas criadas!
echo.

REM Importar dados
echo [5/5] Importando dados da planilha...
echo.
echo IMPORTANTE: Coloque sua planilha Excel na pasta 'dados'
echo com o nome: CONTRATO DE EXPERIENCIA.xlsx
echo.
echo Se ja existe uma planilha na pasta, ela sera importada.
echo.

if exist "dados\CONTRATO DE EXPERIENCIA.xlsx" (
    python database.py importar "dados\CONTRATO DE EXPERIENCIA.xlsx"
) else if exist "dados\CONTRATO DE EXPERIENCIA 14.07.xls" (
    python database.py importar "dados\CONTRATO DE EXPERIENCIA 14.07.xls"
) else (
    echo Nenhuma planilha encontrada na pasta dados.
    echo Coloque a planilha e execute: python database.py importar [caminho]
)
echo.

REM Criar usuario padrao
python database.py usuarios
echo.

echo ============================================================
echo   INSTALACAO CONCLUIDA!
echo ============================================================
echo.
echo Para iniciar o sistema:
echo   python app.py
echo.
echo Acesse pelo navegador:
echo   http://localhost:5000
echo.
echo Login padrao:
echo   E-mail: dp@ghf.com
echo   Senha:  123456
echo.
echo Para outros computadores na rede, use o IP desta maquina.
echo ============================================================
echo.
pause
