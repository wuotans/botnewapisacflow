@echo off
REM Remove o diretório cvl_ssw_pkg
rmdir /S /Q cvl_ssw_pkg
REM Clona o repositório
git clone git@github.com:cvltransportes/cvl_ssw_pkg.git
REM Muda para o diretório do repositório clonado
cd cvl_ssw_pkg

REM Remove o diretório .git
rmdir /S /Q .git

REM Opcional: Exibe uma mensagem de confirmação
echo Diretório .git removido com sucesso.
pause