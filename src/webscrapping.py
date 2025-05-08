from botweb import BotWeb
import json
import csv
import os
import requests
import unicodedata
from datetime import datetime

class MyBot(BotWeb):
    def __init__(self, *args, **kwargs):
        super().__init__(
            prefix_env="SSW",
            credentials_keys=['DOMINIO', "CPF", "USUARIO", "SENHA"]
        )
        self.headers = {
            "accept": "*/*",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }

    def _enter_domain(self):
        self.driver.execute_script(
            f"document.getElementById('1').value='{self.credentials['DOMINIO']}'"
        )

    def _enter_cpf(self):
        self.driver.execute_script(
            F"document.getElementById('2').value='{self.credentials['CPF']}'"
        )

    def _enter_user(self):
        self.driver.execute_script(
            F"document.getElementById('3').value='{self.credentials['USUARIO']}'"
        )

    def _enter_password(self):
        self.driver.execute_script(
            F"document.getElementById('4').value='{self.credentials['SENHA']}'"
        )

    def _click_submit(self):
        self.driver.execute_script(
            F"document.getElementById('5').click()"
        )

    def _enter_code(self, code):
        self.driver.execute_script(
            F"document.getElementById('3').value='{code}'; doOption();"
        )

    def login(self):
        self._enter_domain()
        self._enter_cpf()
        self._enter_user()
        self._enter_password()
        self._click_submit()
        self.get_cookies()

    def fetch_data_from_api(self, url, headers):
        """Faz uma solicitação GET à API e retorna os dados em formato JSON."""
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro na API: {response.status_code} - {response.text}")

    def save_to_json_file(self, data, filepath):
        """Salva os dados em um arquivo JSON."""
        folder = os.path.dirname(filepath)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def convert_datetime(self, date_str):
        """
        Converte a string de data da API para o formato aceito pelo banco de dados.
        Formato de entrada: '2024-03-04T15:17:57.056Z'
        Formato de saída: '2024-03-04 15:17:57'
        """
        if not date_str:
            return None  

        try:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            return dt.strftime("%Y-%m-%d %H:%M:%S")  # Remove os milissegundos
        except ValueError as e:
            print(f"Erro ao converter data: {date_str} - {e}")
            return None

    def remove_accents(self, text):
        """Remove acentos e caracteres especiais de um texto."""
        if not text:
            return ""
        nfkd_form = unicodedata.normalize('NFKD', text)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def save_csv(self, filename, data):
        """Salva os dados em um arquivo CSV, removendo acentos."""
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        fieldnames = [
            "id_ticket", "accountId", "contactId", "channel", "createdAt", "closedAt", 
            "feedbackScore", "queueId", "queue_name", "acceptedAt", "archived", "status", 
            "userId", "user_name","uniqueKey", "whatsappId", "updatedAt", "contact_id", 
            "contact_name", "contact_email", "contact_number", "contact_profilePicUrl"
        ]

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                for row in data:
                    cleaned_row = {k: self.remove_accents(str(v)) for k, v in row.items()}
                    writer.writerow(cleaned_row)
        except PermissionError:
            print(f"Erro: Permissão negada ao acessar {filename}. Feche o arquivo e tente novamente.")

    def process_and_save_data(self, data):
        """Processa os dados, converte datas e salva no CSV."""
        processed_data = []
        for ticket in data.get("tickets", []):
            processed_data.append({
                "id_ticket": ticket.get("id", ""),
                "accountId": ticket.get("accountId", ""),
                "contactId": ticket.get("contactId", ""),
                "channel": ticket.get("channel", ""),
                "createdAt": self.convert_datetime(ticket.get("createdAt", "")),
                "closedAt": self.convert_datetime(ticket.get("closedAt", "")),
                "feedbackScore": ticket.get("feedbackScore", ""),
                "queueId": ticket.get("queueId", ""),
                "queue_name": self.remove_accents(ticket.get("queue", {}).get("name", "")),
                "acceptedAt": self.convert_datetime(ticket.get("acceptedAt", "")),
                "archived": ticket.get("archived", ""),
                "status": ticket.get("status", ""),
                "userId": ticket.get("userId", ""),
                "user_name": self.remove_accents(ticket.get("user", {}).get("name", "")),
                "uniqueKey": ticket.get("uniqueKey", ""),
                "whatsappId": ticket.get("whatsappId", ""),
                "updatedAt": self.convert_datetime(ticket.get("updatedAt", "")),
                "contact_id": ticket.get("contact", {}).get("id", ""),
                "contact_name": self.remove_accents(ticket.get("contact", {}).get("name", "")),
                "contact_email": ticket.get("contact", {}).get("email", ""),
                "contact_number": ticket.get("contact", {}).get("number", ""),
                "contact_profilePicUrl": ticket.get("contact", {}).get("profilePicUrl", ""),
            })

        self.save_csv("relatorios/tickets.csv", processed_data)

if __name__ == '__main__':
    with MyBot() as mybot:
        mybot.init_browser(headless=True, browser="chrome")

        url = "https://api2.sacflow.io/api/public/tickets"
        headers = {
            "User-Agent": "insomnia/10.2.0",
            "Authorization": "Bearer ad8d672c-b196-4f2e-bf24-aaa8523ef258",
            "accountId": "2"
        }

        data = mybot.fetch_data_from_api(url, headers)
        mybot.save_to_json_file(data, 'dados.json')
        mybot.process_and_save_data(data)
