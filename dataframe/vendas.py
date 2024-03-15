from datetime import datetime
from typing import Optional

import pandas as pd
from requests import request

from utils.utils import formatar_cnpj, formatar_telefone, headers, order, vendas_url


class Vendas:
    def __init__(
        self,
        ano: Optional[int] = None,
        mes: Optional[str] = None,
        cnpj: Optional[str] = None,
        n_pedido: Optional[str] = None,
    ) -> pd.DataFrame:
        self.ano = ano
        self.mes = mes
        self.cnpj = cnpj
        self.n_pedido = n_pedido
        self.data = self.__formatar_dados()

    def vendas_by_data(
        self,
        ano: Optional[int] = None,
        mes: Optional[str] = None,
        group: Optional[bool] = None,
    ):
        now = datetime.now()
        dataframe = self.data

        if group:
            return dataframe

        if ano and mes == "Todos":
            return dataframe[(dataframe["Ano"] == int(ano))]

        elif ano and mes:
            return dataframe[(dataframe["Ano"] == int(ano)) & (dataframe["Mês"] == mes)]

        dataframe = dataframe.groupby("Data", as_index=False).sum(numeric_only=True)
        dataframe = dataframe[
            (dataframe["Data"].dt.month != now.month)
            | (dataframe["Data"].dt.year != now.year)
        ]
        return dataframe

    @staticmethod
    def add_venda(
        token,
        cnpj,
        telefone,
        consultor,
        data,
        gestor,
        plano,
        volume,
        equipe,
        tipo,
        email,
        ja_cliente,
        preco: Optional[float] = 0,
    ):
        authorization = {"Authorization": f"Bearer {token}"}

        params = {
            "cnpj": cnpj,
            "telefone": telefone,
            "consultor": consultor,
            "data": str(datetime.strptime(str(data), "%Y-%m-%d").strftime("%d-%m-%Y")),
            "gestor": gestor,
            "plano": plano,
            "volume": volume,
            "equipe": equipe,
            "tipo": tipo,
            "email": email,
            "ja_cliente": ja_cliente,
            "preco": preco,
        }

        response = request("PUT", url=vendas_url, json=params, headers=authorization)
        return response.status_code

    @staticmethod
    def remove_venda(id, token):
        authorization = {"Authorization": f"Bearer {token}"}
        response = request(
            "DELETE", url=vendas_url, headers=authorization, json={"id": id}
        )
        return response.status_code

    def __formatar_dados(self):
        dataframe = self.__get_data()

        dataframe.rename(
            columns={
                "id": "ID",
                "cnpj": "CNPJ",
                "plano": "Plano",
                "tipo": "Tipo",
                "volume": "Volume",
                "preco": "Preço",
                "receita": "Receita",
                "consultor": "Consultor",
                "cep": "CEP",
                "uf": "UF",
                "municipio": "Município",
                "bairro": "Bairro",
                "telefone": "Telefone",
                "email": "Email",
                "ano": "Ano",
                "mes": "Mês",
                "data": "Data",
                "equipe": "Equipe",
                "gestor": "Gestor",
                "cnae": "CNAE",
                "faturamento": "Faturamento",
                "quadro_funcionarios": "Quadro de Funcionários",
                "capital_social": "Capital",
                "porte": "Porte",
                "natureza_juridica": "Natureza Jurídica",
                "matriz": "Matriz",
                "regime_tributario": "Regime Tributário",
                "adabas": "ADABAS",
                "numero_pedido": "Número do Pedido",
                "ja_cliente": "Já Cliente?",
                "status": "Status",
            },
            inplace=True,
        )

        dataframe["CNPJ"] = dataframe["CNPJ"].apply(lambda cnpj: formatar_cnpj(cnpj))
        dataframe["Telefone"] = dataframe["Telefone"].apply(
            lambda telefone: formatar_telefone(telefone)
        )
        dataframe["Data"] = pd.to_datetime(dataframe["Data"], unit="ms")

        return dataframe[order].sort_values(by="Data", ascending=False)

    def __get_data(self):
        data = request("GET", url=vendas_url, headers=headers).json()
        vendas = pd.DataFrame(data)
        vendas.replace(
            {
                "NaN": "Não Informado",
                "nan": "Não Informado",
                "UNDEFINED": "Não Informado",
                None: "Não Informado",
            },
            inplace=True,
        )
        return vendas
