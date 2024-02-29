import pandas as pd
from typing import Optional
from utils.utils import __filter_by__, months

class Stats:
    def __init__(self):
        self.data = self.__get_data__()

    def filter_by(self, ano: Optional[int] = None, mes: Optional[str] = None, tipo: Optional[str] = None):
        return __filter_by__(dataframe = self.data, ano = ano ,mes = mes, tipo = tipo)

    def years(self) -> list[int]:
        return list(self.data['ano'].unique())

    def months(self, ano) -> list[str]:
        return list(self.filter_by(ano)['mês'].unique())
    
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
    
    def receita_total(self, ano, mes):
        return self.filter_by(ano, mes)['valor_acumulado'].sum()

    def quantidade_vendida(self, ano, mes):
        return self.filter_by(ano, mes)['quantidade_de_produtos'].sum()

    def quantidade_clientes(self, ano, mes):
        return self.filter_by(ano, mes).shape[0]

    def ticket_medio(self, ano, mes):
        return self.receita_total(ano, mes) / self.quantidade_clientes(ano, mes)
    
    def receita_media_diaria(self, ano, mes):
        return self.receita_total(ano, mes) / 22
    
    def media_por_consultor_geral(self, ano, mes):
        return self.__get_media__(ano, mes)
    
    def media_por_consultor_altas(self, ano, mes):
        return self.__get_media__(ano, mes, 'ALTAS')
    
    def media_por_consultor_migracao(self, ano, mes):
        return self.__get_media__(ano, mes, 'MIGRAÇÃO PRÉ-PÓS')
    
    def media_por_consultor_fixa(self, ano, mes):
        return self.__get_media__(ano, mes, 'FIXA')
    
    def media_por_consultor_avancada(self, ano, mes):
        return self.__get_media__(ano, mes, 'AVANÇADA')
    
    def media_por_consultor_vvn(self, ano, mes):
        return self.__get_media__(ano, mes, 'VVN')
    
    def delta_receita_total(self, ano, mes):
        return self.__calculate_delta_metric__(self.receita_total, ano, mes)

    def delta_quantidade_clientes(self, ano, mes):
        return self.__calculate_delta_metric__(self.quantidade_clientes, ano, mes)

    def delta_quantidade_produtos(self, ano, mes):
        return self.__calculate_delta_metric__(self.quantidade_vendida, ano, mes)

    def delta_ticket_medio(self, ano, mes):
        return self.__calculate_delta_metric__(self.ticket_medio, ano, mes)

    def delta_media_diaria(self, ano, mes):
        return self.__calculate_delta_metric__(self.receita_media_diaria, ano, mes)

    def delta_media_por_consultor(self, ano, mes):
        return self.__calculate_delta_metric__(self.media_por_consultor_geral, ano, mes)

    @property
    def ufs(self):
        return self.data['UF'].unique().tolist()

    @property
    def consultores(self):
        return self.data['Consultor'].unique().tolist()
    
    @property
    def produtos(self):
        return self.data['Plano'].unique().tolist()
    
    def __get_data__(self):
        data = pd.read_excel('dataframe/dataframe/Vendas concluídas.xlsx')
        return data
    
    def __get_media__(self, ano: Optional[int] = None, mes: Optional[str] = None, tipo: Optional[str] = None):
        dataframe = self.filter_by(ano, mes, tipo)
        consultores: int = dataframe['consultor'].nunique() # -> Quantidade de consultores
        media_por_consultor: int = dataframe['valor_acumulado'].sum() / consultores

        return media_por_consultor
    
    def __calculate_delta_metric__(self, metric_function, ano: int = None, mes: str = None) -> int:
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