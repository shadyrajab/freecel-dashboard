from typing import Optional

import pandas as pd
from requests import request

from utils.utils import consultores_url, headers, produtos_url, stats_url


class Stats:
    def __init__(self, ano: Optional[int] = None, mes: Optional[str] = None):
        self.ano = ano
        self.mes = mes
        self.data = self.__get_data__()

    def __getitem__(self, key):
        return self.data.get(key, 0)

    @property
    def dates(self):
        return self["dates"]

    @property
    def receita(self):
        return self["receita"]

    @property
    def volume(self):
        return self["volume"]

    @property
    def clientes(self):
        return self["clientes"]

    @property
    def ticket_medio(self):
        return self["ticket_medio"]

    @property
    def receita_media(self):
        return self["receita_media"]

    @property
    def media_consultor_geral(self):
        return self["media_consultor_geral"]

    @property
    def media_consultor_altas(self):
        return self["media_consultor_altas"]

    @property
    def media_consultor_migracao(self):
        return self["media_consultor_migracao"]

    @property
    def media_consultor_fixa(self):
        return self["media_consultor_fixa"]

    @property
    def media_consultor_avancada(self):
        return self["media_consultor_avancada"]

    @property
    def media_consultor_vvn(self):
        return self["media_consultor_vvn"]

    @property
    def media_consultor_portabilidade(self):
        return self["media_consultor_portabilidade"]

    @property
    def delta_receita(self):
        return self["delta_receita"]

    @property
    def delta_clientes(self):
        return self["delta_clientes"]

    @property
    def delta_volume(self):
        return self["delta_volume"]

    @property
    def delta_ticket_medio(self):
        return self["delta_ticket_medio"]

    @property
    def delta_receita_media(self):
        return self["delta_receita_media"]

    @property
    def delta_media_consultor_geral(self):
        return self["delta_media_consultor_geral"]

    @property
    def ufs(self):
        return self["ufs"]

    @staticmethod
    def consultores():
        data = request("GET", url=consultores_url, headers=headers).json()

        nomes_consultores = [consultor["nome"] for consultor in data]
        return nomes_consultores

    @staticmethod
    def produtos():
        data = request("GET", url=produtos_url, headers=headers).json()
        return pd.DataFrame(data)

    def __get_data__(self):
        params = {"ano": self.ano, "mes": self.mes}
        data = request("GET", url=stats_url, params=params, headers=headers).json()
        return data
