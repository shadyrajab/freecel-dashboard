from requests import request
import pandas as pd
from typing import Optional
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TOKEN = getenv('tokenFreecel')

class Vendas:
    def __init__(self, ano: Optional[int] = None, mes: Optional[str] = None) -> pd.DataFrame:
        self.ano = ano
        self.mes = mes
        self.vendas = self.__get_data__()

    def vendas_by_data(self, ano: Optional[int] = None, mes: Optional[str] = None):
        now = datetime.now()
        dataframe = self.vendas

        if ano and mes:
            
            return dataframe[(dataframe['ano'] == ano) & (dataframe['mês'] == mes)]

        dataframe = dataframe.groupby('data', as_index = False).sum(numeric_only = True)
            
        dataframe = dataframe[(dataframe['data'].dt.month != now.month) | (dataframe['data'].dt.year != now.year)]

        return dataframe

    def __get_data__(self):
        url = f'https://freecelapi-b44da8eb3c50.herokuapp.com/vendas'
        headers = {
            'Authorization': f'Bearer {TOKEN}'
        }

        data = request('GET', url = url, headers=headers).json()
        vendas = pd.DataFrame(data)
        vendas['data'] = pd.to_datetime(vendas['data'], unit='ms')

        vendas.replace(['NaN', 'UNDEFINED'], 'Não Informado', inplace = True)

        return vendas.sort_values(
            by = 'data', ascending=False)
