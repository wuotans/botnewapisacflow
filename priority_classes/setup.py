from setuptools import setup, find_packages
import platform

# Determine the platform
if platform.system() == 'Windows':
    psycopg2_package = 'psycopg2-binary'
else:
    psycopg2_package = 'psycopg2-binary'
setup(
    name="priority_classes",
    version="3.0.0",
    packages=find_packages(),
    description='Priority Classes Package for carvalima bots',
    author='Ben-Hur P. B. Santos',
    author_email='benstronics@gmail.com',
    install_requires=[
        'selenium>=4',
        'webdriver-manager',
        'beautifulSoup4',
        'openpyxl',
        'gspread',
        'cryptography',
        'pandas',
        'oauth2client',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'customtkinter',
        'Pillow',
        'tkcalendar',
        psycopg2_package,
        'pyppeteer',
        ],
    )

# python setup.py sdist
# To run selenium on linux see https://tecadmin.net/setup-selenium-with-python-on-ubuntu-debian/
# or run the following commands on linux terminal:
# wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo apt update
# sudo apt install -f ./google-chrome-stable_current_amd64.deb
