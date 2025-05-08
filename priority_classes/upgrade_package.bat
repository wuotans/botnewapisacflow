REM Verificar versao instalado do python (este projeto foi feito em Python 3.11)
python --version

REM Ativar o ambiente virtual
call venv\Scripts\activate.bat

REM Atualizar PIP para última versão
python.exe -m pip install --upgrade pip

REM Upgrade packages
python -m pip install --upgrade cryptography
python -m pip install --upgrade certifi
python -m pip install --upgrade Pillow
python -m pip install --upgrade sphinx
python -m pip install --upgrade requests
python -m pip install --upgrade selenium

REM Freeze requirements
python -m pip freeze > requirements.txt

REM Listar pacotes instalados
pip list

