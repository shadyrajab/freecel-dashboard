from requests import request
import pandas as pd
from typing import Optional
from utils.utils import headers, rankings_url

class Rankings:
    def __init__(self, ano: Optional[int] = None, mes: Optional[str] = None) -> pd.DataFrame:
        self.ano = ano
        self.mes = mes
        self.data = self.__get_data__()

    @property
    def ranking_consultores(self):
        return pd.DataFrame(self.data.get('ranking_consultores'))
    
    @property
    def ranking_produtos(self):
        return pd.DataFrame(self.data.get('ranking_produtos'))
    
    @property
    def ranking_altas(self):
        return pd.DataFrame(self.data.get('ranking_altas'))
    
    @property
    def ranking_migracao(self):
        return pd.DataFrame(self.data.get('ranking_migracao'))
    
    @property
    def ranking_fixa(self):
        return pd.DataFrame(self.data.get('ranking_fixa'))

    @property
    def ranking_avancada(self):
        return pd.DataFrame(self.data.get('ranking_avancada'))
    
    @property
    def ranking_vvn(self):
        return pd.DataFrame(self.data.get('ranking_vvn'))
    
    @property
    def ranking_planos(self):
        return pd.DataFrame(self.data.get('ranking_planos'))
    
    @property
    def ranking_portabilidade(self):
        return pd.DataFrame(self.data.get('ranking_portabilidade'))
    
    def __get_data__(self):
        params = { "ano": self.ano, "mes": self.mes }
        data = request('GET', url = rankings_url, params = params, headers = headers).json()
        return data