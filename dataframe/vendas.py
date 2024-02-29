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
            return dataframe[(dataframe['Ano'] == ano)]
        
        elif ano and mes:
            return dataframe[(dataframe['Ano'] == ano) & (dataframe['Mês'] == mes)]
        
        dataframe['Receita'] = dataframe['Receita'].astype(float)
        dataframe['Volume'] = dataframe['Volume'].astype(int)

        dataframe = dataframe.groupby('Data', as_index = False).sum(numeric_only = True)
        dataframe = dataframe[(dataframe['Data'].dt.month != now.month) | (dataframe['Data'].dt.year != now.year)]
        return dataframe

    @staticmethod
    def add_venda(token, cnpj, ddd, telefone, consultor, data, gestor, plano, quantidade_de_produtos, equipe, tipo, uf, email, valor_do_plano):
        if isinstance(valor_do_plano, str):
            valor_do_plano = float(valor_do_plano.replace(',', '.'))

        if ddd not in DDDS_valor_inteiro:
            valor_do_plano *= 0.3 

        valor_do_plano *= int(quantidade_de_produtos)

        authorization = {
            'Authorization': f'Bearer {token}'
        }

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

        response = request('PUT', url = vendas_url, json = params, headers = authorization)
        return response.status_code

    @staticmethod
    def remove_venda(id, token):
        authorization = {
            'Authorization': f'Bearer {token}'
        }
        response = request('DELETE', url = vendas_url, headers = authorization, json = { 'id': id })
        return response.status_code
    
    def __formatar_dados__(self):
        dataframe = self.__get_data__()

        dataframe.rename(
            columns = {
                'id': 'ID', 
                'cnpj': 'CNPJ', 
                'plano': 'Plano', 
                'tipo': 'Tipo', 
                'quantidade_de_produtos': 'Volume', 
                'valor_do_plano': 'Preço', 
                'valor_acumulado': 'Receita', 
                'consultor': 'Consultor', 
                'cep': 'CEP', 
                'uf': 'UF', 
                'municipio': 'Município', 
                'bairro': 'Bairro', 
                'telefone': 'Telefone', 
                'email': 'Email', 
                'ano': 'Ano',
                'mês': 'Mês', 
                'data': 'Data',
                'revenda': 'Equipe', 
                'gestor': 'Gestor', 
                'cnae': 'CNAE', 
                'faturamento': 'Faturamento', 
                'quadro_funcionarios': 'Quadro de Funcionários', 
                'capital_social': 'Capital', 
                'porte': 'Porte',
                'natureza_juridica': 'Natureza Jurídica', 
                'matriz': 'Matriz', 
                'situacao_cadastral': 'Situação Cadastral', 
                'regime_tributario': 'Regime Tributário'
            }, 
            inplace = True
        )
        
        dataframe['CNPJ'] = dataframe['CNPJ'].apply(lambda cnpj: formatar_cnpj(cnpj))
        dataframe['Telefone'] = dataframe['Telefone'].apply(lambda telefone: formatar_telefone(telefone))
        dataframe[['Matriz', 'Porte', 'Capital', 'Situação Cadastral', 'CEP']] = dataframe[
            ['Matriz', 'Porte', 'Capital', 'Situação Cadastral', 'CEP']
        ].map(remover_ponto)
        dataframe['Data'] = pd.to_datetime(dataframe['Data'], unit = 'ms')

        return dataframe[order]

    def __get_data__(self):
        vendas = pd.read_excel('dataframe/dataframe/Vendas concluídas.xlsx').astype(str)
        vendas.replace({
            'NaN': 'Não Informado',
            'nan': 'Não Informado',
            'UNDEFINED': 'Não Informado'
        }, inplace = True)

        return vendas