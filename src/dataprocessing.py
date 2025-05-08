import os
import sys
import pandas as pd
import re
from dataprocess import dataprocessing as hd
import pandas as pd
from priority_classes.database.database import Postgresql
import re
from datetime import datetime

# from settings import (
#     PATH_DOWNLOADS
# )

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ler_arquivo():
    arquivo_csv = 'relatorios/tickets.csv'
    table = hd.import_file(arquivo_csv, encoding='utf-8')
    table = hd.clear_table(table)
    dtype = {
        'datetime':[
            'createdAt',
            'closedAt',
            'acceptedAt',
            'updatedAt'
        ]
    }
    table = hd.convert_table_types(table, dtypes=dtype)
    print(table)
    print(table.info())
    
    return table

def to_db(table):
    db = Postgresql()
    table['Data de atualizacao'] = datetime.now()
    dtype = {
        'Data de atualizacao': 'TIMESTAMP',
        'createdAt': 'TIMESTAMP',
        'closedAt': 'TIMESTAMP',
        'acceptedAt': 'TIMESTAMP',
        'updatedAt': 'TIMESTAMP'
    }
    db.to_postgresql(
        table, table_name='tickets_sacflow', dtypes_columns=dtype,
        call_procedure=db.create_procedure_to_delete_duplicateds('tickets_sacflow')
    )
    
if __name__ == "__main__":
    table = ler_arquivo()
    to_db(table)