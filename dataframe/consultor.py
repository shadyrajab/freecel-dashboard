from typing import Optional

import pandas as pd
from requests import request

from utils.utils import consultores_url, headers


class Consultor:
    def __init__(self, nome: str, ano: Optional[int] = None, mes: Optional[str] = None):
        self.nome = nome
        self.ano = ano
        self.mes = mes
        self.data = self.__get_data__()

    @property
    def dates(self):
        return self.data.get("dates")

    @property
    def years(self):
        return self.vendas.get("ano").unique().tolist()

    @property
    def months(self):
        return self.vendas.get("mês").unique().tolist()

    @property
    def name(self):
        return self.data.get("name")

    @property
    def receita(self):
        return self.data.get("receita")

    @property
    def ranking_planos(self):
        return pd.DataFrame(self.data.get("ranking_planos"))

    @property
    def ranking_produtos(self):
        return pd.DataFrame(self.data.get("ranking_produtos"))

    @property
    def delta_clientes(self):
        return self.data.get("delta_clientes", 0)

    @property
    def delta_volume(self):
        return self.data.get("delta_volume", 0)

    @property
    def delta_receita(self):
        return self.data.get("delta_receita", 0)

    @property
    def delta_ticket_medio(self):
        return self.data.get("delta_ticket_medio", 0)

    @property
    def delta_receita_media(self):
        return self.data.get("delta_receita_media", 0)

    @property
    def volume(self):
        return self.data.get("volume")

    @property
    def clientes(self):
        return self.data.get("clientes")

    @property
    def receita_media(self):
        return self.data.get("receita_media")

    @property
    def volume_media(self):
        return self.data.get("volume_media")

    @property
    def delta_volume_media(self):
        return self.data.get("delta_volume_media")

    @property
    def ticket_medio(self):
        return self.data.get("ticket_medio")

    @property
    def vendas(self):
        dataframe = pd.DataFrame(self.data.get("vendas")).sort_values(
            by="data", ascending=False
        )

        dataframe["data"] = pd.to_datetime(dataframe["data"], unit="ms")
        return dataframe

    @property
    def groupby_data(self):
        return (
            self.vendas.groupby("data", as_index=False)
            .sum(numeric_only=True)
            .sort_values(by="data", ascending=False)
        )

    def __get_data__(self):
        params = {"ano": self.ano, "mes": self.mes, "display_vendas": True}
        data = request(
            "GET", url=consultores_url + self.nome, params=params, headers=headers
        ).json()
        return data
