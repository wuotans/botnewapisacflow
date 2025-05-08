import logging
import os, sys
from datetime import datetime

# import graypy

import json

try:
    from rich import print

    logging.info("Usando rich para visualização de logs")
except:
    pass

# from src.main import var_test


class LogTipo:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class CustomLogger:
    """
    Logger responsável por registrar todos os "prints" em forma de log com níveis

    Parametros:
    path_init: caminho do diretório onde o arquivo .log sera gerado
    nome_log: nome do arqivo .log sem a extensão
    name_bot: nome do bot (nome da apsta onde serão inseridos os logs desse bot especifico)
    print_logs: define se os logs registrados serão printados em tela
    nivel_logger: define o nível de logs a serem registrados
        - O método setLevel do módulo logging em Python é utilizado para definir o nível mínimo de severidade das mensagens de log que serão capturadas pelo logger. Somente mensagens de log com um nível de severidade igual ou superior ao nível configurado serão processadas.
    """
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    def __init__(
        self,
        path_init: str = "",
        nome_log: str = "",
        name_bot: str = "",
        print_logs: bool = True,
        nivel_logger=logging.DEBUG,
        remove_datailed_web_logs: bool = True,
    ):
        self.path_init = path_init
        self.nome_log = nome_log
        self.name_bot = name_bot
        self.print_logs = print_logs
        self.nivel_logger = nivel_logger
        self.real_folder_logs = ""
        self.remove_datailed_web_logs = remove_datailed_web_logs

        self.logger = None
        self.init_logger()

    def define_path_local_logs(self):
        self.real_folder_logs = os.path.join(
            self.path_init, self.name_bot
        )
        if not os.path.exists(self.real_folder_logs):
            os.makedirs(self.real_folder_logs)

    def init_logger(self):
        self.define_path_local_logs()

        # se nao passar nenhum nome, cria um nome com base na hora atual
        if not self.nome_log:
            self.nome_log = self.string_hora()

        file_path = os.path.join(self.real_folder_logs, f"{self.string_data()}_{self.nome_log}.log")
        logging.info(file_path)

        logging.basicConfig(
            filename=file_path,
            format="%(asctime)s %(message)s",
            filemode="a",
        )

        logging.info(f"------------- INICIO   ->  {self.nome_log}")

        self.logger = logging.getLogger()  # Creating an object

        if self.remove_datailed_web_logs:
            # desabilita o registro de logs desnecessários
            logging.getLogger("selenium").setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)
            logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(
                logging.WARNING
            )

        self.logger.setLevel(
            self.nivel_logger
        )  # Setting the threshold of logger to DEBUG
        # self.logger.setLevel(logging.ERROR)  # Setting the threshold of logger to DEBUG

    def string_data(self):
        agora = datetime.now()
        return agora.strftime("%Y-%m-%d")

    def string_hora(self):
        agora = datetime.now()
        return agora.strftime("%H-%M-%S")

    def register_in_db():
        """Pode ser adicionado aos registros de log em reg() para também registrar no banco"""
        pass

    def reg(
        self,
        msg: str,
        type: LogTipo = LogTipo.DEBUG,
        reg_screenshot: bool = False,
        driver=None,
    ):
        """----------------------------------------------------------
        Printa na tela e salva no arquivo de log definido no init
        para registrar print é necessario passar o driver selenium
        """
        msg_reg = ""
        if type == LogTipo.DEBUG:
            msg_reg = f"[D] {str(msg)}"
            self.logger.debug(msg_reg)
        elif type == LogTipo.INFO:
            msg_reg = f"[I] {str(msg)}"
            self.logger.info(msg_reg)
        elif type == LogTipo.WARNING:
            msg_reg = f"[W] {str(msg)}"
            self.logger.warning(msg_reg)
        elif type == LogTipo.ERROR:
            msg_reg = f"[E] {str(msg)}"
            self.logger.error(msg_reg)
            if reg_screenshot:
                self.registra_screenshot(driver, tipo="[E]")
        elif type == LogTipo.CRITICAL:
            msg_reg = f"[C] {str(msg)}"
            self.logger.critical(msg_reg)
            if reg_screenshot:
                self.registra_screenshot(driver, tipo="[C]")
        else:
            msg_reg = "------------ [erro interno] tipo de log invalido"

        if self.print_logs == True:
            logging.info(msg_reg)
        return msg_reg

    def registra_screenshot(self, driver, tipo="[C]"):
        try:
            if driver:
                try:
                    print_nome = f"{self.string_hora()}__{self.string_data()}.png"
                    print_path = os.path.join(self.real_folder_logs, print_nome)
                    self.logger.debug(f"salvando screeshot em [{print_path}]")
                    driver.save_screenshot(print_path)
                except:
                    self.logger.critical(
                        f"Não poi possível registrar scheenshot do erro do tipo {tipo}"
                    )
        except Exception as e:
            # em caso de erro no registro de um log nao pode travar a applicação
            self.reg(f'Erro ao registrar screenshot. {e}', LogTipo.WARNING, reg_screenshot=False)
