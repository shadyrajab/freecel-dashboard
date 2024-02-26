from requests import request
import pandas as pd
from typing import Optional
from datetime import datetime
from utils.utils import (
    formatar_cnpj, 
    formatar_telefone, 
    remover_ponto, 
    order, 
    DDDS_valor_inteiro,
    vendas_url,
    headers
)

class Vendas:
    def __init__(self, ano: Optional[int] = None, mes: Optional[str] = None) -> pd.DataFrame:
        self.ano = ano
        self.mes = mes
        self.data = self.__formatar_dados__()

    def vendas_by_data(self, ano: Optional[int] = None, mes: Optional[str] = None, group: Optional[bool]= None):
        now = datetime.now()
        dataframe = self.data

        if group:
            return dataframe
        
        if ano and mes == 'Todos':
            return dataframe[(dataframe['ano'] == int(ano))]
        
        elif ano and mes:
            return dataframe[(dataframe['ano'] == int(ano)) & (dataframe['mês'] == mes)]

        dataframe = dataframe.groupby('data', as_index = False).sum(numeric_only = True)
        dataframe = dataframe[(dataframe['data'].dt.month != now.month) | (dataframe['data'].dt.year != now.year)]
        return dataframe

    @staticmethod
    def add_venda(cnpj, ddd, telefone, consultor, data, gestor, plano, quantidade_de_produtos, equipe, tipo, uf, email, valor_do_plano):
        if isinstance(valor_do_plano, str):
            valor_do_plano = float(valor_do_plano.replace(',', '.'))

        if ddd not in DDDS_valor_inteiro:
            valor_do_plano *= 0.3 

        valor_do_plano *= int(quantidade_de_produtos)

        params = {
            "cnpj": cnpj,
            "telefone": telefone,
            "consultor": consultor,
            "data": str(datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')),
            "gestor": gestor,
            "plano": plano,
            "quantidade_de_produtos": quantidade_de_produtos,
            "revenda": equipe,
            "tipo": tipo,
            "uf": uf,
            "valor_do_plano": valor_do_plano,
            "email": email
        }

        response = request('PUT', url = vendas_url, json = params, headers = headers)
        return response.status_code

    @staticmethod
    def remove_venda(id):
        response = request('DELETE', url = vendas_url, headers = headers, json = { 'id': id })
        return response.status_code
    
    def __formatar_dados__(self):
        dataframe = self.__get_data__()
        dataframe['cnpj'] = dataframe['cnpj'].apply(lambda cnpj: formatar_cnpj(cnpj))
        dataframe['telefone'] = dataframe['telefone'].apply(lambda telefone: formatar_telefone(telefone))
        dataframe[['matriz', 'porte', 'capital_social', 'situacao_cadastral', 'cep']] = dataframe[
            ['matriz', 'porte', 'capital_social', 'situacao_cadastral', 'cep']
        ].map(remover_ponto)

        return dataframe[order]

    def __get_data__(self):
        data = request('GET', url = vendas_url, headers = headers).json()
        vendas = pd.DataFrame(data)
        vendas['data'] = pd.to_datetime(vendas['data'], unit = 'ms')

        vendas.replace(['NaN', 'UNDEFINED'], 'Não Informado', inplace = True)

        return vendas.sort_values(by = 'data', ascending = False)