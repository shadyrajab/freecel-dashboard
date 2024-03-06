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
        return pd.DataFrame(self.data.get(key))

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
    