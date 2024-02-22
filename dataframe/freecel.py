from requests import request
import pandas as pd
from typing import Optional
from dotenv import load_dotenv
from os import getenv
from typing import Optional
from datetime import datetime

load_dotenv()

TOKEN = getenv('tokenFreecel')

headers = {
    'Authorization': f'Bearer {TOKEN}'
}

class Stats:
    def __init__(self, ano: Optional[int] = None, mes: Optional[str] = None):
        self.ano = ano
        self.mes = mes

        self.data = self.__get_data__()
    
    def __get_data__(self):
        params = {
            "ano": self.ano,
            "mes": self.mes,
        }

        url = f'https://freecelapi-b44da8eb3c50.herokuapp.com/stats?'
        data = request('GET', url = url, params = params, headers=headers).json()

        return data
    
    @staticmethod
    def vendas(ano: Optional[int] = None, mes: Optional[str] = None, groupby: Optional[str] = None):
        now = datetime.now()
        url = f'https://freecelapi-b44da8eb3c50.herokuapp.com/vendas'
        params = {
            "ano": ano,
            "mes": mes,
        }

        data = request('GET', url = url, headers=headers, params=params).json()
        vendas = pd.DataFrame(data)
        vendas['data'] = pd.to_datetime(vendas['data'], unit='ms')

        if groupby:
            vendas = vendas.groupby('data', as_index = False).sum()
            vendas = vendas[(vendas['data'].dt.month != now.month) | (vendas['data'].dt.year != now.year)]

        vendas.replace(['NaN', 'UNDEFINED'], 'Não Informado', inplace = True)

        return vendas.sort_values(
            by = 'data', ascending=False)
    
    @property
    def receita_total(self):
        return self.data['receita_total']
    
    @property
    def quantidade_vendida(self):
        return self.data['quantidade_vendida']
    
    @property
    def quantidade_clientes(self):
        return self.data['quantidade_clientes']
    
    @property 
    def ticket_medio(self):
        return self.data['ticket_medio']

    @property
    def receita_media_diaria(self):
        return self.data['receita_media_diaria']
    
    @property
    def media_por_consultor(self):
        return self.data['media_por_consultor']
    
    @property
    def maior_venda_mes(self):
        return self.data['maior_venda_mes']
    
    @property
    def delta_receita_total(self):
        if not self.ano and not self.mes:
            return 0

        return self.data['delta_receita_total']
    
    @property
    def delta_quantidade_clientes(self):
        if not self.ano and not self.mes:
            return 0
        
        return self.data['delta_quantidade_clientes']
    
    @property
    def delta_quantidade_produtos(self):
        if not self.ano and not self.mes:
            return 0

        return self.data['delta_quantidade_produtos']
    
    @property
    def delta_ticket_medio(self):
        if not self.ano and not self.mes:
            return 0

        return self.data['delta_ticket_medio']
    
    @property
    def delta_media_diaria(self):
        if not self.ano and not self.mes:
            return 0

        return self.data['delta_media_diaria']

    @property
    def delta_media_por_consultor(self):
        if not self.ano and self.mes:
            return 0

        return self.data['delta_media_por_consultor']
    
    @property
    def consultor_do_mes(self):
        return self.data['consultor_do_mes']
    
    @property
    def qtd_vendas_por_cnae(self):
        return pd.DataFrame(self.data['qtd_vendas_por_cnae'])

    @property
    def qtd_vendas_por_faturamento(self):
        return pd.DataFrame(self.data['qtd_vendas_por_faturamento'])
    
    @property
    def qtd_vendas_por_colaboradores(self):
        return pd.DataFrame(self.data['qtd_vendas_por_colaboradores'])
    
    @property
    def ufs(self):
        return self.data['ufs']
    
    @staticmethod
    def consultores():
        url = f'https://freecelapi-b44da8eb3c50.herokuapp.com/consultores'

        data = request('GET', url = url, headers=headers).json()

        return pd.DataFrame(data)