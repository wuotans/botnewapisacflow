@echo off
REM Remove o diretório cvl_apis_framework
rmdir /S /Q cvl_apis_framework
REM Clona o repositório
git clone git@github.com:cvltransportes/cvl_apis_framework.git
REM Muda para o diretório do repositório clonado
cd cvl_apis_framework

REM Remove o diretório .git
rmdir /S /Q .git

REM Opcional: Exibe uma mensagem de confirmação
echo Diretório .git removido com sucesso.
pause