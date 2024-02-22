from requests import request
import pandas as pd
from typing import Optional
from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv('tokenFreecel')

class Ranking:
    def __init__(self, ano: Optional[int] = None, mes: Optional[str] = None) -> pd.DataFrame:
        self.ano = ano
        self.mes = mes
        self.__get_data__(ano, mes)

    def __get_data__(self, ano: Optional[int] = None, mes: Optional[str] = None):
        url = f'https://freecelapi-b44da8eb3c50.herokuapp.com/rankings'
        params = {
            "ano": ano,
            "mes": mes,
        }

        headers = {
            'Authorization': f'Bearer {TOKEN}'
        }
        
        data = request('GET', url = url, params=params, headers=headers).json()

        self.ranking_consultores = pd.DataFrame(data['ranking_consultores'])
        self.ranking_produtos = pd.DataFrame(data['ranking_produtos'])
        self.ranking_altas = pd.DataFrame(data['ranking_altas'])
        self.ranking_migracao = pd.DataFrame(data['ranking_migracao'])
        self.ranking_fixa = pd.DataFrame(data['ranking_fixa'])
        self.ranking_avancada = pd.DataFrame(data['ranking_avancada'])
        self.ranking_vvn = pd.DataFrame(data['ranking_vvn'])

    def ranking_geral(self):
        def renomear_colunas(dataframe, nome_do_ranking):
            novo_nome_colunas = {
                'valor_acumulado': f'valor_acumulado_{nome_do_ranking}',
                'quantidade_de_produtos': f'quantidade_de_produtos_{nome_do_ranking}',
                'quantidade_de_vendas': f'quantidade_de_vendas_{nome_do_ranking}'
            }
            return dataframe.rename(columns=novo_nome_colunas)
        
        ranking_consultores = renomear_colunas(self.ranking_consultores, 'consultores')
        ranking_altas = renomear_colunas(self.ranking_altas, 'altas')
        ranking_migracao = renomear_colunas(self.ranking_migracao, 'migracao')
        ranking_fixa = renomear_colunas(self.ranking_fixa, 'fixa')
        ranking_avancada = renomear_colunas(self.ranking_avancada, 'avancada')
        ranking_vvn = renomear_colunas(self.ranking_vvn, 'vvn')

        merged_df = pd.merge(ranking_consultores, ranking_altas, on='consultor', how='outer')
        merged_df = pd.merge(merged_df, ranking_migracao, on='consultor', how='outer')
        merged_df = pd.merge(merged_df, ranking_fixa, on='consultor', how='outer')
        merged_df = pd.merge(merged_df, ranking_avancada, on='consultor', how='outer')
        if len(ranking_vvn.columns):
            merged_df = pd.merge(merged_df, ranking_vvn, on='consultor', how='outer')

        merged_df.fillna(0, inplace = True)

        merged_df.rename(
            columns = {
                'quantidade_de_produtos_consultores': 'Volume',
                'valor_acumulado_consultores': 'Receita',
                'quantidade_de_vendas_consultores': 'Clientes',
                'quantidade_de_produtos_altas': 'Volume',
                'valor_acumulado_altas': 'Receita',
                'quantidade_de_produtos_migracao': 'Volume',
                'valor_acumulado_migracao': 'Receita',
                'quantidade_de_produtos_fixa': 'Volume',
                'valor_acumulado_fixa': 'Receita',
                'quantidade_de_produtos_avancada': 'Volume',
                'valor_acumulado_avancada': 'Receita',



            }, inplace = True
        )  

        merged_df.drop(['quantidade_de_vendas_avancada', 'quantidade_de_vendas_fixa','quantidade_de_vendas_migracao','quantidade_de_vendas_altas'], axis = 1, inplace = True)
        merged_df.set_index('consultor', inplace = True)

        return merged_df

