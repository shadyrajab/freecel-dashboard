from requests import request
import pandas as pd
from typing import Optional
from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv('tokenFreecel')

headers = {
    'Authorization': f'Bearer {TOKEN}'
}

class Consultor:
    def __init__(self, nome: str, ano: Optional[int] = None, mes: Optional[str] = None):
        self.nome = nome
        self.ano = ano
        self.mes = mes

        self.data = self.__get_data__()

    def __get_data__(self):
        params = {
            "ano": self.ano,
            "mes": self.mes,
            "display_vendas": True
        }

        url = f'https://freecelapi-b44da8eb3c50.herokuapp.com/consultores/{self.nome}'
        data = request('GET', url = url, params = params, headers=headers).json()

        return data
    
    @property
    def years(self):
        return self.vendas.get('ano').unique().tolist()
    
    @property
    def months(self):
        return self.vendas.get('mês').unique().tolist()
    
    @property
    def name(self):
        return self.data.get('name')
    
    @property
    def receita_total(self):
        return self.data.get('receita_total')
    
    @property
    def quantidade_vendida(self):
        return self.data.get('quantidade_vendida')
    
    @property
    def quantidade_clientes(self):
        return self.data.get('quantidade_clientes')
    
    @property
    def receita_media_diaria(self):
        return self.data.get('receita_media_diaria')
    
    @property
    def quantidade_media_diaria(self):
        return self.data.get('quantidade_media_diaria')
    
    @property
    def quantidade_media_mensal(self):
        return self.data.get('quantidade_media_mensal')
    
    @property
    def receita_media_mensal(self):
        return self.data.get('receita_media_mensal')
    
    @property
    def ticket_medio(self):
        return self.data.get('ticket_medio')
    
    @property
    def delta_receita_mensal(self):
        if not self.ano and not self.mes:
            return 0
        
        return self.data.get('delta_receita_mensal')
    
    @property
    def delta_quantidade_mensal(self):
        if not self.ano and not self.mes:
            return 0
        
        return self.data.get('delta_quantidade_mensal')
    
    @property
    def vendas(self):
        dataframe = pd.DataFrame(self.data.get('vendas')).sort_values(
            by = 'data', ascending = False
        )

        dataframe['data'] = pd.to_datetime(dataframe['data'], unit='ms')
        return dataframe

    @property
    def groupby_data(self):
        vendas = self.vendas

        dataframe = vendas.groupby('data', as_index = False).sum(numeric_only = True).sort_values(
            by = 'data', ascending = False
        )
        return dataframe