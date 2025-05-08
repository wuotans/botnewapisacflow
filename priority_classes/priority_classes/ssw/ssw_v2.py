import html
import json
import logging
import shutil
import sys
import time
import zipfile
import customtkinter
import requests
import string
import os
import platform
from cryptography.fernet import Fernet
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urlencode, unquote
import pandas as pd
import priority_classes.globals.globals as gb
import asyncio
from threading import Thread
import threading as td
from priority_classes.decorators.decorators import time_out
from selenium.webdriver.firefox.options import Options as FirefoxOptions


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))


class EmptyValue(Exception):
    pass


class SswInterface:
    """
    A class that provides an interface for entering and storing encrypted credentials.

    :Example:

        >>> ssw_interface = SswInterface()
        >>> ssw_interface.ask_credentials()
        >>> credentials = ssw_interface.load_credentials()

    """

    def __init__(self):
        """
        Constructor method.
        Initializes the SswInterface object with several tkinter widgets and an instance of the SswCript class.
        """
        super().__init__()

        # configurando to titulo do app e a geometria dinamica
        # gb.init_root().title("SSW")
        # gb.init_root().geometry("+100+100")

        self.entry_login = None
        self.label_login = None
        self.button_login = None
        self.credentials = None
        self.messagebox_window = None
        self.label_image = None
        self.label_messabox = None
        self.button_messagebox = None

        self.path_credentials = os.path.abspath(os.path.join(os.getcwd(), 'parameters/ssw_credentials.bot'))

        self.cript = SswCript()

    @staticmethod
    def init_root():
        global ROOT
        try:
            customtkinter.CTkFrame(ROOT)
        except Exception as e:
            ROOT = customtkinter.CTk()
            return ROOT
        else:
            return ROOT

    def _create_folder(self, path):
        """
        Creates a folder at the specified path if it does not already exist.

        :param path: Path to the folder to be created.
        :type path: str
        :return: Absolute path to the folder.
        :rtype: str
        """
        if ':' not in path:
            root_path = os.getcwd()
            path = os.path.abspath(root_path + f'/{path}')

        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def ask_credentials(self):
        """
        Presents an interface for entering credentials.

        :return: None
        """
        # criando a interface the inserção das credenciais

        self.credentials_window = customtkinter.CTkToplevel(gb.init_root())
        self.credentials_window.title("SSW")
        self.credentials_window.attributes("-topmost", True)
        self.credentials_window.geometry("+100+100")

        self.entry_frame = customtkinter.CTkFrame(self.credentials_window)
        self.entry_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        image = self._load_image(os.path.join(PARENT_DIR, 'assets/ssw_logo.png'), 30, 30)
        self.label_login = customtkinter.CTkLabel(self.entry_frame, text="Insira suas credenciais!",
                                                  font=customtkinter.CTkFont(size=18, weight="bold"),
                                                  image=image,
                                                  compound='left'
                                                  )
        self.label_login.grid(row=1, column=0, padx=(20, 20), pady=(20, 10))

        self.entry_login = [customtkinter.CTkEntry(self.entry_frame) for _ in range(5)]
        self.entry_login[0] = customtkinter.CTkEntry(self.entry_frame, placeholder_text="Dominio", width=70)
        self.entry_login[0].grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.entry_login[1] = customtkinter.CTkEntry(self.entry_frame, placeholder_text="CPF")
        self.entry_login[1].grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.entry_login[2] = customtkinter.CTkEntry(self.entry_frame, placeholder_text="Usuario")
        self.entry_login[2].grid(row=4, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.entry_login[3] = customtkinter.CTkEntry(self.entry_frame, placeholder_text="Senha", show="*")
        self.entry_login[3].grid(row=5, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.entry_login[4] = customtkinter.CTkEntry(self.entry_frame, placeholder_text="Unidade")
        self.entry_login[4].grid(row=6, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.button_login = customtkinter.CTkButton(self.entry_frame, text='Avançar', command=self._button_login_event)
        self.button_login.grid(row=7, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        try:
            self.credentials_window.mainloop()
        except RuntimeError as e:
            logging.exception(e)

    def set_persistent_env_var(self, var_name, var_value):
        import subprocess
        system = platform.system()

        if system == 'Windows':
            # Set an environment variable persistently on Windows
            subprocess.run(['setx', var_name, var_value], check=True)
        elif system == 'Linux':
            # Set an environment variable persistently on Linux
            # Writing to .bashrc for the user
            home = os.path.expanduser('~')
            bashrc_path = os.path.abspath(os.path.join(home, '.bashrc'))
            with open(bashrc_path, 'a') as bashrc:
                bashrc.write(f'\nexport {var_name}="{var_value}"\n')
            logging.info(f"Variable added to {bashrc_path}. Please re-login or source the file.")
        else:
            raise NotImplementedError(f"Setting environment variables persistently is not implemented for {system}")

    def ask_credentials_cli(self, prefix_env):
        import getpass
        list_params = [
            'DOMINIO',
            'CPF',
            'USUARIO',
            'SENHA',
            'UNIDADE'
        ]
        values = []
        for param in list_params:
            if 'senha' in param.lower() or 'password' in param.lower():
                value = getpass.getpass(f'Informe a Senha para ({prefix_env}): ')
            else:
                value = input(f'Informe o(a) {param} para ({prefix_env}): ')
            self.set_persistent_env_var(f'{prefix_env}_{param}'.upper(), value)
            values.append(value)
        self.credentials = values

    def _button_login_event(self):
        """
        Encrypts the entered credentials and stores them if they are valid.

        :return: None
        """
        self.credentials = [self.cript.cripto_data(str(entry.get())) if len(entry.get()) > 0 else None for entry in
                            self.entry_login]
        if None in self.credentials:
            self.messagebox('Insira sua credenciais\n corretamente!')
        else:
            self._store_credentials()

        self.hide_window()
        self.quit()

    def _store_credentials(self):
        """
        Stores the encrypted credentials in a file.

        :return: None
        """
        self._create_folder('parameters')
        self.credentials = ' ;'.join(self.credentials)
        with open(self.path_credentials, 'w') as file:
            file.write(self.credentials)

    def messagebox(self, message, type_alert: str = 'warning'):
        """
        Presents a messagebox with a given message and alert type.

        :param message: Message to be displayed.
        :type message: str
        :param type_alert: Alert type (either 'warning' or 'info').
        :type type_alert: str
        :return: None
        """
        self.messagebox_window = customtkinter.CTkToplevel(gb.init_root())
        self.messagebox_window.title(type_alert.upper())
        self.messagebox_window.attributes("-topmost", True)

        self.messagebox_window.geometry("300x300+170+170")
        self.messagebox_window.rowconfigure(1, weight=1)
        self.messagebox_window.columnconfigure(0, weight=1)

        image = self._load_image(os.path.join(PARENT_DIR, 'assets/warning.png')) if type_alert == 'warning' \
            else self._load_image(os.path.join(PARENT_DIR, 'assets/info.png'))
        self.label_image = customtkinter.CTkLabel(self.messagebox_window,
                                                  text='',
                                                  image=image,
                                                  compound='left')
        self.label_image.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        self.label_messabox = customtkinter.CTkLabel(self.messagebox_window, text=message,
                                                     font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_messabox.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="nsew")

        self.button_messagebox = customtkinter.CTkButton(self.messagebox_window, text='Ok',
                                                         command=self.messagebox_window.destroy)
        self.button_messagebox.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        try:
            self.messagebox_window.mainloop()
        except RuntimeError as e:
            logging.exception(e)

    def _load_image(self, path_image, width: int = 50, height: int = 50):
        """
        Loads an image from a specified path and resizes it to a specified width and height.

        :param path_image: Path to the image file.
        :type path_image: str
        :param width: Width to resize the image to.
        :type width: int
        :param height: Height to resize the image to.
        :type height: int
        :return: Resized image.
        :rtype: customtkinter.CTkImage
        """
        # load and create background image
        path = os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), path_image))
        img = Image.open(path).copy()
        return customtkinter.CTkImage(Image.open(path), size=(width, height))

    def load_credentials(self):
        """
        Loads the encrypted credentials from a file and decrypts them.

        :return: Decrypted credentials.
        :rtype: list of str
        """
        if os.path.exists(self.path_credentials):
            with open(self.path_credentials, 'r') as file:
                self.credentials = file.read().split(';')
            for i, param in enumerate(self.credentials):
                self.credentials[i] = self.cript.decripto_data(param)
            return self.credentials
        else:
            return None

    def hide_window(self):
        """
        Hides the main tkinter window.

        :return: None
        """
        gb.init_root().withdraw()

    def show_window(self):
        """
        Shows the main tkinter window.

        :return: None
        """
        gb.init_root().iconify()

    def quit(self):
        gb.init_root().quit()
        gb.init_root().destroy()

    def loop(self):
        """
        Starts the tkinter event loop.

        :return: None
        """
        try:
            gb.init_root().mainloop()
        except RuntimeError as e:
            logging.exception(e)


class SswCript:
    """
    A class used for the encryption and decryption of data, which uses Fernet symmetric encryption.

    :Example:

        >>> ssw_cript = SswCript()
        >>> encrypted_data = ssw_cript.cripto_data("some sensitive data")
        >>> original_data = ssw_cript.decripto_data(encrypted_data)

    """

    def __init__(self):
        """
        Constructor method.
        Initializes the SswCript object with None as the key.
        """
        self.key = None

    @staticmethod
    def create_folder(path):
        """
        Creates a folder at the specified path.

        :param path: Path to the folder to be created.
        :type path: str
        :return: Absolute path to the folder.
        :rtype: str
        """
        if ':' not in path:
            root_path = os.getcwd()
            path = os.path.abspath(root_path + f'/{path}')

        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @staticmethod
    def create_path_to_save():
        """
        Creates a path for storing the key file.

        :return: Path to the key file.
        :rtype: str
        """
        system = platform.system()

        if system == 'Windows':
            # Path for AppData in Windows
            current_user = os.path.dirname(os.getenv('APPDATA'))
            path_store_key = os.path.abspath(current_user + '/Local/cvl')
        elif system == 'Linux':
            home_dir = os.path.expanduser('~')  # Gets the home directory
            path_store_key = os.path.join(home_dir, '.cvl')  # Creates a path within the home directory
            os.makedirs(path_store_key, exist_ok=True)
        else:
            logging.error(f"Unsupported operating system: {system}")
            return
        os.makedirs(path_store_key, exist_ok=True)
        logging.info(path_store_key)
        return path_store_key

    def generate_secret_key(self):
        """
        Generates a Fernet key and saves it into a file.

        :return: None
        """
        key = Fernet.generate_key()
        path_store_key = os.path.abspath(self.create_path_to_save())
        if not os.path.exists(f"{path_store_key}/h.b"):
            with open(f"{path_store_key}/h.b", "wb") as key_file:
                key_file.write(key)

    def load_key(self):
        """
        Loads the Fernet key from a file.

        :return: None
        """
        path_store_key = os.path.abspath(self.create_path_to_save())
        with open(f"{path_store_key}/h.b", "rb") as key_file:
            self.key = key_file.read()

    def salting(self, dados):
        """
        Salts the input data by interspersing it with ASCII characters.

        :param dados: Data to be salted.
        :type dados: str
        :return: Salted data.
        :rtype: str
        """
        salted = ''
        salt = string.ascii_uppercase + string.ascii_lowercase
        for i, c in enumerate(dados[::-1]):
            index = salt.find(c)
            salted += c + salt[i] if index == -1 else salt[index - 7] + salt[i]
        return salted

    def d_salt(self, salted):
        """
        Removes the salt from the input data.

        :param salted: Salted data.
        :type salted: str
        :return: Original unsalted data.
        :rtype: str
        """
        original_dados = ''
        salt = string.ascii_uppercase + string.ascii_lowercase
        for i, c in enumerate(salted[::-1]):
            index = salt.find(c)
            index_char_alt_range = salt[-7:].find(c)
            d_salted = salt[index + 7] if index_char_alt_range == -1 else salt[index_char_alt_range]
            if i % 2 != 0:
                original_dados += c if index == -1 else d_salted
        return original_dados

    def cripto_data(self, dados):
        """
        Encrypts and salts the input data.

        :param dados: Data to be encrypted.
        :type dados: str
        :return: Encrypted data.
        :rtype: str
        """
        self.generate_secret_key()
        if self.key is None:
            self.load_key()

        salted = self.salting(dados)
        salted = salted.encode()
        cipher_suite = Fernet(self.key)
        cipher_text = cipher_suite.encrypt(salted)
        dado_text = str(cipher_text.decode())
        return dado_text

    def decripto_data(self, dado_text):
        """
        Decrypts the input data and removes the salt.

        :param dado_text: Data to be decrypted.
        :type dado_text: str
        :return: Decrypted data.
        :rtype: str
        """
        if self.key is None:
            self.load_key()
        cipher_suite = Fernet(self.key)
        plain_text = cipher_suite.decrypt(dado_text.encode())
        salted = str(plain_text.decode())
        original_dado = self.d_salt(salted)
        return original_dado


class InvalidLogin(Exception):
    pass


class TryAgain(Exception):
    pass


class SswRequest:
    _instances = {}
    #_is_initialized = False

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SswRequest, cls).__new__(cls)
        return cls._instances[cls]

    def __init__(self, domain: str = None, cpf: int = None, user: str = None, password: str = None, unit: str = None,
                 env: bool = True, prefix_env: str = 'SSW', *args, **kwargs):
        """
        Initializes the SswRequest class. Sets up the necessary properties and user interface.
        """
        if not hasattr(self, '_is_initialized') or not self._is_initialized:
            self.page_count = 0
            self.ui = SswInterface()
            self.event_loop = None
            self.credentials = None
            self.driver = None
            self.method = None
            self.action = None
            self.cookies = None
            self.last_opssw = None
            self.prefix_env = prefix_env
            self.thread_event = td.Event()
            self.thread_refresh = None
            self.path_to_downloads = 'downloads'
            self.link = "https://sistema.ssw.inf.br/bin/ssw0422"
            self.session = requests.Session()
            self.headers = {
                "accept": "*/*",
                "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded",
                "pragma": "no-cache",
                "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin"
            }
            os.makedirs('config', exist_ok=True)
            value = self._create_file_txt(f'env:{env}', 'config_env_credentials', 'config')
            self.env = True if 'true' in value.lower() else False

            self._load_credentials(domain, cpf, user, password, unit)
            self.refresh_browser_and_login_each_time(*args, **kwargs)
            self._is_initialized = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.quit()
        return False

    def refresh_browser_and_login_each_time(self, time_to_refresh: int = 300, *args, **kwargs):
        def refresh(name_instance):
            counter = 0
            qtde_error = 0
            while not self.thread_event.is_set():
                time.sleep(1)
                try:
                    if counter > time_to_refresh:
                        logging.info('#' * 20, f'SSW refreshing {name_instance}', '#' * 20)
                        try:
                            self.init_browser(*args, **kwargs)
                            self.login()
                        except Exception as e:
                            logging.info('Erro.......')
                            logging.exception(e)
                        counter = 0
                    counter += 1
                except KeyboardInterrupt:
                    self.quit()
                except Exception as e:
                    qtde_error += 1
                    logging.exception(e)
                    time.sleep(qtde_error * 10)
                if qtde_error > 60:
                    break
            self.driver.quit()

        name_instance = kwargs.pop("name_instance") if 'name_instance' in kwargs else 'ssw'
        self.init_browser(*args, **kwargs)
        self.login()
        self.thread_refresh = Thread(target=lambda : refresh(name_instance))
        self.thread_refresh.start()

    def _load_credentials(self, domain, cpf, user, password, unit):
        """
        Loads the user's credentials from the interface or asks for them if they haven't been set yet.
        """
        if None in (domain, cpf, user, password, unit):
            if self.env:
                logging.info('Getting environ...')
                domain = os.getenv(f'{self.prefix_env}_DOMINIO')
                cpf = os.getenv(f'{self.prefix_env}_CPF')
                user = os.getenv(f'{self.prefix_env}_USUARIO')
                password = os.getenv(f'{self.prefix_env}_SENHA')
                unit = os.getenv(f'{self.prefix_env}_UNIDADE')
                self.credentials = [domain, cpf, user, password, unit]
                if None in self.credentials:
                    self.ui.ask_credentials_cli(self.prefix_env)
            else:
                self.credentials = self.ui.load_credentials()
                if self.credentials is None:
                    self.ui.ask_credentials()
                    self.credentials = self.ui.load_credentials()
        else:
            self.credentials = [domain, cpf, user, password, unit]

    def _create_folder(self, path):
        """
        Creates a folder at a given path if it does not exist already.

        :param path: The path where the folder should be created
        :type path: str
        :return: The absolute path of the created folder
        :rtype: str
        """

        path = os.path.abspath(path)
        os.makedirs(path, exist_ok=True)
        return path

    def _create_file_txt(self, text: str = '', name_file: str = '', path_to_save: str = '', subs: bool = False):
        """
        Creates a .txt file at a specified location with provided text. If the file already exists,
        the method can either overwrite it or read its content based on the 'subs' argument.
        The method first ensures that the path to save the file exists, creating it if it doesn't.

        :param text: The text to write into the file. Default is an empty string.
        :type text: str

        :param name_file: The name of the file to be created. Default is an empty string.
        :type name_file: str

        :param path_to_save: The directory where the file should be saved. Default is the current working directory.
        :type path_to_save: str

        :param subs: If True, existing file will be overwritten. If False and file exists, its content will be read. Default is False.
        :type subs: bool

        :return: The text written to the file or read from it.
        :rtype: str

        :Example:

            self._create_file_txt("Hello, world!", "test", "/path/to/save", True) # creates/overwrites a file named "test.txt" with the text "Hello, world!" at "/path/to/save"

        """
        path_to_save = self._create_folder(path_to_save)
        full_path_file = os.path.abspath(f'{path_to_save}/{name_file}.txt')

        if not os.path.exists(full_path_file) or subs:
            with open(full_path_file, 'w') as f:
                f.write(text)
        else:
            with open(full_path_file, 'r') as f:
                text = f.read()
        return text

    @staticmethod
    def _read_file_txt(full_path_file):
        with open(os.path.abspath(full_path_file), 'r') as f:
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

    def wait_download(self, timeout: int = 3600, ext_optional: str = '.txt'):
        # tuple of commom extentions in the project to download
        use_to_ext = ('.xls', '.csv', '.sswweb', '.json', '.pdf', ext_optional)

        # loop over path download until file be found
        contador_while = 0
        while contador_while < timeout:

            # getting the files extentions
            ext_files_list = [str(file_name).split('.')[-1].lower() for file_name in os.listdir(self.path_to_downloads)]
            found = [True for ext in ext_files_list if ext in use_to_ext]
            if True in found:
                break
            contador_while += 1
            time.sleep(1)

    def define_profile_path(self, name_instance, subs: bool = True):
        system = platform.system()
        path_store_profile = 'bot_profile_chrome' if system == 'Linux' else os.path.dirname(
            os.getenv('APPDATA')) + '/profile_chrome'
        path_store_profile = os.path.abspath(os.path.join(path_store_profile, name_instance))
        if not os.path.exists(path_store_profile):
            os.makedirs(path_store_profile, exist_ok=True)

        profile_path = self._create_file_txt(path_store_profile, 'profile_path_browser', 'parameters', subs)
        return profile_path

    def init_browser(self, profile_path: str = 'profile_browser', ignore_profile: bool = True, path_to_downloads='downloads',
                     headless: bool = True, driver: str = 'edge',**kwargs):
        """
        Initializes the web browser.

        :param driver:
        :param headless:
        :param name_instance: Name of the browser instance, defaults to 'Default'
        :type name_instance: str, optional
        :param ignore_profile: Whether to ignore the profile, defaults to True
        :type ignore_profile: bool, optional
        :param path_to_downloads: Path to the downloads folder, defaults to 'downloads'
        :type path_to_downloads: str, optional
        """
        self.path_to_downloads = self._create_folder(path_to_downloads)

        profile_path = self._create_folder(profile_path)

        driver = self._create_file_txt(driver, 'config_driver_browser', 'config', True)
        if driver == 'chrome':
            self.chrome_driver(self.path_to_downloads, profile_path, ignore_profile, headless,**kwargs)
            self.action = ActionChains(self.driver)
        elif driver == 'edge':
            self.edge_driver(self.path_to_downloads, profile_path, ignore_profile, headless,**kwargs)
            self.action = ActionChains(self.driver)
        elif driver in ['firefox', 'mozilla']:
            self.firefox_driver(self.path_to_downloads, profile_path, ignore_profile, headless,**kwargs)
            self.action = ActionChains(self.driver)

    def chrome_driver(self, path_to_downloads, profile_path, ignore_profile, headless,**kwargs):
        logging.info('...Chromedriver Option...')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")

        options.add_experimental_option("prefs", {
            "download.default_directory": path_to_downloads,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
            "download.extensions_to_open": "applications/pdf",
            'plugins.always_open_pdf_externally': True
        })
        # Trying to use ChromeDriverManager to get the latest driver
        # path_chrome_driver = self.chromedriver_install()

        if len(profile_path) > 0 and not ignore_profile:
            options.add_argument(f"user-data-dir={profile_path}")

        if headless:
            options.add_argument('headless')

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
        self.driver = webdriver.Chrome(options=options)  # executable_path=path_chrome_driver,


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
        logging.info(f'path_to_downloads: {path_to_downloads}')
        options.set_preference("browser.download.dir", path_to_downloads)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # Ajuste conforme necessário
        options.set_preference("pdfjs.disabled", True)  # Desativa visualizador PDF interno do Firefox
        options.set_preference("browser.download.useDownloadDir", True)
        options.set_preference("browser.download.panel.shown", False)
        self.driver = webdriver.Firefox(options=options)
        #self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)


    def edge_driver(self, path_to_downloads, profile_path, ignore_profile, headless,**kwargs):
        logging.info('...Edgedriver Option...')
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        if len(profile_path) > 0 and not ignore_profile:
            logging.info(profile_path)
            options.add_argument(f"--user-data-dir={profile_path}")

        if headless:
            options.add_argument('--headless')

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
        options.add_experimental_option("prefs", {"download.default_directory": f"{path_to_downloads}"})
        self.driver = webdriver.Edge(options=options)

    @time_out()
    def _send_credential_to_input_id(self, i):
        """
        Executes JavaScript code to identify an input element on a web page by its ID
        and then sends the corresponding credential (based on the index `i`) to that input field.
        The execution of this function is managed by the `time_out` decorator to prevent hanging in case of failure.

        :param i: Index corresponding to the credential to be sent. This also corresponds to the ID of the HTML input element.
        :type i: int

        :Example:

            self._send_credential_to_input_id(1)  # sends the first credential to the input field with ID '1'

        :raises: TimeoutException if unable to execute the script or send the credential after the specified timeout period.
        """
        script = f"""
        var input = document.getElementById('{i}').value = '{self.credentials[i - 1]}'
        return input
        """
        self.driver.execute_script(script)

    def _enter_credentials(self):
        """
        Sends user credentials to their respective input fields on the SSW login page.
        """
        for i in range(1, 5):
            self._send_credential_to_input_id(i)

    @time_out(time_out=2)
    def _click_submit(self):
        """
        Executes JavaScript code to click the submit button (identified by the ID '5') on a web page.
        The execution of this function is managed by the `time_out` decorator to prevent hanging in case of failure.

        :Example:

            self._click_submit()

        :raises: TimeoutException if unable to execute the script after the specified timeout period.
        """
        script = """
        document.getElementById('5').click()
        """
        self.driver.execute_script(script)

    @time_out()
    def _get_cookies(self):
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
        logging.info('#'*20,'Session Cookies','#'*20)
        logging.info(self.session.cookies)

    @time_out(3, raise_exception=False)
    def close_child_windows(self):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if handle != self.home_page:
                self.driver.close()
        self.driver.switch_to.window(self.home_page)

    @time_out(time_out=10)
    def next_window(self, idx):
        self.driver.switch_to.window(self.driver.window_handles[idx])

    @time_out(10)
    def wait_main_page(self):
        page = self.driver.current_url
        if not page == 'https://sistema.ssw.inf.br/bin/menu01':
            raise TryAgain

    @time_out(time_out=2, raise_exception=False)
    def _verify_warning(self, id):
        script = f"""
        var error = document.getElementById('errormsglabel')
        if (error){{
            var innerText = error.innerText
            document.getElementById('{id}').click()
            return innerText
        }}
        """
        return self.driver.execute_script(script)

    def _login_selenium(self):
        # open the ssw link
        self.driver.get(self.link)
        #logging.info(self.driver.page_source)

        # get credentials access
        # self._load_credentials()

        # put the credentials
        self._enter_credentials()

        # submit login
        self._click_submit()

        # verify possible warning
        time.sleep(3)
        result = self._verify_warning(0)
        logging.info(result)
        if result is not None:
            # os.remove(self.ui.path_credentials)
            raise InvalidLogin

        # wait main page
        self.wait_main_page()

        # load cookies to enable requests
        self._get_cookies()

        self.home_page = self.driver.current_window_handle
        logging.info(self.driver.current_url)

    @time_out(2,delay=5)
    def login(self):
        """
        Performs the login process to the SSW system by opening the SSW link,
        loading credentials, entering them, submitting the login form, and obtaining cookies for future requests.
        """
        self._login_selenium()
        # verify login
        self.verify_login()

    @time_out(2)
    def verify_login(self, *args, **kwargs):
        """
        Perform the model operation.

        :return: None
        """
        self.last_opssw = '101'

        # first query post
        data = f"act=TRO&f2={self.credentials[4]}&f3={self.last_opssw}&dummy=1686835505969"

        response = self.session.post("https://sistema.ssw.inf.br/bin/menu01", headers=self.headers, data=data)

        logging.info(response.status_code)
        logging.info(response.text)
        if 'Filial n&atilde;o encontrada.' in response.text:
            # os.remove(self.ui.path_credentials)
            raise InvalidLogin

    @staticmethod
    def convert_query_url_to_dict(query, empty_values: bool = True, fill_empty_values_by: str = ''):
        """
        Converts a query URL into a dictionary.

        :param query: The query URL to convert
        :type query: str
        :param empty_values: Whether to empty the values, defaults to True
        :type empty_values: bool, optional
        :param fill_empty_values_by: empty values will be replace by this value
        :type fill_empty_values_by: str, optional
        :return: The dictionary obtained from the query URL
        :rtype: dict
        """
        dict_query = {}
        query_list = query.split('&')
        for param in query_list:
            param_list = param.split('=')
            if not empty_values:
                dict_query[param_list[0]] = param_list[1]
            elif fill_empty_values_by != '':
                if str(param_list[1]).strip() == '':
                    dict_query[param_list[0]] = fill_empty_values_by
            else:
                dict_query[param_list[0]] = ''
        return dict_query

    @staticmethod
    def convert_dict_to_query_url(dict_query, show_values: bool = False):
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
            if show_values:
                logging.info(f'{key}={dict_query[key]}')
        return '&'.join(query_format)

    def pretty_show_query(self, query):
        query = self.convert_query_url_to_dict(query, False)
        logging.info(json.dumps(query, indent=6))

    def show_kwargs_possible_values(self, html, query_model,**kwargs):
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
        verbose = kwargs.get('verbose', True)
        if verbose:
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
                        if div_tag is not None:
                            # Extract the query parameter name and value
                            param_name = input_tag['name']
                            param_value = div_tag.text.strip().replace('&nbsp;', '').replace(' ', '')

                            # Build the query string
                            query = f'        - {param_name}: {param_value}'

                            logging.info(query)
                except KeyError:
                    pass
                except AttributeError:
                    pass
            logging.info('    :type kwargs: dict')
            logging.info('    :return: None')
            logging.info('"""')

    def _get_value(self, element, att):
        if att == 'value':
            return element.get('value')
        elif att == 'text':
            return element.text

    def get_input_values_from_html(self, html, attribute: str = 'id', **kwargs) -> dict:
        soup = BeautifulSoup(html, 'html.parser')

        # Find all input tags in the HTML
        inputs = soup.find_all('input')

        value = 'value' if 'value' not in kwargs else kwargs.pop('value')

        # Build a dictionary with the ids and values from the input tags
        params = {input_tag.get(attribute): self._get_value(input_tag, value) for input_tag in
                  inputs}  # input_tag.get('value')
        return params

    def get_all_type_input_values(self):
        script = """
         //parameters = parameters + "?act=" + valor;
         g_ctrc_ser_ctrc
          var inputsLength = document.getElementsByTagName("TEXTAREA").length;
          for (i=0; i<inputsLength; i++){
           if (document.getElementsByTagName("TEXTAREA")[i].value != "")
           {
            var til = document.getElementsByTagName("TEXTAREA")[i].value;
             parameters = parameters + "&" + document.getElementsByTagName("TEXTAREA")[i].name
                        + "=" + escape(til);
           }
          }
          var inputsLength = document.getElementsByTagName("INPUT").length;
          for (i=0; i<inputsLength; i++){
           if (document.getElementsByTagName("INPUT")[i].type.toUpperCase() == "TEXT")
           {
            if (document.getElementsByTagName("INPUT")[i].value != "")
            {
             if (document.getElementsByTagName("INPUT")[i].name.toUpperCase() != "SR_ACC")
             {
              var ovalue = document.getElementsByTagName("INPUT")[i].value;
              parameters = parameters + "&" + document.getElementsByTagName("INPUT")[i].name
                        + "=" + escape(ovalue).replace(/\+/g, '%2B');
             }
            }
           }
           if (document.getElementsByTagName("INPUT")[i].type.toUpperCase() == "PASSWORD")
           {
            if (document.getElementsByTagName("INPUT")[i].value != "")
            {
             parameters = parameters + "&" + document.getElementsByTagName("INPUT")[i].name
                       + "=" + escape(document.getElementsByTagName("INPUT")[i].value);
            }
           }
        
           if (document.getElementsByTagName("INPUT")[i].type.toUpperCase() == "CHECKBOX") {
            if (document.getElementsByTagName("INPUT")[i].checked) {
             parameters = parameters + "&" + document.getElementsByTagName("INPUT")[i].name + "=TRUE";
            }
           }
        
           if (document.getElementsByTagName("INPUT")[i].type.toUpperCase() == "HIDDEN")
           {// so insere o act que estava como hidden se o atual for vazio
            if ((document.getElementsByTagName("INPUT")[i].name != "act") ||
               ((document.getElementsByTagName("INPUT")[i].name == "act") &&
                (document.getElementsByTagName("INPUT")[i].value != "") && 
                (valor == "")))
            {
             var ovalue = document.getElementsByTagName("INPUT")[i].value;
             parameters = parameters + "&" + document.getElementsByTagName("INPUT")[i].name
                        + "=" + ovalue;
            }
           }
           if ((document.getElementsByTagName("INPUT")[i].type.toUpperCase() == "FILE") && (document.getElementsByTagName("INPUT")[i].id != "uploadBtn"))
           {
            bupload = true;
            var fileid = i;
            var ovalue = document.getElementsByTagName("INPUT")[i].value;
            parameters = parameters + "&" + document.getElementsByTagName("INPUT")[i].name
                       + "=" + escape(ovalue);
           }
          }
          
          parameters = parameters + "&dummy=" + new Date().getTime();
        console.log(parameters)
        return parameters
        """
        return self.driver.execute_script(script)

    def update_query_values(self, html, query_model, attribute: str = 'id', **kwargs):
        """
        Update the values in the query string of the query model.

        :param html: The HTML content of the page.
        :type html: str
        :param query_model: The query model string.
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

        value = 'value' if 'value' not in kwargs else kwargs.pop('value')

        # Build a dictionary with the ids and values from the input tags
        params = {input_tag.get(attribute): self._get_value(input_tag, value) for input_tag in
                  inputs}  # input_tag.get('value')

        self.show_kwargs_possible_values(html, query_model,**kwargs)

        unquote_ = kwargs.pop('unquote') if 'unquote' in kwargs else False

        additional_params = self.convert_query_url_to_dict(query_model)
        for key in additional_params:
            try:
                additional_params[key] = params[key]
            except KeyError:
                pass
        for key in kwargs:
            if unquote_:
                additional_params[key] = unquote(str(kwargs[key]))
            else:
                additional_params[key] = kwargs[key]

        # Use urlencode to create the query string
        query = urlencode(additional_params)

        return query

    @staticmethod
    def scrap_tags_from_xml(html, tag_inicio, tag_final):
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
            else:
                found = float('nan')
            founds.append(found)
        return founds

    @staticmethod
    def get_dummy():
        # Get the current time in seconds since the epoch
        timestamp = time.time()

        # Convert the timestamp to milliseconds
        dummy = int(timestamp * 1000)

        logging.info(dummy)
        return dummy

    def get_table(self, html_content, range_):
        import html
        html_content = html.unescape(html_content)
        tags_inicio = [f'<f{i}>' for i in range(range_)]
        tags_fim = [f'</f{i}>' for i in range(range_)]
        fila = {}
        for tag_inicio, tag_fim in zip(tags_inicio, tags_fim):
            fila[tag_inicio] = self.scrap_tags_from_xml(html_content, tag_inicio, tag_fim)
        df = pd.DataFrame(fila).dropna(how='all', ignore_index=True)
        return df

    def get_screenshot(self, path_filename):
        self.driver.save_screenshot(path_filename)
        return path_filename
    def filter_df_by_values(self, df, filter_dict):
        # Filter the DataFrame based on a dictionary with possible partial matches
        query_str = ' & '.join(
            f"`{col}`.str.contains('{val}', case=False, na=False)" for col, val in filter_dict.items() if
            col in df.columns)
        logging.info(query_str)
        df = df.query(query_str).reset_index(drop=True)
        return df

    @staticmethod
    def extract_html_values(html_text, keyword_ini, keyword_fin):
        """
        Extracts values from decoded text between the specified keywords.

        This function extracts values from the decoded text between the specified keywords.
        If the extraction encounters an IndexError, it will log the exception and return the error message as the extracted value.

        :param decoded_text: The decoded HTML text.
        :type decoded_text: str
        :param keyword_ini: The keyword marking the beginning of the value to extract.
        :type keyword_ini: str
        :param keyword_fin: The keyword marking the end of the value to extract.
        :type keyword_fin: str
        :return: The extracted value from the decoded text.
        :rtype: str
        """
        try:
            decoded_text = html.unescape(html_text)
            logging.info(decoded_text)
            decoded_text = decoded_text.replace('<b>', '').replace('</b>', '')
            index_ini = decoded_text.find(keyword_ini)
            index_fin = decoded_text.find(keyword_fin)
            extracted_val = decoded_text[index_ini + len(keyword_ini):index_fin]
        except IndexError as e:
            logging.exception(e)
            extracted_val = None
        return extracted_val

    def _get_user_table156(self, html):
        """
        Retrieves the user table from the 156 system.

        :param html: The HTML content.
        :type html: str
        :return: The user table.
        :rtype: pandas.DataFrame
        """
        tags_inicio = ['<f0>', '<f1>', '<f3>', '<f6>', '<f8>']
        tags_fim = ['</f0>', '</f1>', '</f3>', '</f6>', '</f8>']
        fila = {}
        for tag_inicio, tag_fim in zip(tags_inicio, tags_fim):
            fila[tag_inicio] = self.scrap_tags_from_xml(html, tag_inicio, tag_fim)

        # converting to Dataframe to better manipulation
        df_fila = pd.DataFrame(fila)

        # Filter by user
        df_fila_user = df_fila[df_fila['<f3>'] == self.credentials[2].lower()].reset_index(drop=True)

        # filter by option
        series_fila_op = pd.Series(df_fila_user['<f1>'].str.upper())
        df_fila_user_op = df_fila_user[series_fila_op.str.contains(self.last_opssw, na=False)].reset_index(
            drop=True)
        return df_fila_user_op

    def _get_sequence_id156(self, html):
        """
        Retrieves the sequence ID from the 156 system.

        :param html: The HTML content.
        :type html: str
        :return: The sequence ID.
        :rtype: str
        """
        df_fila_user_op = self._get_user_table156(html)

        # filter by status
        series_fila_status = pd.Series(df_fila_user_op['<f6>'].str.upper())
        df_fila_user_status = df_fila_user_op[series_fila_status.str.contains('AGUARDANDO', na=False)].reset_index(
            drop=True)

        # getting the sequence id
        sequence_id = str(df_fila_user_status.loc[0, '<f0>'])

        return sequence_id

    def _get_status_sequence_id156(self, html, sequence_id):
        """
        Gets the status of a sequence ID on the 156 system.

        :param html: The HTML content.
        :type html: str
        :param sequence_id: The sequence ID.
        :type sequence_id: str
        :return: The status of the sequence ID.
        :rtype: str
        """
        df_fila_user_op = self._get_user_table156(html)

        # filter by sequence
        index = df_fila_user_op['<f0>'].tolist().index(sequence_id)

        # getting status
        status = df_fila_user_op.loc[index, '<f6>'].lower()
        return status

    def _get_act_value_to_download_156(self, html, sequence_id):
        """
        Gets the 'act' value to download a file on the 156 system.

        :param html: The HTML content.
        :type html: str
        :param sequence_id: The sequence ID.
        :type sequence_id: str
        :return: The 'act' value to download the file.
        :rtype: str
        """
        df_fila_user_op = self._get_user_table156(html)

        # filter by sequence
        index = df_fila_user_op['<f0>'].tolist().index(sequence_id)

        # getting act
        act = df_fila_user_op.loc[index, '<f8>']

        act_to_download = act.split("'")[1]
        return act_to_download

    def _wait_file_to_be_completed_on_156(self):
        """
        Waits for the file to be completed on the 156 system.

        :return: The 'act' value to download the file.
        :rtype: str
        """
        html = self.op156()

        sequence_id = self._get_sequence_id156(html)
        logging.info(sequence_id)

        # wait until 'conclu' or 'abortado' status on 156
        out_status = ('conclu', 'abortado')
        while len([s for s in out_status if s in self._get_status_sequence_id156(html, sequence_id)]) == 0:
            html = self.op156()
            time.sleep(2)
        logging.info('Concluido!')
        html = self.op156()
        act_to_download = self._get_act_value_to_download_156(html, sequence_id)
        return act_to_download

    def build_url_to_download(self, html):
        """
        Builds the URL to download a file from the 156 system.

        :param html: The HTML content containing the required values.
        :type html: str
        :return: The URL to download the file.
        :rtype: str
        """
        # Parse the HTML input
        soup = BeautifulSoup(html, "html.parser")
        web_body_value = soup.find("input", id="web_body")["value"]

        # Extract the required values from the web_body value
        decoded_text = unquote(web_body_value)

        values = decoded_text.split("'")
        if len(values) < 5:
            values = decoded_text.split('"')
        act_value, filename_value, path_value = values[1], values[3], values[5]

        # Build the URL dynamically
        base_url = "https://sistema.ssw.inf.br/bin/ssw0424"
        query_params = {
            "act": act_value,
            "filename": filename_value,
            "path": path_value,
            "down": "1",
            "nw": "1"
        }
        url = base_url + "?" + self.convert_dict_to_query_url(query_params)

        logging.info(f"web_body_value: {decoded_text}")
        logging.info(f"URL: {url}") 
        return url, filename_value

    def download_from_156(self, name_file: str = None):
        """
        Downloads a file from the 156 system.

        :param name_file: The name of the file to be downloaded.
        :type name_file: str
        """
        act_to_download = self._wait_file_to_be_completed_on_156()

        # requestto get the filename to download
        data = f"act={act_to_download}&web_body=&dummy=1686931946874"
        logging.info(data)

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1440", headers=self.headers, data=data)

        # build the ssw url to download
        url, filename_value = self.build_url_to_download(response.text)

        name_file = name_file if name_file is not None else filename_value

        # get the content
        response = self.session.get(url)

        # write file
        filename = os.path.abspath(
            f"{self.path_to_downloads}/{name_file}")  # Specify the filename to save the downloaded file
        with open(filename, "wb") as file:
            file.write(response.content)

    def op156(self):
        """
        Performs an operation on the 156 system.

        :return: The response text.
        :rtype: str
        """
        data = "dummy=1686925010219"

        response = self.session.post("https://sistema.ssw.inf.br/bin/ssw1440", headers=self.headers, data=data)

        # showing results
        return response.text

    def request_download(self, url, name_file):
        # get the content
        response = self.session.get(url)
        # write file
        filename = os.path.abspath(
            f"{self.path_to_downloads}/{name_file}")  # Specify the filename to save the downloaded file
        with open(filename, "wb") as file:
            file.write(response.content)

    def direct_download(self, html, name_file: str = None):
        """
        Downloads a file from the ssw system directly.

        :param name_file: The name of the file to be downloaded.
        :type name_file: str
        """

        # build the ssw url to download
        url, filename_value = self.build_url_to_download(html)

        name_file = name_file if name_file is not None else filename_value
        name_file = name_file if '.' in name_file else name_file + '.' + filename_value.split('.')[-1]

        self.request_download(url, name_file)

    def handle_download(self, html, **kwargs):
        name_file = kwargs.pop('name_file') if 'name_file' in kwargs else None
        if 'enviada para processamento' in html and '156' in html:
            self.download_from_156(name_file)
        else:
            self.direct_download(html, name_file)

    def add_left_zero(self, value, len_desired):
        zeros = ''.join(['0' for i in range(len_desired - len(str(value)))])
        return zeros + str(value)

    @staticmethod
    def find_all_ocurrences(html, key_word):
        index_ini = 0
        index_ocurrences = []
        while index_ini != -1:
            index_ini = html.find(key_word, index_ini)
            if index_ini != -1:
                logging.info(f"Occurrence found at index: {index_ini}")
                index_ocurrences.append(index_ini)
                index_ini += len(key_word)
        return index_ocurrences

    def get_nfe_info_from_ssw(self, chave_nfe):
        url = f"https://sistema.ssw.inf.br/bin/ssw0024?act=ISSSW&chavenfe={chave_nfe}&stepImport=1&tp_docrestr=N&dummy={self.get_dummy()}"
        response = self.session.get(url, headers=self.headers)
        data = response.text
        data_json = json.loads(data.split('|')[1])
        return data_json

    def get_city_name_from_ssw_for_cep(self, cep):
        url = f"https://sistema.ssw.inf.br/bin/ssw0017?ajax=S&cep={cep}&id=44&dummy={self.get_dummy()}"
        response = self.session.get(url, headers=self.headers)
        data = response.text
        logging.info(data)
        data = data.split('<_3>')[1].split('</_3>')[0]
        return data

    def get_cep_from_ssw_for_city_name(self, city_name):
        import xmltodict
        url = f"https://sistema.ssw.inf.br/bin/ssw0385?key={city_name}&tipo=cidade&cep=1&dummy={self.get_dummy()}"
        response = self.session.get(url, headers=self.headers)
        data = response.text
        logging.info(data)
        data_dict = xmltodict.parse(data)
        logging.info(data_dict)
        return data_dict

    def get_current_html_text(self):
        return self.html_text

    def get_current_html_content(self):
        return self.html_content

    def save_html_content(self):
        with open('index.html', 'wb') as f:
            f.write(self.get_current_html_content())
        return self.get_current_html_content()

    def quit(self):
        self.driver.quit()
        self.thread_event.set()


if __name__ == '__main__':
    app = SswRequest()
    app.init_browser(headless=False)
    app.login()
    app.op019(relatorio_excel='s')
    app.quit()
