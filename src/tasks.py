import os
import sys
from dataprocess import dataprocessing as hd

#from settings import *
import src.dataprocessing as dp
from src.webscrapping import MyBot
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def process_all_data():
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


def env_db():
    table = dp.ler_arquivo()
    dp.to_db(table)
    
    
if __name__ == '__main__':
    process_all_data()
    env_db()    
    