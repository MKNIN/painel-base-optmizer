@echo off
chcp 65001 >nul
title Windows Optimizer Ultimate
cls

echo ========================================
echo    WINDOWS OPTIMIZER ULTIMATE
echo ========================================
echo.

:: Descobre automaticamente onde o BAT está executando
set "PASTA_ATUAL=%~dp0"
echo Procurando painel em: %PASTA_ATUAL%

:: Verifica se o arquivo principal existe
if exist "%PASTA_ATUAL%windows_optimizer_ultimate.py" (
    echo Arquivo principal encontrado!
    cd /d "%PASTA_ATUAL%"
    goto EXECUTAR
)

:: Se não encontrou, procura em subpastas
echo Procurando em subpastas...
for /r "%PASTA_ATUAL%" %%i in (windows_optimizer_ultimate.py) do (
    if exist "%%i" (
        set "PASTA_ENCONTRADA=%%~dpi"
        echo Encontrado em: %%i
        cd /d "%%~dpi"
        goto EXECUTAR
    )
)

echo.
echo ERRO: Arquivo windows_optimizer_ultimate.py nao encontrado!
echo.
echo Coloque este arquivo BAT na mesma pasta do seu painel.
echo.
pause
exit

:EXECUTAR
echo.
echo Iniciando Windows Optimizer Ultimate...
echo.

:: Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Instale o Python em: https://python.org
    echo.
    pause
    exit
)

:: Executa o painel
python windows_optimizer_ultimate.py

echo.
echo Painel finalizado.
pause