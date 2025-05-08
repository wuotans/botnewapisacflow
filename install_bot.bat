REM Verificar versao instalado do python
python --version

REM Crie um ambiente virtual em Python
python -m venv venv

REM Ativar o ambiente virtual
call venv\Scripts\activate.bat

REM Atualizar PIP para última versão
python.exe -m pip install --upgrade pip

REM Instalar pacotes necessários usando o arquivo requerimentos.txt
python -m pip install -r requirements.txt

REM Listar pacotes instalados
pip list

pause