import pandas as pd
from typing import Optional
from utils.utils import __filter_by__, months

class Consultor:
    def __init__(self, nome: str, ano: Optional[int] = None, mes: Optional[str] = None):
        self.nome = nome
        self.ano = ano
        self.mes = mes
        self.data = self.__get_data__()
    
    def filter_by(self, ano: Optional[int] = None, mes: Optional[str] = None, consultor: Optional[str] = None):
        return __filter_by__(dataframe = self.data, ano = ano ,mes = mes, consultor = consultor)
    
    @property
    def dates(self):
        dates = []
        for year in self.years():
            dates.append(
                {
                    f"{year}": self.months(year)
                }
            )
        return dates
    
    def years(self):
        return list(self.data['ano'].unique())
    
    def months(self, ano):
        return list(self.filter_by(ano)['mês'].unique())
    
    def receita_total(self, ano, mes):
        return self.filter_by(ano, mes, self.nome)['valor_acumulado'].sum()
    
    @property
    def meses_trabalhados(self):
        meses_trabalhados = self.data['data'].nunique()

        return meses_trabalhados
    
    @property
    def ranking_planos(self):
        quantidade_de_vendas = self.filter_by(self.ano, self.mes, self.nome)['tipo'].value_counts().reset_index()
        quantidade_de_vendas.columns = ['tipo', 'quantidade_de_vendas']

        ranking_produtos = self.filter_by(self.ano, self.mes).groupby('tipo', as_index = False).sum(numeric_only = True)
        ranking_produtos.drop(['ano', 'valor_do_plano', 'id'], axis = 1, inplace = True)

        return pd.merge(ranking_produtos, quantidade_de_vendas, on = 'tipo')
    
    @property
    def ranking_produtos(self):
        quantidade_de_vendas = self.filter_by(self.ano, self.mes, self.nome)['plano'].value_counts().reset_index()
        quantidade_de_vendas.columns = ['plano', 'quantidade_de_vendas']

        ranking_planos = self.filter_by(self.ano, self.mes).groupby('plano', as_index = False).sum(numeric_only = True)
        ranking_planos.drop(['ano', 'valor_do_plano', 'id'], axis = 1, inplace = True)

        return pd.merge(ranking_planos, quantidade_de_vendas, on = 'plano')
    
    def delta_quantidade_clientes(self, ano = None, mes = None ):
        return self.__calculate_delta_metric__(self.quantidade_clientes, ano, mes)
    
    def delta_quantidade_produtos(self, ano = None, mes = None):
        return self.__calculate_delta_metric__(self.quantidade_vendida, ano, mes)
    
    def delta_receita_total(self, ano = None, mes = None):
        return self.__calculate_delta_metric__(self.receita_total, ano, mes)
    
    def delta_ticket_medio(self, ano, mes = None):
        return self.__calculate_delta_metric__(self.ticket_medio, ano, mes)
    
    def delta_media_diaria(self, ano, mes):
        return self.__calculate_delta_metric__(self.receita_media_diaria, ano, mes)
    
    def quantidade_vendida(self, ano, mes):
        return self.filter_by(ano, mes, self.nome)['quantidade_de_produtos'].sum()
    
    def quantidade_clientes(self, ano, mes):
        return self.filter_by(ano, mes, self.nome).shape[0]
    
    def receita_media_diaria(self, ano, mes):
        return self.receita_total(ano, mes) / 22
    
    def quantidade_media_diaria(self, ano = None, mes = None):
        return self.quantidade_vendida(ano, mes) / 22
    
    @property
    def quantidade_media_mensal(self):
        return self.data.get('quantidade_media_mensal')
    
    def receita_media_mensal(self, ano = None, mes = None):
        receita_media_mensal = self.receita_total(ano, mes) / self.meses_trabalhados
        return receita_media_mensal
    
    def ticket_medio(self, ano = None, mes = None):
        ticket_medio = self.receita_total(ano, mes) / self.quantidade_clientes(ano, mes)

        return ticket_medio
    
    @property
    def vendas(self):
        dataframe = self.filter_by(self.ano, self.mes, self.nome)
        dataframe = dataframe.sort_values(
            by = 'data', ascending = False
        )

        dataframe['data'] = pd.to_datetime(dataframe['data'], unit='ms')
        return dataframe

    @property
    def groupby_data(self):
        dataframe = self.filter_by(self.ano, self.mes, self.nome)
        return dataframe.groupby('data', as_index = False).sum(numeric_only = True).sort_values(
            by = 'data', ascending = False
        )
    
    def __get_data__(self):
        df = pd.read_excel('dataframe/dataframe/Vendas concluídas.xlsx')
        df['data'] = pd.to_datetime(df['data'], unit = 'ms')
        return df
    
    def __get_media__(self, ano: Optional[int] = None, mes: Optional[str] = None, consultor: Optional[str] = None):
        dataframe = self.filter_by(ano, mes, consultor)
        consultores = dataframe['consultor'].nunique() # -> Quantidade de consultores
        media_por_consultor = dataframe['valor_acumulado'].sum() / consultores

        return media_por_consultor
    
    def __calculate_delta_metric__(self, metric_function, ano: Optional[int] = None, mes: Optional[str] = None) -> int:
        ano = int(ano)
        
        if ano == min(self.years()) and mes == None:
            return 0
        
        if ano == min(self.years()) and mes.lower() == 'janeiro':
            return 0
        
        if mes:
            mes = mes.capitalize()

            ano_delta = ano - 1 if mes == 'Janeiro' else ano
            index_mes_passado = months.index(mes) - 1
            mes_delta = months[index_mes_passado]

            return metric_function(ano, mes) - metric_function(ano_delta, mes_delta)
        else:
            ano_delta = ano - 1 if ano != min(self.years()) else ano
            return metric_function(ano) - metric_function(ano_delta)