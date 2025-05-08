import logging
import re
import shutil
import platform
import time
import os
import zipfile
from cryptography.fernet import Fernet
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from urllib.parse import urlencode, unquote
import pandas as pd
import requests
import asyncio
from pyppeteer import launch
from priority_classes.decorators.decorators import time_out
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
class EmptyValue(Exception):
    pass


class NotFound(Exception):
    pass


class Web:

    def __init__(self):
        self.method = None
        self.driver:webdriver.Chrome = None
        self.action = None
        self.session = requests.Session()
        self.cookies = None
        self.token = None
        self.path_to_downloads = 'downloads'

    def create_folder(self, path):
        path = os.path.abspath(path)
        os.makedirs(path, exist_ok=True)
        return path

    def create_file_txt(self, text: str = '', name_file: str = '', path_to_save: str = '', subs: bool = False):
        path_to_save = self.create_folder(path_to_save)
        full_path_file = os.path.abspath(f'{path_to_save}/{name_file}.txt')

        if not os.path.exists(full_path_file) or subs:
            with open(full_path_file, 'w') as f:
                f.write(text)
        else:
            with open(full_path_file, 'r') as f:
                text = f.read()
        return text

    @staticmethod
    def move_file(from_path_file, to_path_file):
        """
        Move a file from the source location to the destination location.

        :param from_path_file: Source file path.
        :type from_path_file: str
        :param to_path_file: Destination file path.
        :type to_path_file: str
        """
        shutil.copy2(from_path_file, to_path_file)

    def wait_download(self, timeout: int = 3600, ext_optional: str = 'txt'):
        # tuple of commom extentions in the project to download
        use_to_ext = ('xls', 'csv', 'sswweb', 'json', 'pdf','xlsx', ext_optional)

        # loop over path download until file be found
        contador_while = 0
        while contador_while < timeout:
            # getting the files extentions
            files = os.listdir(self.path_to_downloads)
            ext_files_list = [str(file_name).split('.')[-1].lower() for file_name in files]
            logging.info('Arquivos encontrados: \n',files)
            logging.info('Extensões encontradas: \n',ext_files_list)
            found = [True for ext in ext_files_list if ext in use_to_ext]
            part = [True for ext in ext_files_list if 'part' in ext] #arquivos não concluidos!
            logging.info("Part: \n",part)
            if any(found) and not part:
                logging.info('Arquivo baixado!')
                break
            contador_while += 1
            time.sleep(1)

    def define_profile_path(self, name_instance, subs: bool = True):
        system = platform.system()
        path_store_profile = '.bot_profile_chrome' if system == 'Linux' else os.path.dirname(os.getenv('APPDATA')) + '/profile_chrome'

        path_store_profile = os.path.abspath(os.path.join(path_store_profile, name_instance))
        counter = 0
        while os.path.exists(path_store_profile):
            try:
                os.remove(path_store_profile)
            except PermissionError:
                pass
            except Exception as e:
                logging.exception(e)
            counter += 1
            path_store_profile = os.path.abspath(os.path.join(path_store_profile, f'{name_instance}_{counter}'))
        if not os.path.exists(path_store_profile):
            os.makedirs(path_store_profile, exist_ok=True)

        profile_path = self.create_file_txt(path_store_profile, 'profile_path_browser', 'parameters', subs)
        return profile_path

    def init_browser(self, profile_path: str = 'Default', ignore_profile: bool = True, path_to_downloads='downloads',
                     headless: bool = True, driver: str = 'edge', method: str = 'selenium',force_drive:bool=False, more_options:dict={},**kwargs):
        """
        Initializes the web browser.

        :param method:
        :param driver:
        :param headless:
        :param name_instance: Name of the browser instance, defaults to 'Default'
        :type name_instance: str, optional
        :param ignore_profile: Whether to ignore the profile, defaults to True
        :type ignore_profile: bool, optional
        :param path_to_downloads: Path to the downloads folder, defaults to 'downloads'
        :type path_to_downloads: str, optional
        """
        self.path_to_downloads = self.create_folder(path_to_downloads)

        profile_path = self.create_folder(profile_path)#self.define_profile_path(name_instance)
        self.method = method
        self.method = self.create_file_txt(self.method, 'config_method_browser', 'config',True)
        if not force_drive:
            driver = self.create_file_txt(driver, 'config_driver_browser', 'config',True)

        if 'selenium' == self.method:
            if driver == 'chrome':
                self.chrome_driver(self.path_to_downloads, profile_path, ignore_profile, headless, more_options=more_options,**kwargs)
                self.action = ActionChains(self.driver)
            elif driver == 'edge':
                self.edge_driver(self.path_to_downloads, profile_path, ignore_profile, headless, more_options=more_options,**kwargs)
                self.action = ActionChains(self.driver)
            elif driver in ['firefox', 'mozilla']:
                self.firefox_driver(self.path_to_downloads, profile_path, ignore_profile, headless,**kwargs)
                self.action = ActionChains(self.driver)

        elif 'pypperteer' == self.method:
            from pyppeteer import launch
            asyncio.get_event_loop().run_until_complete(self.pypperteer_browser(headless, profile_path))
            # thread = Thread(target=self.run_async_method, args=(headless, profile_path))
            # thread.start()
            # thread.join()

    def chromedriver_install(self):
        try:
            ZIP = 'chromedriver.zip'
            resp = requests.get(
                'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json')
            chromedrivers = resp.json()['channels']['Stable']['downloads']['chromedriver']
            url_win64 = [chromedriver["url"] for chromedriver in chromedrivers if "win64" in chromedriver["platform"]][
                0]
            resp = requests.get(url_win64)
            with open(ZIP, 'wb') as f:
                f.write(resp.content)
            self.create_folder('chromedriver')
            # Open the zip file in read mode
            with zipfile.ZipFile(ZIP, 'r') as zip_ref:
                # Extract all the files
                zip_ref.extractall('chromedriver')
            os.remove(ZIP)
        except PermissionError as e:
            pass
        return os.path.abspath('chromedriver/chromedriver-win64/chromedriver.exe')

    def chrome_driver(self, path_to_downloads, profile_path, ignore_profile, headless, more_options:dict={},**kwargs):
        options = Options()
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")

        if more_options.get('enable_edge_arguments', None):
            options.add_argument("--log-level=3")  # Define o nível de logging (3=error)
            options.add_argument("start-maximized")  # Inicia maximizado
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--lang=pt-BR")
            # options.add_argument("--disable-dev-shm-usage")
            # options.add_argument("--ignore-ssl-errors=yes")
            # options.add_argument("--ignore-certificate-errors")
            # options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # options.add_argument("--disable-software-rasterizer")
            # options.add_argument("--disable-infobars")
            # options.add_argument("--remote-debugging-port=9222")

            # # options.add_argument("disable-features=IsolateOrigins,site-per-process")
            # # options.add_argument("disable-web-security")

            # options.add_argument("--disable-blink-features=AutomationControlled")
            # options.add_argument("--disable-translate")
            # options.add_argument("--disable-features=NetworkService")

            # options.add_argument("--disable-gpu")
            # # habilita suporte a alta resolução
            # options.add_argument("--high-dpi-support=1")
            # # define o fator de escala para 1 (DPI 100%)
            # options.add_argument("--force-device-scale-factor=1")
            # # define a resolução da janela do navegador
        
        options.add_experimental_option("prefs", {
            "intl.accept_languages": "pt-BR,pt",
            "download.default_directory": path_to_downloads,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
            "download.extensions_to_open": "applications/pdf",
            'plugins.always_open_pdf_externally': True
        })
        if more_options.get('multiplos_downloads', None):
            options.add_argument("--incognito")  # Modo incógnito
            options.add_experimental_option("prefs", {
            "intl.accept_languages": "pt-BR,pt",
            "download.default_directory": path_to_downloads,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
            "profile.default_content_settings.popups": 0,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
            "download.extensions_to_open": "applications/pdf",
            "safebrowsing.disable_download_protection": True,
            "plugins.always_open_pdf_externally": True,
    })
        add_extensions = kwargs.pop('add_extensions',None)
        if add_extensions:
            if isinstance(add_extensions,list):
                for ext in add_extensions:
                    if not os.path.exists(ext):
                        raise ValueError(
                            f"Invalid value for extension: {ext}. It needs to be a existing os.path"
                        )
                    options.add_extension(ext)
            elif isinstance(add_extensions,str) and os.path.exists(add_extensions):
                options.add_extension(ext)
            else:
                raise ValueError(
                    f"Invalid value for extension: {add_extensions}. It needs to be a existing os.path"
                )

        # Trying to use ChromeDriverManager to get the latest driver
        #path_chrome_driver = self.chromedriver_install()

        if len(profile_path) > 0 and not ignore_profile:
            options.add_argument(f"user-data-dir={profile_path}")

        if headless:
            options.add_argument('headless')

        self.driver = webdriver.Chrome(options=options)#executable_path=path_chrome_driver,

    def firefox_driver(self, path_to_downloads, profile_path, ignore_profile, headless,**kwargs):
        logging.info('...FirefoxDriver Option...')
        options = FirefoxOptions()
        # options = webdriver.FirefoxOptions()

        if len(profile_path) > 0 and not ignore_profile:
            options.set_preference("profile", profile_path)

        if headless:
            options.add_argument("--headless")

        options.log.level = "fatal"  # Define o nível de logging (fatal)
        options.add_argument("--start-maximized")  # Inicia maximizado
        options.add_argument("--window-size=1000,700")  # Define o tamanho da janela
        options.add_argument("--disable-dev-shm-usage")  # Problemas de memória compartilhada no Docker
        options.add_argument("--disable-extensions")  # Desativar extensões para reduzir uso de memória
        options.add_argument("--disable-popup-blocking")  # Desativar bloqueio de pop-ups
        options.add_argument("--incognito")
        options.add_argument("--disable-gpu")  # Necessário para alguns sistemas

        # Adiciona preferências específicas do Firefox
        logging.info('path_to_downloads',path_to_downloads)
        options.set_preference("browser.download.dir", path_to_downloads)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # Ajuste conforme necessário
        options.set_preference("pdfjs.disabled", True)  # Desativa visualizador PDF interno do Firefox
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.download.panel.shown", False)
        self.driver = webdriver.Firefox(options=options)
        #self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)

    def edge_driver(self, path_to_downloads, profile_path, ignore_profile, headless, more_options:dict={},**kwargs):
        logging.info('...Edgedriver Option...')
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        if len(profile_path) > 0 and not ignore_profile:
            options.add_argument(f"--user-data-dir={profile_path}")

        if headless:
            options.add_argument('--headless')
            #options.headless = Falsep
            if more_options.get('enable_edge_arguments', None):
                options.add_argument("--headless=new")  # Modo headless, novo comportamento

        if more_options.get('enable_edge_arguments', None):
            logging.info('...entering... in more options....')
            options.add_argument("--log-level=3")  # Define o nível de logging (3=error)
            options.add_argument("start-maximized")  # Inicia maximizado
            # options.add_argument("--window-size=1000,700")  # Define o tamanho da janela
            options.add_argument("--disable-dev-shm-usage")  # Problemas de memória compartilhada no Docker
            options.add_argument("--disable-extensions")  # Desativar extensões para reduzir uso de memória
            options.add_argument("--disable-popup-blocking")  # Desativar bloqueio de pop-ups
            options.add_argument("--incognito")
            # options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Exclui o logging do navegador
            # options.add_argument("--high-dpi-support=1")  # Habilita suporte a DPI alto
            # options.add_argument("--force-device-scale-factor=1")  # Força o fator de escala do dispositivo para 1
            options.add_argument('--disable-gpu')  # Necessário para alguns sistemas
            # options.add_argument("--headless=new")  # Modo headless, novo comportamento
            # options.add_argument('--no-sandbox')  # Desabilita o sandbox
            # options.add_argument('--disable-dev-shm-usage')  # Desabilita /dev/shm
            # options.add_argument('--disable-extensions')  # Desabilita extensões
            # options.add_argument('--disable-software-rasterizer')  # Desabilita rasterização de software
            # options.add_argument('--disable-web-security')  # Desabilita a segurança da web (usar com cautela)
            # options.add_argument('--allow-running-insecure-content')  # Permite conteúdo inseguro (usar com cautela)
            # options.add_argument('--enable-logging')  # Habilita o logging
            # options.add_argument('--v=1')  # Nível de verbosity do logging
            # options.add_argument('--disable-popup-blocking')  # Desabilita o bloqueio de pop-ups
            # options.add_argument("--disable-renderer-backgrounding")  # Desabilita fundo do renderizador
            # options.add_argument("--disable-background-timer-throttling")  # Desabilita limitação do temporizador em segundo plano
            # options.add_argument("--disable-backgrounding-occluded-windows")  # Desabilita janelas ocultas em segundo plano
            # options.add_argument("--disable-client-side-phishing-detection")  # Desabilita detecção de phishing no lado do cliente
            # options.add_argument("--disable-crash-reporter")  # Desabilita o relatório de crashes
            # options.add_argument("--disable-oopr-debug-crash-dump")  # Desabilita o dump de crash OOPR debug
            # options.add_argument("--no-crash-upload")  # Não faz upload de crashes
            # options.add_argument("--disable-low-res-tiling")  # Desabilita tiling de baixa resolução
            # options.add_argument("--log-level=3")  # Define o nível de logging (3=error)
            # options.add_argument("--silent")  # Roda em modo silencioso
            # options.add_argument("headless")  # Roda o navegador no modo headless
        experimental_options = {
            "download.default_directory": f"{path_to_downloads}"
        }
        if more_options.get('multiplos_downloads', None):
            experimental_options["profile.default_content_settings.popups"] = 0
            experimental_options["download.prompt_for_download"] = False
            experimental_options["download.directory_upgrade"] = True
            experimental_options["safebrowsing.enabled"] = True
            experimental_options["safebrowsing.disable_download_protection"] = True
            experimental_options["profile.content_settings.exceptions.automatic_downloads.*.setting"] = 1  # Habilita múltiplos downloads

        options.add_experimental_option("prefs", experimental_options)

        add_extensions = kwargs.pop('add_extensions',None)
        if add_extensions:
            if isinstance(add_extensions,list):
                for ext in add_extensions:
                    if not os.path.exists(ext):
                        raise ValueError(
                            f"Invalid value for extension: {ext}. It needs to be a existing os.path"
                        )
                    options.add_extension(ext)
            elif isinstance(add_extensions,str) and os.path.exists(add_extensions):
                options.add_extension(ext)
            else:
                raise ValueError(
                    f"Invalid value for extension: {add_extensions}. It needs to be a existing os.path"
                )
            



            

        #path_to = os.path.abspath('edgedriver/msedgedriver.exe')
        # try:
        #     #path_default = EdgeChromiumDriverManager().install()
        #     self._create_folder('edgedriver')
        #     self.move_file(path_default, path_to)
        # except PermissionError as e:
        #     pass

        self.driver = webdriver.Edge(options=options)#executable_path=path_to,

    async def pypperteer_browser(self, headless, instance, ignore_profile):
        if not ignore_profile:
            self.create_folder('profile_pypperteer')
            path_ = self.create_folder(f'profile_pypperteer/{instance}')
        else:
            path_ = None
        self.driver = await launch(headless=headless,
                                   executablePath=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                                   userDataDir=path_,
                                   defaultViewport={'width': 1000, 'height': 900}
                                   )

    async def _login_with_pypperteer(self, url, script, time_wait):

        self.page = await self.driver.newPage()

        await self.page.goto(url)

        ret = await self.page.evaluate(f'''() => {{
                {script};
            }}''')

        # await page.click("a[id='5']")
        # await page.close()

        await asyncio.sleep(time_wait)

        # Get cookies from Pyppeteer
        cookies_list = await self.page.cookies()

        # Close the browser
        # await browser.close()

        for cookie in cookies_list:
            self.session.cookies.set(cookie['name'], cookie['value'])

        self.cookies = cookies_list

        return ret

    def login_puppyteer(self, url, script, time_wait: int = 3):
        return asyncio.get_event_loop().run_until_complete(self._login_with_pypperteer(url, script, time_wait))

    async def _get_cookies_pypperteer(self):

        # Get cookies from Pyppeteer
        cookies_list = await self.page.cookies()
        if len(cookies_list) > 0:
            for cookie in cookies_list:
                self.session.cookies.set(cookie['name'], cookie['value'])

            self.cookies = cookies_list
        else:
            raise EmptyValue

    @time_out()
    def get_cookies_pypperteer(self):
        return asyncio.get_event_loop().run_until_complete(self._get_cookies_pypperteer())

    async def _get_html_page_pypperteer(self):

        # Get cookies from Pyppeteer
        content = await self.page.content()
        return content

    @time_out()
    def get_html_page_pypperteer(self):
        return asyncio.get_event_loop().run_until_complete(self._get_html_page_pypperteer())

    async def _execute_script_pypperteer(self, script, time_wait):

        ret = await self.page.evaluate(f'''() => {{
                {script};
            }}''')

        # await page.click("a[id='5']")
        # await page.close()

        await asyncio.sleep(time_wait)

        return ret

    def execute_script_pypperteer(self, script, time_wait: int = 3):
        return asyncio.get_event_loop().run_until_complete(self._execute_script_pypperteer(script, time_wait))

    async def _send_keys_pypperteer(self, element, value_to_send):
        await self.page.focus(element)
        await self.page.type(element, value_to_send)

    def send_keys_pypperteer(self, element, value_to_send):
        return asyncio.get_event_loop().run_until_complete(self._send_keys_pypperteer(element, value_to_send))

    @time_out()
    def get_cookies(self):
        """
        Retrieves cookies from the current session of the browser and stores them in the `session` property of the class.
        The retrieval of cookies is managed by the `time_out` decorator to prevent hanging in case of failure.

        :Example:

            self._get_cookies()

        :raises: EmptyValue if no cookies are retrieved from the current session.
                 TimeoutException if unable to retrieve cookies after the specified timeout period.
        """
        self.cookies = self.driver.get_cookies()

        if len(self.cookies) == 0:
            raise EmptyValue

        for cookie in self.cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

    @time_out()
    def get_bearer_authorization_from_storage(self):
        """
            Retrieves the bearer authorization token from the SacFlow application.

            This method retrieves the bearer authorization token stored in the local storage of the browser. It executes a JavaScript script to retrieve the token and assigns it to the `self.token` attribute. If the token is `None`, it raises a `NotFound` exception.

            :raises NotFound: If the bearer authorization token is not found.
            :return: The bearer authorization token.
            :rtype: str
        """
        script = """
        var token = localStorage.getItem('token');
        console.log(token);
        return token
        """
        self.token = self.driver.execute_script(script)
        logging.info(self.token)
        if self.token is None:
            raise NotFound

        self.token = f"Bearer {self.token}"
        return self.token

    def convert_query_url_to_dict(self, query, empty_values: bool = True):
        """
        Converts a query URL into a dictionary.

        :param query: The query URL to convert
        :type query: str
        :param empty_values: Whether to empty the values, defaults to True
        :type empty_values: bool, optional
        :return: The dictionary obtained from the query URL
        :rtype: dict
        """
        dict_query = {}
        query_list = query.split('&')
        for param in query_list:
            param_list = param.split('=')
            if not empty_values:
                dict_query[param_list[0]] = param_list[1]
            else:
                dict_query[param_list[0]] = ''
        return dict_query

    def convert_dict_to_query_url(self, dict_query):
        """
        Converts a dictionary into a query URL.

        :param dict_query: The dictionary to convert
        :type dict_query: dict
        :return: The query URL obtained from the dictionary
        :rtype: str
        """
        query_format = []
        for key in dict_query:
            query_format.append(f'{key}={dict_query[key]}')
        return '&'.join(query_format)

    def show_kwargs_possible_values(self, html, query_model):
        """
        Displays the possible keys that can be passed to a function as keyword arguments (kwargs).
        This method takes an HTML document and a query model as arguments. It parses the HTML document
        to extract input tags, and for each key in the query model, it finds the corresponding input tag
        and its next sibling div tag in the HTML document. It then prints the name and value of each parameter
        in the console.

        :param html: The HTML document to be parsed.
        :type html: str

        :param query_model: The query model that contains the keys to be searched in the HTML document.
        :type query_model: str

        :return: None
        :rtype: None

        :Example:

            >>>self.show_kwargs_possible_values("<html>...</html>", "key1=value1&key2=value2")

        :process:
        1. The method converts the query model into a dictionary of parameters.
        2. It finds the input tag corresponding to each key in the parameters dictionary in the HTML document.
        3. If the input tag is found, it finds its next sibling div tag and extracts its text value.
        4. It then prints the name and value of the parameter.
        5. If the input tag is not found, it continues with the next key.
        """

        # Create a BeautifulSoup object
        soup = BeautifulSoup(html, 'html.parser')

        additional_params = self.convert_query_url_to_dict(query_model)
        logging.info('"""')
        logging.info('    :param kwargs:')
        logging.info('    Possible keys include:')
        for key in additional_params:
            try:
                # Find the input tag
                input_tag = soup.find('input', attrs={'name': key})

                if input_tag is not None:
                    # Find the div tag
                    div_tag = input_tag.find_next_sibling('div')

                    # Extract the query parameter name and value
                    param_name = input_tag['name']
                    param_value = div_tag.text.strip().replace('&nbsp;', '').replace(' ', '')

                    # Build the query string
                    query = f'        - {param_name}: {param_value}'

                    logging.info(query)
            except KeyError:
                pass
        logging.info('    :type kwargs: dict')
        logging.info('    :return: None')
        logging.info('"""')

    def update_query_values(self, html, query_model, attribute: str = 'id', **kwargs):
        """
        Update the values in the query string of the query model.

        :param html: The HTML content of the page.
        :type html: str
        :param query_model: The query model string or dict.
        :type query_model: str
        :param attribute: The attribute to search for in the input tags.
        :type attribute: str
        :param kwargs: Additional key-value pairs to update in the query string.
        :type kwargs: dict
        :return: The updated query string.
        :rtype: str
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Find all input tags in the HTML
        inputs = soup.find_all('input')

        # Build a dictionary with the ids and values from the input tags
        params = {input_tag.get(attribute): input_tag.get('value') for input_tag in inputs}

        if isinstance(query_model,str):
            additional_params = self.convert_query_url_to_dict(query_model)
            #self.show_kwargs_possible_values(html, query_model)

        elif isinstance(query_model,dict):
            additional_params = query_model
            #self.show_kwargs_possible_values(html, self.convert_dict_to_query_url(query_model))

        for key in additional_params:
            try:
                additional_params[key] = params[key]
            except KeyError:
                pass
        for key in kwargs:
            additional_params[key] = kwargs[key]

        # Use urlencode to create the query string
        if 'urlencode' in kwargs and not kwargs['urlencode']:
            return additional_params

        return urlencode(additional_params)

    def scrap_tags_from_xml(self, html, tag_inicio, tag_final):
        """
        Scrap tags from XML content in the HTML.

        :param html: The HTML content.
        :type html: str
        :param tag_inicio: The starting tag to search for.
        :type tag_inicio: str
        :param tag_final: The ending tag to search for.
        :type tag_final: str
        :return: The list of found tags.
        :rtype: list
        """
        content = html
        tag_inicio_xml = '<xml'
        tag_final_xml = '</xml>'
        idx_inicio = content.find(tag_inicio_xml)
        idx_final = content.find(tag_final_xml) + len(tag_final_xml)
        xml_user = content[idx_inicio:idx_final]

        # Find number of rows
        rows = xml_user.split('<r>')

        founds = []
        for row in rows:
            idx_inicio = row.find(tag_inicio)
            idx_final = row.find(tag_final)

            if -1 not in (idx_inicio, idx_final):
                found = row[idx_inicio + 4:idx_final]
                founds.append(found)
        return founds

    @time_out()
    def click_id_el(self, id):

        script = f"""
        return document.getElementById('{id}').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def get_el_by_id(self, id):
        script = f"""
        return document.getElementById('{id}')
        """
        return self.driver.execute_script(script)

    @time_out()
    def get_els_by_tag(self, tag):
        script = f"""
        return document.getElementsByTagName('{tag}')
        """
        return self.driver.execute_script(script)

    @time_out()
    def get_el_by_xpath(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

    def quit(self):
        self.driver.quit()
