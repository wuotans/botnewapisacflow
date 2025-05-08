import logging
import platform,re
import smtplib, ssl, os, imaplib
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import tkinter
import customtkinter
import string
from cryptography.fernet import Fernet
from PIL import Image
import time
from datetime import datetime
from  typing import Optional, Union

import priority_classes.globals.globals as gb
from priority_classes.decorators.decorators import time_out


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))


class Email:

    def __init__(self, env: bool = True, prefix_env="WEBMAIL"):
        self.ui = EmailInterface()
        self.env = env
        self.prefix_env = prefix_env
        self.smtp = "smtp.carvalima.com.br"
        self.imap_server = imaplib.IMAP4_SSL("imap.carvalima.com.br", port=993)
        self.credentials = None
        self.message = None
        self.all_mails_to_send = None
        self.mail_ids_imap = []
        self._load_credentials()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        return False


    @staticmethod
    def create_folder(path):

        if ":" not in path:
            root_path = os.getcwd()
            path = os.path.abspath(root_path + f"/{path}")

        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def create_file_txt(
        self,
        text: str = "",
        name_file: str = "",
        path_to_save: str = "",
        subs: bool = False,
    ):

        path_to_save = self.create_folder(path_to_save)
        full_path_file = os.path.abspath(f"{path_to_save}/{name_file}.txt")

        if not os.path.exists(full_path_file) or subs:
            with open(full_path_file, "w") as f:
                f.write(text)
        else:
            with open(full_path_file, "r") as f:
                text = f.read()
        return text

    @staticmethod
    def thread_it(qtd_threads, list_params, function):
        from tqdm import tqdm
        import threading as td

        threads = [td.Thread() for _ in range(qtd_threads)]
        counter = 0
        for param in tqdm(list_params, desc="Threading", unit="item"):
            threads[counter] = td.Thread(target=lambda: function(param))
            threads[counter].start()
            counter += 1
            if counter >= qtd_threads:
                [threads[i].join() for i in range(counter)]
                counter = 0
        if counter < qtd_threads:
            [threads[i].join() for i in range(counter)]

    @staticmethod
    def convert_string_date_to_datetime(date_string, date_format: str = "%d/%m/%Y"):
        # Convert the date string to a datetime object
        return datetime.strptime(date_string, date_format)

    def _load_credentials(self):
        """
        Loads the user's credentials from the interface or asks for them if they haven't been set yet.
        """
        if self.env:

            user = os.getenv(f"{self.prefix_env}_USUARIO")
            password = os.getenv(f"{self.prefix_env}_SENHA")
            self.credentials = [user, password]
            if None in self.credentials:
                self.ui.ask_credentials_cli()
        else:
            self.credentials = self.ui.load_credentials()
            if self.credentials is None:
                self.ui.ask_credentials()
                self.credentials = self.ui.load_credentials()

    def _conect_server_smtp(self):
        self.smtp_server = smtplib.SMTP(self.smtp, 587)
        self.smtp_server.connect(self.smtp, 587)

    def _start_server_smtp(self):
        self._conect_server_smtp()
        self.smtp_server.ehlo()
        self.smtp_server.starttls()
        self.smtp_server.ehlo()

    def _close_server_smtp(self):
        self.smtp_server.quit()

    def _login_smtp(self):
        self.smtp_server.login(*self.credentials)

    def _header_mail_smtp(self, assunto, email_destinatario, emails_em_copia):
        if not isinstance(emails_em_copia, list):
            emails_em_copia = emails_em_copia.split(";")
        emails_em_copia.append(self.credentials[0])
        COMMASPACE = ", "
        self.message = MIMEMultipart()
        self.message["From"] = self.credentials[0]
        self.message["To"] = COMMASPACE.join([email_destinatario])
        self.message["Cc"] = COMMASPACE.join(emails_em_copia)
        self.message["Subject"] = assunto
        self.all_mails_to_send = [email_destinatario] + emails_em_copia

    def _generate_html_message_smtp(self, saudacao, destinatario, text_mail):
        header = """
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #F5F5F5;
                        padding: 20px;
                        color: #333;
                    }
                    .container {
                        background-color: #fff;
                        border-radius: 5px;
                        padding: 20px;
                    }
                    h1 {
                        color: #4F4F4F;
                    }
                    h2 {
                        color: #414651;
                    }
                    h4 {
                        color: #4E74C3;
                    }
                    a {
                        color: #2F80ED;
                        text-decoration: none;
                    }
                    a:hover {
                        color: #0F53A6;
                    }
                </style>
            </head>

        """
        body = """
            <body>
                <div class="container">
                    <h2>#saudacao #destinatario</h1>
                    <h3>#text_mail</h2>
                    <a href="http://www.carvalima.com.br/">
                        <h4><br>Att.<br><strong>Carvalima Transportes</strong><br>
                        Rod. Palmiro Paes de Barros, n° 2700 - Parque Cuiabá | Cuiabá | MT | Brasil CEP: 78090-702
                        </h4>
                    </a>
                </div>
            </body>
        </html>
        """
        html = header + body
        self.create_folder("config")
        # html = self.create_file_txt(html, 'html_body_email', 'config')
        html = (
            html.replace("#saudacao", saudacao)
            .replace("#destinatario", destinatario)
            .replace("#text_mail", text_mail)
        )
        return html

    def _body_mail_smtp(
        self, saudacao, nome_destinatario, body_message, format_mail: str = "html"
    ):
        self.message.attach(
            MIMEText(
                self._generate_html_message_smtp(
                    saudacao, nome_destinatario, body_message
                ),
                format_mail,
            )
        )

    def _append_file_smtp(self, file_paths, type_file):
        for file_path in file_paths.split(";"):
            if ".pdf" in file_path.lower():
                type_file = "octet-stream"
            elif ".xlsx" in file_path.lower() or ".csv" in file_path.lower():
                type_file = "vnd.ms-excel"
            with open(os.path.abspath(file_path), "rb") as attachment:
                file_to_send = MIMEBase(
                    "application", type_file
                )  # ("application", "octet-stream") "vnd.ms-excel"
                file_to_send.set_payload(attachment.read())

            encoders.encode_base64(file_to_send)
            file_to_send.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file_path).replace(' ','_')}",
            )
            self.message.attach(file_to_send)

    def _send_smtp(self):
        self.smtp_server.sendmail(
            self.credentials[0], self.all_mails_to_send, self.message.as_string()
        )

    @time_out(raise_exception=True,show_exception=True)
    def send_email(
        self,
        assunto:str,
        email_destinatario:str,
        emails_em_copia:list|str,
        saudacao:str,
        nome_destinatario:str,
        body_message:str,
        path_file: str = None,
        type_file: str = "octet-stream",
        format_mail: str = "html",
    ):
        self._start_server_smtp()
        self._login_smtp()
        self._header_mail_smtp(assunto, email_destinatario, emails_em_copia)
        self._body_mail_smtp(saudacao, nome_destinatario, body_message, format_mail)
        if path_file is not None and len(path_file) > 0:
            self._append_file_smtp(path_file, type_file)
        self._send_smtp()
        self._close_server_smtp()

    def extract_payload(self,message):
        """Extrai o payload principal (texto) de uma mensagem de e-mail."""
        if message.is_multipart():
            # Itera pelas partes e encontra a parte de texto
            for part in message.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":  # Prioriza o texto simples
                    return part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
        else:
            # Mensagem não multipart, extrai o payload diretamente
            return message.get_payload(decode=True).decode(message.get_content_charset() or 'utf-8')


    @time_out(3,raise_exception=True,show_exception=True)
    def forward_email(
        self,
        original_email_id: str | int,
        forward_to: str | list,
        body:str
    ) -> None:
        """Cria e envia um e-mail de encaminhamento."""
        status, data = self.imap_server.fetch(str(original_email_id), '(RFC822)')
        if status == 'OK':
            original_message =  email.message_from_bytes(data[0][1])
        else:
            raise Exception("Erro ao recuperar e-mail.")
        
        forwarded_message = EmailMessage()
        COMMASPACE = ", "
        subject = original_message['Subject'].replace('\n', '').replace('\r', '')
        forwarded_message['Subject'] = f"Fwd: {subject}"
        forwarded_message['From'] = self.credentials[0]
        forwarded_message['To'] = COMMASPACE.join(forward_to.split(';'))
        # Extrai o conteúdo do e-mail original
        original_content = self.extract_payload(original_message)

        # Torna a mensagem multipart para aceitar anexos
        forwarded_message.make_mixed()
        # Opcional: incluir o e-mail original como anexo (preserva 100% dos dados)
        forwarded_message.attach(MIMEText(
            body
            ))
        #forwarded_message.set_content(f"Encaminhando o e-mail:\n\n---\n{original_content}")
        

        forwarded_message.add_attachment(original_message.as_bytes(), maintype='message', subtype='rfc822')
    
        self._start_server_smtp()
        self._login_smtp()
        self.smtp_server.send_message(forwarded_message)
        print("E-mail encaminhado com sucesso!")
        self._close_server_smtp()

    @time_out(3,raise_exception=True,show_exception=True)
    def forward_email2(
        self,
        original_email_id: str | int,
        forward_to: str | list,
        body: str
        ) -> None:
        """Cria e envia um e-mail de encaminhamento."""
        # Recupera o e-mail original
        status, data = self.imap_server.fetch(str(original_email_id), '(RFC822)')
        if status == 'OK':
            original_message = email.message_from_bytes(data[0][1])
        else:
            raise Exception("Erro ao recuperar e-mail.")
        
        forwarded_message = EmailMessage()
        COMMASPACE = ", "
        
        # Configura o assunto
        subject = original_message['Subject'].replace('\n', '').replace('\r', '')
        forwarded_message['Subject'] = f"Fwd: {subject}"
        forwarded_message['From'] = self.credentials[0]
        forwarded_message['To'] = COMMASPACE.join(forward_to.split(';'))
        
        # Extrai o conteúdo do e-mail original
        original_content = self.extract_payload(original_message)

        # Constrói o corpo do e-mail com o histórico
        forwarded_message.set_content(f"{body}\n\n--- Histórico do E-mail Original ---\n{original_content}")
        
        # Torna a mensagem multipart para aceitar anexos
        forwarded_message.make_mixed()

        # Anexa os anexos do e-mail original
        for part in original_message.walk():
            content_disposition = part.get("Content-Disposition")
            if content_disposition and "attachment" in content_disposition:
                # Extrai o conteúdo do anexo
                attachment_data = part.get_payload(decode=True)
                filename = part.get_filename()
                # Limpa o nome do arquivo para remover caracteres inválidos
                if filename:
                    filename = filename.replace('\n', '').replace('\r', '')

                if filename:
                    # Cria o anexo
                    attachment = MIMEBase(part.get_content_type().split('/')[0], part.get_content_type().split('/')[1])
                    attachment.set_payload(attachment_data)
                    encoders.encode_base64(attachment)
                    attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                    # Adiciona o anexo ao e-mail de encaminhamento
                    forwarded_message.add_attachment(attachment_data, maintype=part.get_content_type().split('/')[0],
                                                    subtype=part.get_content_type().split('/')[1],
                                                    filename=filename)

        forwarded_message.add_attachment(original_message.as_bytes(), maintype='message', subtype='rfc822')
        # Envia o e-mail
        self._start_server_smtp()
        self._login_smtp()
        self.smtp_server.send_message(forwarded_message)
        print("E-mail encaminhado com sucesso!")
        self._close_server_smtp()

    def set_flag(self, email_id, flag: str) -> bool:
        """Além das flagas padrão do imap:
        \Seen: Indica que o e-mail foi lido.
        \Answered: Indica que o e-mail foi respondido.
        \Flagged: Indica que o e-mail foi marcado como importante.
        \Deleted: Indica que o e-mail foi marcado para exclusão.
        \Draft: Indica que o e-mail é um rascunho.
        \Recent: Indica que o e-mail é novo e ainda não foi acessado por nenhum cliente de e-mail.
        Com este metodo voce pode settar novas flags personalizadas passando uma string.
        Não inserir "\" na flag, pois o servidor imap não reconhecerá sua "\flag" como válida
        """
        try:
            # Note the absence of `\` before the flag for custom flags
            result = self.imap_server.store(str(email_id), "+FLAGS", flag)
            if result[0] == "OK":
                logging.info(f"Flag {flag} set for email ID {email_id}")
                return True
            else:
                logging.error(f"Falha ao setar flag {flag} para o email ID {email_id}")
                return False
        except Exception as e:
            logging.exception(f"Erro ao setar flag {flag} ao email ID {email_id}: {str(e)}")
            return False

    def remove_flag(self, email_id, flag: str) -> bool:
        """Remove uma flag acicionada.
        Não inserir "\" na flag, pois o servidor imap não reconhecerá sua "\flag" como válida
        """
        try:
            result = self.imap_server.store(str(email_id), "-FLAGS", flag)
            if result[0] == "OK":
                logging.info(f"Flag {flag} removed for email ID {email_id}")
                return True
            else:
                logging.error(f"Falha ao remover flag {flag} do email ID {email_id}")
                return False
        except Exception as e:
            logging.exception(f"Error ao remover flag {flag} do email ID {email_id}: {str(e)}")
            return False

    def check_flag(self, email_id, flag: str) -> bool:
        """Verifica se uma determinada flag foi setada no email
        Não inserir "\" na flag, pois o servidor imap não reconhecerá sua "\flag" como válida
        """
        try:
            result, data = self.imap_server.uid("fetch", str(email_id), "(FLAGS)")
            if result == "OK":
                flags = data[0].decode()
                if flag in flags:
                    logging.info(f"Email ID {email_id} contém a flag {flag}")
                    return True
                else:
                    logging.info(f"Email ID {email_id} não possui a flag {flag}")
                    return False
            else:
                logging.error(f"Falha ao verificar flags no email ID {email_id}")
                return False
        except Exception as e:
            logging.exception(f"Erro ao verificar flag {flag} no email ID {email_id}: {str(e)}")
            return False

    def login_imap(self):
        try:
            self.imap_server.login(*self.credentials)
        except imaplib.IMAP4.error as e:
            logging.exception('Error during login, ensure you dont tried to login twice with an already ative session')
            self.logout()
            self.imap_server.login(*self.credentials)

    def select_imap(self, partition: str = "INBOX"):
        self.imap_server.select(partition)

    def logout(self):
        self.imap_server.logout()

    def get_all_emails_ids(self):
        result, data = self.imap_server.uid("search", None, "ALL")
        mail_ids = data[0]
        id_list = mail_ids.split()
        id_list = [int(id_) for id_ in id_list]
        return id_list

    def get_content_from_email_id(self, id_):
        logging.info(id_)
        result, message_raw = self.imap_server.uid("fetch", str(id_), "(BODY.PEEK[])")
        if message_raw is not None and message_raw[0] is not None:
            raw_email = message_raw[0][1].decode(
                "utf-8"
            )  # converts byte literal to string removing b''"utf-8"
            email_message = email.message_from_string(raw_email)
        return email_message
    
    def extract_all_tables_from_email_html(self,id_):
        from bs4 import BeautifulSoup
        import pandas as pd
        import chardet
        message = self.get_content_from_email_id(id_)
        email_body = None
        try:
            if message.is_multipart():
                for part in message.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/html":
                        part_content = part.get_payload(decode=True)
                        detected_encoding = chardet.detect(part_content)['encoding']  # Detecta a codificação
                        print(f'Detected encoding: {detected_encoding}')
                        email_body = part_content.decode(detected_encoding, errors='replace')  # Decodifica com a codificação detectada
            else:
                email_body = message.get_payload(decode=True).decode()
        except UnicodeDecodeError as e:
            logging.error(e)
        
        # Lista para armazenar os DataFrames
        dataframes = []
        if email_body:
            soup = BeautifulSoup(email_body, 'html.parser')
            # Procura a tabela no corpo do e-mail
            tables = soup.find_all('table')
            if not tables:
                raise Exception("Tabela não encontrada no e-mail.")
            

            
            for table in tables:
                rows = []
                # Itera pelas linhas da tabela
                for row in table.find_all('tr'):
                    # Extrai o texto de cada célula (td ou th)
                    cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                    rows.append(cells)
                # Converte para DataFrame
                if rows:
                    df = pd.DataFrame(rows)
                    df.columns = df.iloc[0]  # Define a primeira linha como cabeçalho
                    df = df[1:].reset_index(drop=True)  # Remove a primeira linha e redefine os índices
                    print(df)
                    dataframes.append(df)
            
        return dataframes
    
    def get_content_from_email_id_by_fetch(self, id_):
        _, data = self.imap_server.fetch(str(id_).encode(), "(RFC822)")
        email_message = data[0][1].decode("utf-8")
        email_message = email.message_from_string(email_message)
        return email_message

    def get_sender_mail_from_email_id(self, id_):
        email_message = self.get_content_from_email_id_by_fetch(id_)
        mail_from = email_message["From"]
        logging.info(mail_from)
        return mail_from

    def get_text_from_email_id(self, id_):
        content = self.get_content_from_email_id(id_)
        logging.info("#" * 60)
        texts = [
            part.as_string()
            for part in content.walk()
            if part.get_content_maintype() == "text"
        ]
        logging.info(texts)
        return texts

    def get_email_ids_by_sender_mail(self, sender_mail):
        result, email_ids = self.imap_server.search(None, f'(FROM "{sender_mail}")')
        email_ids = email_ids[0].split()
        email_ids = [int(id_) for id_ in email_ids]
        logging.info(email_ids)
        return email_ids

    def get_email_ids_by_subject(self, subject):
        # Use the SUBJECT search criterion instead of FROM
        result, email_ids = self.imap_server.search(None, f'(SUBJECT "{subject}")')
        email_ids = email_ids[0].split()
        email_ids = [int(id_) for id_ in email_ids]
        logging.info(email_ids)
        return email_ids

    def get_email_ids_by_range_date(self, data_ini, data_fim):
        data_ini = self.convert_string_date_to_datetime(data_ini)
        data_fim = self.convert_string_date_to_datetime(data_fim)
        status, email_ids = self.imap_server.search(
            None,
            '(OR SINCE "{0:%d-%b-%Y}" ON "{1:%d-%b-%Y}")'.format(data_ini, data_fim),
        )
        email_ids = email_ids[0].split()
        email_ids = [int(id_) for id_ in email_ids]
        logging.info(email_ids)
        return email_ids

    def clean_filename(self,filename):
        if isinstance(filename,str):
            # Define a pattern to match any character that is not allowed in filenames
            invalid_characters = r'[<>:"/\\|?*\;\n\r+,-]'

            # Replace invalid characters with an underscore or remove them
            cleaned_filename = re.sub(invalid_characters, '_', filename)


            # Optionally, trim leading and trailing whitespace
            cleaned_filename = cleaned_filename.strip()
            logging.info(f"Filename: {filename}", )
            logging.info(f"Cleaned Filename: {cleaned_filename}")
            return cleaned_filename

    def get_attachments_from_email_id(self, id_, folder_to,list_types_to_download:list=None):
        os.makedirs(folder_to,exist_ok=True)
        content = self.get_content_from_email_id(id_)
        for part in content.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is None :#or 'attachment' not in part.get("Content-Disposition"):
                continue

            fileName = part.get_filename()
            fileName = self.clean_filename(fileName)
            if fileName is None:
                continue
            ext = fileName.split('.')[-1] if '.' in fileName else None
            list_types_to_download = [value.upper() for value in list_types_to_download] if list_types_to_download is not None else None
            if ext is not None and list_types_to_download is not None and ext.upper() not in list_types_to_download:
                continue
            if bool(fileName):
                try:
                    filePath = os.path.abspath(os.path.join(folder_to, fileName))
                    if not os.path.isfile(filePath):
                        logging.info(fileName)
                        with open(filePath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                except Exception as e:
                    logging.exception(e)


class EmailInterface:
    """
    A class that provides an interface for entering and storing encrypted credentials.

    :Example:

        >>> email_interface = EmailInterface()
        >>> email_interface.ask_credentials()
        >>> credentials = email_interface.load_credentials()

    """

    def __init__(self):
        """
        Constructor method.
        Initializes the EmailInterface object with several tkinter widgets and an instance of the EmailCript class.
        """
        super().__init__()

        # configurando to titulo do app e a geometria dinamica
        # gb.init_root().title("Webmail")
        # gb.init_root().geometry("+100+100")

        self.entry_login = None
        self.label_login = None
        self.button_login = None
        self.credentials = None
        self.messagebox_window = None
        self.label_image = None
        self.label_messabox = None
        self.button_messagebox = None

        self.path_credentials = os.path.join(
            os.getcwd(), "parameters/webmail_credentials.bot"
        )

        self.cript = EmailCript()

    def _create_folder(self, path):
        """
        Creates a folder at the specified path if it does not already exist.

        :param path: Path to the folder to be created.
        :type path: str
        :return: Absolute path to the folder.
        :rtype: str
        """
        path = os.path.abspath(path)
        os.makedirs(path, exist_ok=True)
        return path

    def ask_credentials(self):
        """
        Presents an interface for entering credentials.

        :return: None
        """
        self.credentials_window = customtkinter.CTkToplevel(gb.init_root())
        self.credentials_window.title("Webmail")
        self.credentials_window.attributes("-topmost", True)
        self.credentials_window.geometry("+100+100")

        # criando a interface the inserção das credenciais
        self.entry_frame = customtkinter.CTkFrame(self.credentials_window)
        self.entry_frame.grid(
            row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        image = self._load_image(
            os.path.join(PARENT_DIR, "assets/webmail_logo.png"), 30, 30
        )
        self.label_login = customtkinter.CTkLabel(
            self.entry_frame,
            text="Insira suas credenciais!",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            image=image,
            compound="left",
        )
        self.label_login.grid(row=1, column=0, padx=(20, 20), pady=(20, 10))

        self.entry_login = [customtkinter.CTkEntry(self.entry_frame) for _ in range(2)]
        self.entry_login[0] = customtkinter.CTkEntry(
            self.entry_frame, placeholder_text="Email", width=70
        )
        self.entry_login[0].grid(
            row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        self.entry_login[1] = customtkinter.CTkEntry(
            self.entry_frame, placeholder_text="Senha", show="*"
        )
        self.entry_login[1].grid(
            row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        self.button_login = customtkinter.CTkButton(
            self.entry_frame, text="Avançar", command=self._button_login_event
        )
        self.button_login.grid(
            row=4, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        try:
            self.credentials_window.mainloop()
        except RuntimeError as e:
            logging.exception(e)

    def set_persistent_env_var(self, var_name, var_value):
        import subprocess

        system = platform.system()

        if system == "Windows":
            # Set an environment variable persistently on Windows
            subprocess.run(["setx", var_name, var_value], check=True)
        elif system == "Linux":
            # Set an environment variable persistently on Linux
            # Writing to .bashrc for the user
            home = os.path.expanduser("~")
            bashrc_path = os.path.abspath(os.path.join(home, ".bashrc"))
            with open(bashrc_path, "a") as bashrc:
                bashrc.write(f'\nexport {var_name}="{var_value}"\n')
            logging.info(
                f"Variable added to {bashrc_path}. Please re-login or source the file."
            )
        else:
            raise NotImplementedError(
                f"Setting environment variables persistently is not implemented for {system}"
            )

    def ask_credentials_cli(self):
        import getpass

        list_params = ["USUARIO", "SENHA"]
        values = []
        for param in list_params:
            if "senha" in param.lower() or "password" in param.lower():
                value = getpass.getpass(f"Informe a Senha ({self.prefix_env}): ")
            else:
                value = input(
                    f"Informe o(a) {param} ({self.prefix_env}) do webmail carvalima: "
                )

            self.set_persistent_env_var(f"{self.prefix_env}_{param}".upper(), value)
            values.append(value)
        self.credentials = values

    def _button_login_event(self):
        """
        Encrypts the entered credentials and stores them if they are valid.

        :return: None
        """
        self.credentials = [
            self.cript.cripto_data(str(entry.get())) if len(entry.get()) > 0 else None
            for entry in self.entry_login
        ]
        if None in self.credentials:
            self.messagebox("Insira sua credenciais\n corretamente!")
        else:
            self._store_credentials()

        self.credentials_window.quit()
        self.credentials_window.destroy()

    def _store_credentials(self):
        """
        Stores the encrypted credentials in a file.

        :return: None
        """
        self._create_folder("parameters")
        self.credentials = " ;".join(self.credentials)
        with open(self.path_credentials, "w") as file:
            file.write(self.credentials)

    def messagebox(self, message, type_alert: str = "warning"):
        """
        Presents a messagebox with a given message and alert type.

        :param message: Message to be displayed.
        :type message: str
        :param type_alert: Alert type (either 'warning' or 'info').
        :type type_alert: str
        :return: None
        """
        self.messagebox_window = customtkinter.CTkToplevel(self)
        self.messagebox_window.title(type_alert.upper())
        self.messagebox_window.attributes("-topmost", True)

        self.messagebox_window.geometry("300x300+170+170")
        self.messagebox_window.rowconfigure(1, weight=1)
        self.messagebox_window.columnconfigure(0, weight=1)

        image = (
            self._load_image(os.path.join(PARENT_DIR, "assets/warning.png"))
            if type_alert == "warning"
            else self._load_image(os.path.join(PARENT_DIR, "assets/info.png"))
        )
        self.label_image = customtkinter.CTkLabel(
            self.messagebox_window, text="", image=image, compound="left"
        )
        self.label_image.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        self.label_messabox = customtkinter.CTkLabel(
            self.messagebox_window,
            text=message,
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.label_messabox.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="nsew")

        self.button_messagebox = customtkinter.CTkButton(
            self.messagebox_window, text="Ok", command=self.messagebox_window.destroy
        )
        self.button_messagebox.grid(
            row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        self.messagebox_window.mainloop()

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
            with open(self.path_credentials, "r") as file:
                self.credentials = file.read().split(";")
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

    def loop(self):
        """
        Starts the tkinter event loop.

        :return: None
        """
        try:
            gb.init_root().mainloop()
        except RuntimeError as e:
            logging.exception(e)


class EmailCript:
    """
    A class used for the encryption and decryption of data, which uses Fernet symmetric encryption.

    :Example:

        >>> email_cript = EmailCript()
        >>> encrypted_data = email_cript.cripto_data("some sensitive data")
        >>> original_data = email_cript.decripto_data(encrypted_data)

    """

    def __init__(self):
        """
        Constructor method.
        Initializes the SswCript object with None as the key.
        """
        self.key = None

    def create_folder(self, path):
        """
        Creates a folder at the specified path.

        :param path: Path to the folder to be created.
        :type path: str
        :return: Absolute path to the folder.
        :rtype: str
        """
        if ":" not in path:
            root_path = os.getcwd()
            path = os.path.abspath(root_path + f"/{path}")

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

        if system == "Windows":
            # Path for AppData in Windows
            current_user = os.getenv("APPDATA")
            path_store_key = os.path.abspath(current_user + "/AppData/Local/cvl")
        elif system == "Linux":
            home_dir = os.path.expanduser("~")  # Gets the home directory
            path_store_key = os.path.join(
                home_dir, ".cvl"
            )  # Creates a path within the home directory
            os.makedirs(path_store_key, exist_ok=True)
        else:
            logging.error(f"Unsupported operating system: {system}")
            return
        os.makedirs(path_store_key, exist_ok=True)
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
        self.create_folder(path_store_key)
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
        salted = ""
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
        original_dados = ""
        salt = string.ascii_uppercase + string.ascii_lowercase
        for i, c in enumerate(salted[::-1]):
            index = salt.find(c)
            index_char_alt_range = salt[-7:].find(c)
            d_salted = (
                salt[index + 7]
                if index_char_alt_range == -1
                else salt[index_char_alt_range]
            )
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


if __name__ == "__main__":
    email = Email()
    email.send_email(
        "Nem Email Class",
        "benstronics@gmail.com",
        ["b.hsantossdg@gmail.com"],
        "Olá",
        "Ben-Hur",
        "I'm fine and you?",
    )
