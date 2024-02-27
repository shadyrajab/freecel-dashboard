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
    def media_por_consultor_geral(self):
        return self.data.get('media_por_consultor_geral', 0)
    
    @property
    def media_por_consultor_altas(self):
        return self.data.get('media_por_consultor_altas', 0)
    
    @property
    def media_por_consultor_migracao(self):
        return self.data.get('media_por_consultor_migracao', 0)
    
    @property
    def media_por_consultor_fixa(self):
        return self.data.get('media_por_consultor_fixa', 0)
    
    @property
    def media_por_consultor_avancada(self):
        return self.data.get('media_por_consultor_avancada', 0)
    
    @property
    def media_por_consultor_vvn(self):
        return self.data.get('media_por_consultor_vvn', 0)

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
        return pd.DataFrame(self.data.get('qtd_vendas_por_cnae'))

    @property
    def qtd_vendas_por_faturamento(self):
        return pd.DataFrame(self.data.get('qtd_vendas_por_faturamento'))

    @property
    def qtd_vendas_por_colaboradores(self):
        return pd.DataFrame(self.data.get('qtd_vendas_por_colaboradores'))

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