import os
import logging as log

EMAIL_DEBUG = 'qualidade.10@carvalima.com.br'

BASE_DIR = os.path.dirname(__file__)

PATH_DOWNLOADS = os.path.join(BASE_DIR, 'downloads')
PATH_RELATORIOS = os.path.join(BASE_DIR, 'relatorios')

# logging
LOG_FILENAME = None

log.basicConfig(
    level=log.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=LOG_FILENAME
)
logging = log.getLogger(__name__)
