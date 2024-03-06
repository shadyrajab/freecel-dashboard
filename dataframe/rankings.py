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
        ranking = pd.DataFrame(self.data.get(key))
        if ranking.shape[0] == 0:
            return pd.DataFrame(columns=['consultor', 'receita', 'volume', 'clientes'])
        
        return ranking

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
    
    @property
    def full_ranking(self):
        altas = self['altas'].rename(columns={'volume': 'Volume Altas', 'receita': 'Receita Altas'}).drop(columns=['clientes'])
        geral = self['geral'].rename(columns={'volume': 'Volume Total', 'receita': 'Receita Total'}).drop(columns=['clientes'])
        portabilidade = self['portabilidade'].rename(columns={'volume': 'Volume Portabilidade', 'receita': 'Receita Portabilidade'}).drop(columns=['clientes'])
        vvn = self['vvn'].rename(columns={'volume': 'Volume VVN', 'receita': 'Receita VVN'}).drop(columns=['clientes'])
        avancada = self['avancada'].rename(columns={'volume': 'Volume Avançada', 'receita': 'Receita Avançada'}).drop(columns=['clientes'])
        migracao = self['migracao'].rename(columns={'volume': 'Volume Migração Pré-Pós', 'receita': 'Receita Migração Pré-Pós'}).drop(columns=['clientes'])

        altas_geral = pd.merge(altas, geral, on='consultor', how='outer')
        port_vvn = pd.merge(vvn, portabilidade, on='consultor', how='outer')
        avanc_migr = pd.merge(avancada, migracao, on='consultor', how='outer')

        merged_df = pd.merge(altas_geral, port_vvn, on='consultor', how='outer')
        merged_df = pd.merge(merged_df, avanc_migr, on='consultor', how='outer')

        merged_df['consultor'] = merged_df['consultor'].apply(lambda n: formatar_nome(n))

        return merged_df.rename(columns={'consultor': 'Consultor'})

    
    def __get_data(self):
        params = { "ano": self.ano, "mes": self.mes }
        data = request('GET', url = rankings_url, params = params, headers = headers).json()
        return data
    