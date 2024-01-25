import streamlit as st
import plotly.express as px
from handler.handler_fixa import fixa_avancada
from handler.handler_movel import altas_e_migracoes
import pandas as pd

df_fixa = pd.read_excel('dataframes/vendas concluidas - fixa - 2023 e 2022.xlsx')

df_fixa_2022, df_fixa_2023 = '', ''

filtro_ano = ['Todos','2022', '2023']
filtro_revenda = ['Todos', 'FREECEL', 'PARCEIRO', 'VALPARAISO', 'ESCRITORIO', 'FREECEL SAMAMBAIA']

st.title('Vendas Concluídas 2022 e 2023')
st.write('---------------------------------------')
selectbox_ano = st.selectbox('Ano Selecionado:', options=filtro_ano)
selectbox_revenda = st.selectbox('Revenda: ', options=filtro_revenda)

st.write('#### Avançada ')
tab_fixa, tab_avancada, tab_soho, tab_vvn = st.tabs(['GERAL', 'AVANÇADA', 'SOHO', 'VVN'])

with tab_fixa:
    df_fixa_geral = fixa_avancada(ano=selectbox_ano, tipo='GERAL', revenda=selectbox_revenda, aggregate=True)
    fig = px.line(df_fixa_geral, x='MÊS', y='VALOR ACUMULADO')
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

with tab_avancada:
    df_fixa_avancada = fixa_avancada(ano=selectbox_ano, tipo='AVANÇADA', revenda=selectbox_revenda, aggregate=True)
    fig = px.line(df_fixa_avancada, x='MÊS', y='VALOR ACUMULADO')
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

with tab_soho:
    df_fixa_soho = fixa_avancada(ano=selectbox_ano, tipo='FIXA', revenda=selectbox_revenda, aggregate=True)
    fig = px.line(df_fixa_soho, x='MÊS', y='VALOR ACUMULADO')
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

with tab_vvn:
    df_fixa_vvn = fixa_avancada(ano=selectbox_ano, tipo='VVN', revenda=selectbox_revenda, aggregate=True)
    fig = px.line(df_fixa_vvn, x='MÊS', y='VALOR ACUMULADO')
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

st.write('#### Móvel ')
tab_movel, tab_altas, tab_migracao = st.tabs(['GERAL', 'ALTAS', 'MIGRAÇÃO PRÉ-PÓS'])

with tab_movel:
    df_movel_geral =  altas_e_migracoes(selectbox_ano, revenda=selectbox_revenda, tipo='GERAL', aggregate=True)
    fig = px.line(df_movel_geral, x='MÊS', y='VALOR ACUMULADO')
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

with tab_altas:
    df_movel_altas =  altas_e_migracoes(selectbox_ano, revenda=selectbox_revenda, tipo='ALTAS', aggregate=True)
    fig = px.line(df_movel_altas, x='MÊS', y='VALOR ACUMULADO')
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

with tab_migracao:
    df_movel_migracao = altas_e_migracoes(selectbox_ano, revenda=selectbox_revenda, tipo='MIGRAÇÃO PRÉ-PÓS', aggregate=True)
    fig = px.line(df_movel_migracao, x='MÊS', y='VALOR ACUMULADO')
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    