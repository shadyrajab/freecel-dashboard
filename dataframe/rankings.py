from requests import request
import pandas as pd
from typing import Optional
from utils.utils import headers, rankings_url, __filter_by__

class Rankings:
    def __init__(self, ano: Optional[int] = None, mes: Optional[str] = None) -> pd.DataFrame:
        self.ano = ano
        self.mes = mes
        self.data = self.__get_data__()

    def filter_by(self, ano: Optional[int] = None, mes: Optional[str] = None, tipo: Optional[str] = None):
        return __filter_by__(dataframe = self.data, ano = ano, mes = mes, tipo = tipo)
    
    @property
    def ranking_consultores(self):
        return self.__consultores__(self.ano, self.mes)
    
    @property
    def ranking_produtos(self):
        quantidade_de_vendas = self.filter_by(self.ano, self.mes)['tipo'].value_counts().reset_index()
        quantidade_de_vendas.columns = ['tipo', 'quantidade_de_vendas']

        ranking_produtos = self.filter_by(self.ano, self.mes).groupby('tipo', as_index = False).sum(numeric_only = True)
        ranking_produtos.drop(['ano', 'valor_do_plano', 'id'], axis = 1, inplace = True)

        return pd.merge(ranking_produtos, quantidade_de_vendas, on = 'tipo')
    
    @property
    def ranking_altas(self):
        return self.__consultores__(self.ano, self.mes, 'ALTAS')
    
    @property
    def ranking_migracao(self):
        return self.__consultores__(self.ano, self.mes, 'MIGRAÇÃO PRÉ-PÓS')
    
    @property
    def ranking_fixa(self):
        return self.__consultores__(self.ano, self.mes, 'FIXA')

    @property
    def ranking_avancada(self):
        return self.__consultores__(self.ano, self.mes, 'AVANÇADA')
    
    @property
    def ranking_vvn(self):
        return self.__consultores__(self.ano, self.mes, 'VVN')
    
    @property
    def ranking_planos(self):
        quantidade_de_vendas = self.filter_by(self.ano, self.mes)['plano'].value_counts().reset_index()
        quantidade_de_vendas.columns = ['plano', 'quantidade_de_vendas']

        ranking_planos = self.filter_by(self.ano, self.mes).groupby('plano', as_index = False).sum(numeric_only = True)
        ranking_planos.drop(['ano', 'valor_do_plano', 'id'], axis = 1, inplace = True)

        return pd.merge(ranking_planos, quantidade_de_vendas, on = 'plano')
    
    def __get_data__(self):
        data = pd.read_excel('dataframe/dataframe/Vendas concluídas.xlsx')
        return data
    
    def __consultores__(self, ano: Optional[int] = None, mes: Optional[str] = None, tipo: Optional[str] = None) -> pd.DataFrame:
        if tipo and tipo not in {'ALTAS', 'FIXA', 'AVANÇADA', 'VVN', 'MIGRAÇÃO PRÉ-PÓS'}:
            raise ValueError("O tipo de venda deve ser {'ALTAS', 'FIXA' | 'AVANÇADA' | 'VVN' | 'MIGRAÇÃO PRÉ-PÓS'}")
        
        quantidade_de_vendas = self.filter_by(ano, mes, tipo)['consultor'].value_counts().reset_index()
        quantidade_de_vendas.columns = ['consultor', 'quantidade_de_vendas']
        
        ranking_consultores = self.filter_by(ano, mes, tipo).groupby('consultor', as_index = False).sum(numeric_only = True)
        ranking_consultores.drop(['ano', 'valor_do_plano', 'id'], axis = 1, inplace = True)

        return pd.merge(ranking_consultores, quantidade_de_vendas, on = 'consultor')