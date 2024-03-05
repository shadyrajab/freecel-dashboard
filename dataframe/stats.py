from requests import request
import pandas as pd
from typing import Optional
from utils.utils import headers, stats_url, consultores_url, produtos_url

class Stats:
    def __init__(self, ano: Optional[int] = None, mes: Optional[str] = None):
        self.ano = ano
        self.mes = mes
        self.data = self.__get_data__()

    @property
    def dates(self):
        return self.data.get('dates')
    
    @property
    def receita_total(self):
        return self.data.get('receita', 0)

    @property
    def quantidade_vendida(self):
        return self.data.get('volume', 0)

    @property
    def quantidade_clientes(self):
        return self.data.get('clientes', 0)

    @property 
    def ticket_medio(self):
        return self.data.get('ticket_medio', 0)

    @property
    def receita_media_diaria(self):
        return self.data.get('receita_media', 0)

    @property
    def media_por_consultor_geral(self):
        return self.data.get('media_consultor_geral', 0)
    
    @property
    def media_por_consultor_altas(self):
        return self.data.get('media_consultor_altas', 0)
    
    @property
    def media_por_consultor_migracao(self):
        return self.data.get('media_consultor_migracao', 0)
    
    @property
    def media_por_consultor_fixa(self):
        return self.data.get('media_consultor_fixa', 0)
    
    @property
    def media_por_consultor_avancada(self):
        return self.data.get('media_consultor_avancada', 0)
    
    @property
    def media_por_consultor_vvn(self):
        return self.data.get('media_consultor_vvn', 0)
    
    @property
    def media_por_consultor_portabilidade(self):
        return self.data.get('media_consultor_portabilidade', 0)

    @property
    def delta_receita_total(self):
        return self.data.get('delta_receita', 0)

    @property
    def delta_quantidade_clientes(self):
        return self.data.get('delta_clientes', 0)

    @property
    def delta_quantidade_produtos(self):
        return self.data.get('delta_volume', 0)

    @property
    def delta_ticket_medio(self):
        return self.data.get('delta_ticket_medio', 0)

    @property
    def delta_media_diaria(self):
        return self.data.get('delta_receita_media', 0)

    @property
    def delta_media_por_consultor(self):
        return self.data.get('delta_media_consultor_geral', 0)

    @property
    def ufs(self):
        return self.data.get('ufs')

    @staticmethod
    def consultores():
        data = request('GET', url = consultores_url, headers = headers).json()

        nomes_consultores = [consultor['nome'] for consultor in data]
        return nomes_consultores
    
    @staticmethod
    def produtos():
        data = request('GET', url = produtos_url, headers = headers).json()
        return pd.DataFrame(data)
    
    def __get_data__(self):
        params = { "ano": self.ano, "mes": self.mes }
        data = request('GET', url = stats_url, params = params, headers = headers).json()
        return data