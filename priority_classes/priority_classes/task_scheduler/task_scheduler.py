import os
import ctypes
import sys
from datetime import datetime, timedelta
from priority_classes.interface.interface import Interface
import subprocess
import json
import logging

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
PARENT_RELATIVE_DIR = os.getcwd()
PATH_XML_SCHEDULER = os.path.join(CURRENT_DIR,'task_scheduler.xml')
FOLDER_SCHEDULER = r'C:\Windows\System32\Tasks'
FOLDER_TASKS = 'BotsCarvalima'
PATH_TO_SAVE = os.path.join(os.getcwd(), 'config')
PATH_TO_WINDOWS_TASKS = os.path.join(FOLDER_SCHEDULER, FOLDER_TASKS)
proc_counter = 0

os.makedirs(PATH_TO_SAVE, exist_ok=True)


class TaskManager:

    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    @staticmethod
    def load_credencials():
        ui = Interface('windows_task_manager')
        return ui.load_credentials(['Usuario Windows', 'Senha Windows'])

    @staticmethod
    def get_start_date():
        current_datetime = datetime.now()
        new_datetime = current_datetime + timedelta(seconds=10)
        return new_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')

    @staticmethod
    def get_regiter_date():
        current_datetime = datetime.now()
        return current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')

    @staticmethod
    def get_user_id():
        return os.path.join(os.environ.get('USERDOMAIN'), os.environ.get('USERNAME'))

    @staticmethod
    def get_local_filepath(task_name):
        return os.path.join(PATH_TO_SAVE, task_name) + '.xml'

    @staticmethod
    def get_windows_task_filepath(task_name):
        return os.path.join(PATH_TO_WINDOWS_TASKS, task_name)

    def get_bots_schedules(self):
        bot_scheduler_path = os.path.join(FOLDER_SCHEDULER,FOLDER_TASKS)
        bots_schedule={}
        for bot in os.listdir(bot_scheduler_path):
            logging.info(bot)
            with open(os.path.join(bot_scheduler_path,bot), 'r', encoding='utf-16') as f:
                read_text = f.read()
                #logging.info(read_text)
            if 'Triggers>' in read_text:
                triggers = read_text.split('Triggers>')[1]
                bots_schedule[bot] = triggers
        logging.info(json.dumps(bots_schedule,indent=4))
    def calendar_trigger_now(self):
        xml="""
        <CalendarTrigger>
        <StartBoundary>#6</StartBoundary>
        <Enabled>true</Enabled>
        <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
        </ScheduleByDay>
        </CalendarTrigger>
        """.replace("#6", self.get_start_date())
        return  xml

    def boot_trigger(self):
        xml="""
        <BootTrigger>
          <Enabled>false</Enabled>
          <Delay>PT10S</Delay>
        </BootTrigger>
        """
        return  xml

    def repetition_trigger(self):
        xml="""
        <Repetition>
            <Interval>PT5M</Interval>
            <StopAtDurationEnd>false</StopAtDurationEnd>
        </Repetition>
        """
        return  xml

    def logon_trigger(self):
        xml="""
        <LogonTrigger>
              <Enabled>true</Enabled>
              <Delay>PT10S</Delay>
        </LogonTrigger>
        """
        return  xml

    def update_xml2(self, task_name, **kwargs):
        with open(PATH_XML_SCHEDULER, 'r', encoding='utf-16') as f:
            rows = f.readlines()
            for i, row in enumerate(rows):
                if '<Date>' in row:
                    rows[i] = rows[i].replace("#0", self.get_regiter_date())
                elif '<Author>' in row:
                    rows[i] = rows[i].replace("#1", self.get_user_id())
                elif '<URI>' in row:
                    rows[i] = rows[i].replace("#2", rf'\{os.path.join(FOLDER_TASKS, task_name)}')
                elif '<UserId>' in row:
                    rows[i] = rows[i].replace("#3", self.get_user_id())
                elif '<Command>' in row:
                    path_to_app = os.path.join(PARENT_RELATIVE_DIR, "bot_model_to_schedule.bat")
                    if 'path_to_app' in kwargs:
                        path_to_app = kwargs['path_to_app']

                    rows[i] = rows[i].replace("#4", f'"{path_to_app}"')
                elif '<WorkingDirectory>' in row:
                    rows[i] = rows[i].replace("#5", PARENT_RELATIVE_DIR)
                elif '<#replaceTriggers>' in row:
                    if 'boot_trigger' in kwargs and kwargs['boot_trigger']==True:
                        rows[i] = self.boot_trigger()

                    elif 'repetition_trigger' in kwargs and kwargs['repetition_trigger'] == True:
                        rows[i] = self.repetition_trigger()

                    elif 'logon_trigger' in kwargs and kwargs['logon_trigger'] == True:
                        rows[i] = self.logon_trigger()

                    else:
                        rows[i] = self.calendar_trigger_now()

                elif '<LogonType>' in row:
                    rows[i] = rows[i].replace("#7",
                                              'Password' if 'LogonType' not in kwargs else kwargs.pop('LogonType'))
                elif '<RunLevel>' in row:
                    rows[i] = rows[i].replace("#8",
                                              'HighestAvailable' if 'RunLevel' not in kwargs else kwargs.pop('RunLevel'))

                logging.info(rows[i])

        filepath = self.get_local_filepath(task_name)
        logging.info(filepath)
        if not os.path.exists(filepath) or 'substitute_always' in kwargs:
            with open(filepath, 'w', encoding='utf-16') as f:
                f.writelines(rows)
        return filepath

    def _create_task_scheduler(self, task_name, **kwargs):
        global proc_counter
        filepath = self.update_xml2(task_name, **kwargs)
        credentials = self.load_credencials()
        try:
            # Command to create a scheduled task from an XML file
            command = f'schtasks /create /tn "{FOLDER_TASKS}\\{task_name}" /xml "{filepath}" /RU "{credentials[0]}" /RP "{credentials[1]}" /F'
            subprocess.run(command, check=True, shell=False)
            logging.info("Task created successfully.")
        except subprocess.CalledProcessError as e:
            logging.info(f"An error occurred: {e}")
            if proc_counter == 0:
                proc_counter += 1
                self._create_task_scheduler(task_name, LogonType='InteractiveToken',**kwargs)


    def create_task_scheduler(self, task_name, **kwargs):
        if not os.path.exists(self.get_windows_task_filepath(task_name)):
            if self.is_admin():
                self._create_task_scheduler(task_name, **kwargs)
            else:
                #Re-run the program with admin rights
                retval = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                logging.info(retval)
                # cmd_command = f'cmd /k "{sys.executable}" {" ".join(sys.argv)}'
                #
                # # Re-run the program with admin rights, through cmd to keep the window open
                # retval = ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f'/c "{cmd_command}"', None, 1)
                # logging.info(retval)

    def update_file_task_on_scheduler(self,task_name, **kwargs):
        _=kwargs.pop('substitute_always') if 'substitute_always' in kwargs else None
        filepath = self.update_xml2(task_name,substitute_always=True, **kwargs)
        with open(filepath,'rb') as f:
            file_read = f.read()
        logging.info(file_read)
        with open(self.get_windows_task_filepath(task_name),'wb') as f:
            f.write(file_read)

if __name__ == '__main__':
    mg = TaskManager()
    mg.get_bots_schedules()
