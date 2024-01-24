import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np

df_fixa = pd.read_excel('dataframes/vendas concluidas - fixa - 2023 e 2022.xlsx')
df_movel = pd.read_excel('dataframes/vendas concluidas - movel - 2023 e 2022.xlsx')

df_movel.rename(columns={'QTD SERVIÇOS': 'QUANTIDADE DE PRODUTOS'}, inplace=True)

df_movel_2023 = df_movel[df_movel['ANO'] == 2023]
df_movel_2022 = df_movel[df_movel['ANO'] == 2022]

df_movel_2023 = df_movel_2023.groupby('MÊS').sum(numeric_only=True)
df_movel_2022 = df_movel_2022.groupby('MÊS').sum(numeric_only=True)

df_movel_2023 = df_movel_2023[['QUANTIDADE DE PRODUTOS', 'VALOR ACUMULADO']]
df_movel_2022 = df_movel_2022[['QUANTIDADE DE PRODUTOS', 'VALOR ACUMULADO']]

df_fixa_2023 = df_fixa[df_fixa['ANO'] == 2023]
df_fixa_2022 = df_fixa[df_fixa['ANO'] == 2022]

df_fixa_2023 = df_fixa_2023.groupby('MÊS').sum(numeric_only=True)
df_fixa_2022 = df_fixa_2022.groupby('MÊS').sum(numeric_only=True)

df_fixa_2023 = df_fixa_2023[['QUANTIDADE DE PRODUTOS', 'VALOR ACUMULADO']]
df_fixa_2022 = df_fixa_2022[['QUANTIDADE DE PRODUTOS', 'VALOR ACUMULADO']]

st.title('Análise de vendas da Freecel')
st.write('----------------------------')

st.write('Fixa, Avançada e VVN - 2023')
st.write('----------------------------')
st.dataframe(df_fixa_2023)

st.write('Fixa, Avançada e VVN - 2022')
st.write('----------------------------')
st.dataframe(df_fixa_2022)

st.write('Móvel e Migração - 2023')
st.write('----------------------------')
st.dataframe(df_movel_2023)

st.write('Móvel e Migração - 2022')
st.write('----------------------------')
st.dataframe(df_movel_2022)

st.sidebar.header('Filtros')