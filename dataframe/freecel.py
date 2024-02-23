from requests import request
import pandas as pd
from typing import Optional
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

load_dotenv()

TOKEN = getenv('tokenFreecel')

headers = {
    'Authorization': f'Bearer {TOKEN}'
}

class Stats:
    def __init__(self, ano=None, mes=None):
        self.ano = ano
        self.mes = mes
        self.data = self._get_data()

    def _get_data(self):
        params = {"ano": self.ano, "mes": self.mes}
        url = 'https://freecelapi-b44da8eb3c50.herokuapp.com/stats'
        response = request('GET', url, params=params, headers={'Authorization': f'Bearer {TOKEN}'})
        return response.json() if response.status_code == 200 else {}

    @staticmethod
    def vendas(ano=None, mes=None, groupby=None):
        url = 'https://freecelapi-b44da8eb3c50.herokuapp.com/vendas'
        params = {"ano": ano, "mes": mes}
        data = request('GET', url, headers={'Authorization': f'Bearer {TOKEN}'}, params=params).json()
        vendas = pd.DataFrame(data)
        vendas['data'] = pd.to_datetime(vendas['data'], unit='ms')

        if groupby:
            now = datetime.now()
            vendas = vendas.groupby('data', as_index=False).sum()
            vendas = vendas[(vendas['data'].dt.month != now.month) | (vendas['data'].dt.year != now.year)]

        vendas.replace(['NaN', 'UNDEFINED'], 'Não Informado', inplace=True)
        return vendas.sort_values(by='data', ascending=False)

    @property
    def receita_total(self):
        return self.data.get('receita_total', 0)

    @property
    def quantidade_vendida(self):
        return self.data.get('quantidade_vendida', 0)

    @property
    def quantidade_clientes(self):
        return self.data.get('quantidade_clientes', 0)

    @property 
    def ticket_medio(self):
        return self.data.get('ticket_medio', 0)

    @property
    def receita_media_diaria(self):
        return self.data.get('receita_media_diaria', 0)

    @property
    def media_por_consultor(self):
        return self.data.get('media_por_consultor', 0)

    @property
    def maior_venda_mes(self):
        return self.data.get('maior_venda_mes', 0)

    @property
    def delta_receita_total(self):
        return self.data.get('delta_receita_total', 0)

    @property
    def delta_quantidade_clientes(self):
        return self.data.get('delta_quantidade_clientes', 0)

    @property
    def delta_quantidade_produtos(self):
        return self.data.get('delta_quantidade_produtos', 0)

    @property
    def delta_ticket_medio(self):
        return self.data.get('delta_ticket_medio', 0)

    @property
    def delta_media_diaria(self):
        return self.data.get('delta_media_diaria', 0)

    @property
    def delta_media_por_consultor(self):
        return self.data.get('delta_media_por_consultor', 0)

    @property
    def consultor_do_mes(self):
        return self.data.get('consultor_do_mes')

    @property
    def qtd_vendas_por_cnae(self):
        return pd.DataFrame(self.data.get('qtd_vendas_por_cnae', {}))

    @property
    def qtd_vendas_por_faturamento(self):
        return pd.DataFrame(self.data.get('qtd_vendas_por_faturamento', {}))

    @property
    def qtd_vendas_por_colaboradores(self):
        return pd.DataFrame(self.data.get('qtd_vendas_por_colaboradores', {}))

    @property
    def ufs(self):
        return self.data.get('ufs', [])

    @staticmethod
    def consultores():
        url = 'https://freecelapi-b44da8eb3c50.herokuapp.com/consultores'
        data = request('GET', url, headers={'Authorization': f'Bearer {TOKEN}'}).json()

        nomes_consultores = [consultor['nome'] for consultor in data]
        return nomes_consultores
