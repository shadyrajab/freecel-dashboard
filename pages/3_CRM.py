import streamlit as st
import pandas as pd 
import re
from requests import request

url = 'https://freecelapi-b44da8eb3c50.herokuapp.com/crm'
response = request('GET', url = url).json()

df = pd.DataFrame(response)

def formatar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    cnpj = cnpj.zfill(14)
    cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    
    return cnpj_formatado

df.drop(axis = 1, 
    columns = {
        'Pedido Vinculado',
        'Usuário ADM',
        'Revisão',
        'Item',
        'Data Instalação',
        'Período',
        'Cidade Instalação',
        'Estado Instalação',
        'Rpon',
        'Instância',
        'Consultor na Operadora',
        'Etapa Item'
    }, 
    inplace = True
)

df = df.astype(str)
df['Cpf Cnpj'] = df['Cpf Cnpj'].apply(lambda n: formatar_cnpj(n))
st.dataframe(df)