from requests import request
import pandas as pd
from typing import Optional
from utils.utils import headers, rankings_url, formatar_nome

class Rankings:
    def __init__(self, ano: Optional[int] = None, mes: Optional[str] = None) -> pd.DataFrame:
        self.ano = ano
        self.mes = mes
        self.data = self.__get_data()

    def __getitem__(self, key):
        funcs = {
            'consultores_geral': self.consultores_geral,
            'consultores_altas': self.consultores_altas,
            'consultores_fixa': self.consultores_fixa,
            'consultores_migracao': self.consultores_migracao,
            'consultores_portabilidade': self.consultores_portabilidade,
            'consultores_avancada': self.consultores_avancada
            # 'consultores_vvn': self.consultores_vvn
        }

        if key in funcs:
            return funcs[key]
        
        return pd.DataFrame(self.data.get(key))
    
    @property
    def consultores_geral(self):
        return self.__get_ranking('consultores_geral')
    
    @property
    def consultores_altas(self):
        return self.__get_ranking('consultores_altas')
    
    @property
    def consultores_fixa(self):
        return self.__get_ranking('consultores_fixa')
    
    @property
    def consultores_migracao(self):
        return self.__get_ranking('consultores_migracao')
    
    @property
    def consultores_portabilidade(self):
        return self.__get_ranking('consultores_portabilidade')
    
    @property
    def consultores_avancada(self):
        return self.__get_ranking('consultores_avancada')
    
    @property
    def consultores_vvn(self):
        return self.__get_ranking('consultores_vvn')

    @property
    def geral(self):
        return self['geral']
    
    @property
    def produtos(self):
        return self['produtos']
    
    @property
    def altas(self):
        return self['altas']
    
    @property
    def migracao(self):
        return self['migracao']
    
    @property
    def fixa(self):
        return self['fixa']

    @property
    def avancada(self):
        return self['avancada']
    
    @property
    def vvn(self):
        return self['vvn']
    
    @property
    def planos(self):
        return self['planos']
    
    @property
    def portabilidade(self):
        return self['portabilidade']
    
    def __get_data(self):
        params = { "ano": self.ano, "mes": self.mes }
        data = request('GET', url = rankings_url, params = params, headers = headers).json()
        return data
    
    def __get_ranking(self, name):
        ranking_consultores = pd.DataFrame(self.data.get(name))
        ranking_consultores.rename(columns = {
            'receita': 'Receita',
            'consultor': 'Consultor',
            'volume': 'Volume',
            'volume_media': 'Volume Média',
            'clientes': 'Clientes',
            'ticket_medio': 'Ticket Médio',
            'receita_media': 'Receita Média',
            'clientes_media': 'Clientes Média'
        }, inplace=True)
        ranking_consultores['Consultor'] = ranking_consultores['Consultor'].apply(lambda n: formatar_nome(n))
        return ranking_consultores
