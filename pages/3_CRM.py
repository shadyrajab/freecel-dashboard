import streamlit as st
import pandas as pd 
import re

def formatar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    cnpj = cnpj.zfill(14)
    cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    
    return cnpj_formatado


df = pd.read_excel('dataframes/excel/crm 05-02.xlsx')
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