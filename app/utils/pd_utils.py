'''Provides simple functions to parse data into a dataframe.'''
from datetime import datetime

import pandas as pd

from schemas.datetime import Dates, Times
from utils.logger import log

def a_df(datafile) -> pd.DataFrame:
    '''Crea el dataframe final a partir de json, específico
    para los fines administrativos de San Jorge / KARDUR.'''
    irrelevant_fields =  [  # Campos que quedan fuera del excel.
        'account', 'answertime',
        'endtime', 'price', 'wasrecorded',
        'queue', 'answerby'
    ]
    data = pd.read_json(datafile)
    df1 = pd.DataFrame(data)
    raw_answers = []  # Respuestas en formato Dict
    for value in df1.answerby.values.tolist():
        if not isinstance(value, dict):
            value = {'accountname': None,
                    'terminalname': None
                    }
        raw_answers.append(value)

    df1['waittime'] = df1['duration'] - df1['billseconds']
    for column in irrelevant_fields:
        df1.pop(column)

    df1.columns = [  # Renombra las columnas
        'id','Direccion', 'Estado', 'Nro_Destino', 'Nro_Origen',
        'Destino', 'Origen', 'Fecha_llamada', 'Duracion_Total',
        'Duracion_Conversacion', 'Ultima_accion', 'Tiempo_espera',
        # 'Cuenta Respuesta', 'Terminal Respuesta'
        ]
    df1 = df1[[  # Reordenamiento de columnas
        'Fecha_llamada', 'Direccion', 'Estado',
        'Nro_Origen', 'Origen', 'Nro_Destino', 'Destino',
        'Duracion_Total', 'Duracion_Conversacion', 'Ultima_accion',
        'Tiempo_espera', 'id'#, 'Cuenta Respuesta', 'Terminal Respuesta'
        ]]

    to_str = [
        'Direccion', 'Estado', 'Origen',
        'Nro_Destino', 'Destino','Ultima_accion'
    ]

    for col in to_str:
        df1[col] = df1[col].astype(str)

    df1['Fecha_llamada'] = pd.to_datetime(df1['Fecha_llamada'])
    
    return df1



def query_maker(times: Times, dates: Dates) -> list[dict]:
    '''
    Makes a list of queries for anura api.\n
    Params:
    -------
    - times: a list of ints or digits that represents hours.
    - dates: a list of dates in "%Y%m%d" format.
    '''
    queries = list()

    for date in dates.get_dates():
        for hour in range(times.init, times.finish + 1):
            strhour = str(hour).rjust(2, '0')
            queries.append({
                'startDate': f'{date} {strhour}:00:00',
                'endDate':f'{date} {strhour}:59:59.999'
                })
    
    return queries
