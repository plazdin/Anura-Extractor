import numpy as np
import pandas as pd

from utils import bqo


class PandAnura():

    def __init__(self, jdata: list | str) -> None:
        if isinstance(jdata, str):
            jdata = pd.read_json(jdata)

        self.__formata = bqo.query("SELECT * from bd-sanjorge.ANURA.HISTORIAL limit 1")
        self.data = pd.DataFrame(self.__normalize(jdata))
        self.__data_format()



    def __normalize(self, data: list) -> list:
        '''
        Normalizes the overall structure of the dataframe.
        '''
        normalized_data = []
        for n in data:
            
            normalized = {
                'Fecha_llamada': n['answertime'],
                'Direccion': n['direction'],
                'Estado': n['status'],
                'Nro_Origen': n['calling'],
                'Origen': n['callingname'],
                'Nro_Destino': n['called'],
                'Destino': n['calledname'],
                'Duracion_Total': n['duration'],
                'Duracion_Conversacion': n['billseconds'],
                'Ultima_accion': n['last_action'],
                'Tiempo_espera': n['duration'] - n['billseconds'],
                'id': n['id'],
                'cola_agente': None,
                'cola_terminal_agente':  None
            }
            
            if n['answerby']:
                normalized['cola_agente'] = n['answerby']['accountname']
                normalized['cola_terminal_agente'] = n['answerby']['terminalname']
            
            normalized_data.append(normalized)
        return normalized_data
    

    def __data_format(self) -> None:
        '''
        Simple method that ends the convertion of dataframe, modifying some cols to strict str
        and Fecha_llamada col into a datetime format
        '''
        to_str = [
            'Direccion', 'Estado', 'Origen',
            'Nro_Destino', 'Destino','Ultima_accion',
            'cola_agente', 'cola_terminal_agente'
        ]
        for col in to_str:
            self.data[col] = self.data[col].astype(str)

        self.data['Fecha_llamada'] = pd.to_datetime(self.data['Fecha_llamada'])
        self.data = self.data.replace('None', np.nan)

        # Here we take the dtypes of formata to make our PandAnura
        # object 100% compatible with the dataset of Bigquery.
        cols_to_convert = self.data.select_dtypes(
            include=['object', 'int64']
        ).columns

        self.data[cols_to_convert] = self.data[cols_to_convert].astype(
            self.__formata[cols_to_convert].dtypes
        )


