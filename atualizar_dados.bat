@echo off
chcp 65001 >nul
title GHF - Atualizar Dados
color 0E

echo ============================================================
echo   GHF - Atualizar dados da planilha
echo ============================================================
echo.
echo Coloque sua planilha atualizada na pasta 'dados'
echo com o nome: CONTRATO DE EXPERIENCIA.xlsx
echo.

if exist "dados\CONTRATO DE EXPERIENCIA.xlsx" (
    echo Planilha encontrada! Importando...
    python database.py importar "dados\CONTRATO DE EXPERIENCIA.xlsx"
) else if exist "dados\CONTRATO DE EXPERIENCIA 14.07.xls" (
    echo Planilha alternativa encontrada! Importando...
    python database.py importar "dados\CONTRATO DE EXPERIENCIA 14.07.xls"
) else (
    echo Nenhuma planilha encontrada!
    echo.
    echo Opcoes:
    echo   1. Copie a planilha para a pasta 'dados'
    echo   2. Execute: python database.py importar [caminho_da_planilha]
    echo.
)

echo.
echo Verificando status do sistema...
python database.py status
echo.
pause
