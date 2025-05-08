import os
import sys
import platform
from dataprocess import dataprocessing as hd

from settings import *
import src.tasks as ts
from priority_classes.app.app import BotApp
from priority_classes.decorators.decorators import time_out


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

system = platform.system()

app = BotApp()

app.set_bot(
    bot_name='Bot_new_api_sacflow',
    bot_description='Baixa relatorio de atendimento do Sacflow',
    bot_version='1.0.0',
    bot_department='QUALIDADE'
)


@time_out(1)
def init_credentials():
    """
    Initialize SSW Credentials.

    This function initializes SSW credentials by opening a browser, logging in, and extracting the user information.

    :return: The user's information.
    :rtype: str
    """
    from priority_classes.ssw.ssw import SswRequest
    ssw = SswRequest()
    ssw.init_browser()
    ssw.login()
    user = ssw.credentials[2]
    app.set_user(user)
    return user

#teste

@app.task
def process_all_data():
    """This task do this"""
    ts.process_all_data()


@app.task
def env_db():
    """This task do this"""
    ts.env_db()

# @app.task
# def to_db():
#     """This task do this"""
#     ts.to_db()


def main_ui():
    from priority_classes.interface.interface import Interface
    while True:
        ui = Interface(user=init_credentials())
        buttons_name = ['task1', 'task2']
        buttons_func = [task1, task2]
        ui.ui(buttons_name, buttons_func)


def main():
    # if system == 'Windows':
    #     from priority_classes.task_scheduler.task_scheduler import TaskManager
    #     mg = TaskManager()
    #     mg.create_task_scheduler(app.bot_name)

    process_all_data()
    env_db()
    #to_db()


@time_out()
def main_api():
    """
    pip install Flask
    pip install Flask-RESTful
    pip install Flask-Limiter
    pip install flask-cors
    """
    import priority_classes.wrap_api.wrap_api as wp
    wp.api_wrap('/api/task1', 'task1', task1, methods=['POST'])
    wp.run('50001', False)


if __name__ == '__main__':
    pass
