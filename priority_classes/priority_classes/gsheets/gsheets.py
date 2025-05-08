import gspread
import pandas as pd
import string
import logging
from oauth2client.service_account import ServiceAccountCredentials

def to_reference_hints():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f'{credentials_path_name}.json', scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_url(spreadsheet_url)
    sheet = spreadsheet.worksheet(sheet_name)
    sheet.get_all_records(**kwargs)

class Gsheets:

    def __init__(self):
        self.client = None
        self.spreadsheet = None
        self.sheet = None

    def login(self, credentials_path_name: str = 'api_bot_master'):
        """
        Authenticate and log in to Google Sheets API.

        :param credentials_path_name: The name of the JSON credentials file (without the .json extension).
        :type credentials_path_name: str
        """
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(f'{credentials_path_name}.json', scope)
        self.client = gspread.authorize(credentials)

    def acess_spreadsheet(self, url_sheet):
        """
        Open a specific Google Sheets spreadsheet.

        :param url_sheet: The URL of the Google Sheets file.
        :type url_sheet: str
        """
        spreadsheet_url = url_sheet
        self.spreadsheet = self.client.open_by_url(spreadsheet_url)

    def get_list_sheet_names(self):
        return [sheet.title for sheet in self.spreadsheet.worksheets()]

    def set_sheet_name(self, sheet_name):
        """
        Set the active worksheet in the Google Sheets file by its name.

        :param sheet_name: The name of the worksheet to be accessed.
        :type sheet_name: str
        """
        self.sheet = self.spreadsheet.worksheet(sheet_name)

    def get_all_records(self,dataframe:bool=True,**kwargs):
        """
        Read all data from the active worksheet and return it as a pandas DataFrame.

        :return: A pandas DataFrame containing all the data from the worksheet.
        :rtype: pandas.DataFrame
        """
        data = self.sheet.get_all_records(**kwargs)
        if dataframe:
            table = pd.DataFrame(data)
            logging.info(table)
            return table
        else:
            return data

    def get_all_values(self,**kwargs):
        return self.sheet.get_all_values(**kwargs)

    def clear_sheet(self):
        """
        Clear the contents of the active worksheet.
        """
        self.sheet.clear()

    def clear_table(self,table):
        """
        Clear the contents of the active worksheet.
        """
        table_list = list(map(lambda list: ['' for x in list] ,table.values.tolist()))
        logging.info(table_list)
        table = pd.DataFrame(table_list)
        return  table


    def table_to_sheets(self, table, start_cell: str = 'a2',headers:bool=True):
        """
        Write a pandas DataFrame to the active worksheet starting from the specified cell.

        :param table: The pandas DataFrame to be written to the worksheet.
        :type table: pandas.DataFrame
        :param start_cell: The cell address (e.g., 'a2') where the DataFrame should be written. Default is 'a2'.
        :type start_cell: str
        """
        columns = list(table.columns)
        # Convert the DataFrame to a list of lists and add the headers at the first row
        if headers:
            data_to_write = [columns] + table.values.tolist()
        else:
            data_to_write = table.values.tolist()
        # Update the range with the data
        self.sheet.update(start_cell, data_to_write,raw=False)

        logging.info("Data has been written to Google Sheets.")

    def update_cell_value(self, index_col, index_row, value):
        """
        Update the value of a specific cell in the active worksheet.

        :param index_col: The column index of the cell to be updated (1-based).
        :type index_col: int
        :param index_row: The row index of the cell to be updated (1-based).
        :type index_row: int
        :param value: The new value to be written into the cell.
        :type value: Any
        """
        self.sheet.update_cell(index_col, index_row, value)


if __name__ == '__main__':
    url_sheet = 'https://docs.google.com/spreadsheets/d/1BDqgh893rfEr00eC2AwD0rIQQDlaZ_snnQqSqRuNKIs/edit#gid=1449425634'
    gsh = Gsheets()
    gsh.login('api_bot_master')
    gsh.acess_spreadsheet(url_sheet)
    gsh.set_sheet_name('Página5')
    gsh.get_all_records()
    gsh.set_sheet_name('Página6')
    gsh.get_all_records()
    gsh.clear_sheet()
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(f'api.json', scope)
    # client = gspread.authorize(credentials)
    # spreadsheet = client.open_by_url('')
    # sheet = spreadsheet.worksheet('')
    # sheet.update()

