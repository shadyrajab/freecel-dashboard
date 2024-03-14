from typing import Optional

import pandas as pd
from requests import request

from utils.utils import formatar_nome, headers, rankings_url


class Rankings:
    def __init__(
        self, ano: Optional[int] = None, mes: Optional[str] = None
    ) -> pd.DataFrame:
        self.ano = ano
        self.mes = mes
        self.data = self.__get_data()

    def __getitem__(self, key):
        ranking = pd.DataFrame(self.data.get(key))
        if ranking.shape[0] == 0:
            return pd.DataFrame(columns=["consultor", "receita", "volume", "clientes"])

        return ranking

    @property
    def geral(self):
        return self["geral"]

    @property
    def produtos(self):
        return self["produtos"]

    @property
    def altas(self):
        return self["altas"]

    @property
    def migracao(self):
        return self["migracao"]

    @property
    def fixa(self):
        return self["fixa"]

    @property
    def avancada(self):
        return self["avancada"]

    @property
    def vvn(self):
        return self["vvn"]

    @property
    def planos(self):
        return self["planos"]

    @property
    def portabilidade(self):
        return self["portabilidade"]

    @property
    def full_ranking(self):
        altas_e_portabilidade = pd.merge(
            self["altas"],
            self["portabilidade"],
            on="consultor",
            suffixes=("_df1", "_df2"),
            how="outer",
        ).fillna(0)
        altas_e_portabilidade["volume"] = (
            altas_e_portabilidade["volume_df1"] + altas_e_portabilidade["volume_df2"]
        )
        altas_e_portabilidade["receita"] = (
            altas_e_portabilidade["receita_df1"] + altas_e_portabilidade["receita_df2"]
        )
        altas_e_portabilidade.drop(
            [
                "clientes_df1",
                "clientes_df2",
                "receita_df1",
                "receita_df2",
                "volume_df1",
                "volume_df2",
            ],
            axis=1,
            inplace=True,
        )

        altas_e_portabilidade = altas_e_portabilidade.rename(
            columns={"volume": "Volume Altas", "receita": "Receita Altas"}
        )
        geral = (
            self["geral"]
            .rename(columns={"volume": "Volume Total", "receita": "Receita Total"})
            .drop(columns=["clientes"])
        )
        vvn = (
            self["vvn"]
            .rename(columns={"volume": "Volume VVN", "receita": "Receita VVN"})
            .drop(columns=["clientes"])
        )
        avancada = (
            self["avancada"]
            .rename(
                columns={"volume": "Volume Avançada", "receita": "Receita Avançada"}
            )
            .drop(columns=["clientes"])
        )
        migracao = (
            self["migracao"]
            .rename(
                columns={
                    "volume": "Volume Migração Pré-Pós",
                    "receita": "Receita Migração Pré-Pós",
                }
            )
            .drop(columns=["clientes"])
        )
        fixa = (
            self["fixa"]
            .rename(columns={"volume": "Volume Fixa", "receita": "Receita Fixa"})
            .drop(columns=["clientes"])
        )

        altas_geral = pd.merge(
            altas_e_portabilidade, geral, on="consultor", how="outer"
        )
        avancada_vvn = pd.merge(vvn, avancada, on="consultor", how="outer")
        mig_fix = pd.merge(migracao, fixa, on="consultor", how="outer")

        merged_df = pd.merge(altas_geral, avancada_vvn, on="consultor", how="outer")
        merged_df = pd.merge(merged_df, mig_fix, on="consultor", how="outer")
        merged_df["consultor"] = merged_df["consultor"].apply(
            lambda n: formatar_nome(n)
        )
        merged_df.set_index("consultor", inplace=True)
        merged_df.loc["Total"] = merged_df.sum(axis=0, numeric_only=True)
        merged_df.reset_index(inplace=True)

        return merged_df.rename(columns={"consultor": "Consultor"})

    def __get_data(self):
        params = {"ano": self.ano, "mes": self.mes}
        data = request("GET", url=rankings_url, params=params, headers=headers).json()
        return data
