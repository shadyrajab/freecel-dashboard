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