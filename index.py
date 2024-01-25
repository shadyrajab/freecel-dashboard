import streamlit as st
from plots.generate_plot import plot
import pandas as pd


filtro_ano = ['Geral', 'Todos', '2022', '2023']
filtro_revenda = ['Geral', 'Todos', 'FREECEL', 'PARCEIRO', 'VALPARAISO', 'ESCRITORIO', 'FREECEL SAMAMBAIA']

st.title('Vendas Concluídas 2022 e 2023')
st.write('---------------------------------------')

selectbox_ano = st.selectbox('Ano Selecionado:', options=filtro_ano)
selectbox_revenda = st.selectbox('Revenda: ', options=filtro_revenda)

st.write('#### Avançada ')
tab_fixa, tab_avancada, tab_soho, tab_vvn = st.tabs(['GERAL', 'AVANÇADA', 'SOHO', 'VVN'])

# with tab_fixa:
#     df_fixa_geral = fixa_avancada(ano=selectbox_ano, tipo='GERAL', revenda=selectbox_revenda, aggregate=True)
#     fig = px.line(df_fixa_geral, x='MÊS', y='VALOR ACUMULADO')
#     st.plotly_chart(fig, theme='streamlit', use_container_width=True)

# with tab_avancada:
#     df_fixa_avancada = fixa_avancada(ano=selectbox_ano, tipo='AVANÇADA', revenda=selectbox_revenda, aggregate=True)
#     fig = px.line(df_fixa_avancada, x='MÊS', y='VALOR ACUMULADO')
#     st.plotly_chart(fig, theme='streamlit', use_container_width=True)

# with tab_soho:
#     df_fixa_soho = fixa_avancada(ano=selectbox_ano, tipo='FIXA', revenda=selectbox_revenda, aggregate=True)
#     fig = px.line(df_fixa_soho, x='MÊS', y='VALOR ACUMULADO')
#     st.plotly_chart(fig, theme='streamlit', use_container_width=True)

# with tab_vvn:
#     df_fixa_vvn = fixa_avancada(ano=selectbox_ano, tipo='VVN', revenda=selectbox_revenda, aggregate=True)
#     fig = px.line(df_fixa_vvn, x='MÊS', y='VALOR ACUMULADO')
#     st.plotly_chart(fig, theme='streamlit', use_container_width=True)

st.write('#### Móvel ')
tab_movel, tab_altas, tab_migracao = st.tabs(['GERAL', 'ALTAS', 'MIGRAÇÃO PRÉ-PÓS'])

with tab_movel:
    plot(planilha = 'MÓVEL', revenda = selectbox_revenda, ano = selectbox_ano, tipo='GERAL')

with tab_altas:
    plot(planilha = 'MÓVEL', revenda = selectbox_revenda, ano = selectbox_ano, tipo='ALTAS')

with tab_migracao:
    plot(planilha = 'MÓVEL', revenda = selectbox_revenda, ano = selectbox_ano, tipo='MIGRAÇÃO PRÉ-PÓS')
    