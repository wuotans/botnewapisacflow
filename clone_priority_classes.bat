@echo off
REM Remove o diretório priority_classes
rmdir /S /Q priority_classes
REM Clona o repositório
git clone git@github.com:cvltransportes/priority_classes.git
REM Muda para o diretório do repositório clonado
cd priority_classes

REM Remove o diretório .git
rmdir /S /Q .git

REM Opcional: Exibe uma mensagem de confirmação
echo Diretório .git removido com sucesso.
pause