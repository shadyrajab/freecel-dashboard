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

with tab_fixa:
    plot(planilha = 'FIXA', revenda = selectbox_revenda, ano = selectbox_ano, tipo='GERAL')

with tab_avancada:
    plot(planilha = 'FIXA', revenda = selectbox_revenda, ano = selectbox_ano, tipo='AVANÇADA')

with tab_soho:
    plot(planilha = 'FIXA', revenda = selectbox_revenda, ano = selectbox_ano, tipo='FIXA')

with tab_vvn:
    plot(planilha = 'FIXA', revenda = selectbox_revenda, ano = selectbox_ano, tipo='VVN')

st.write('#### Móvel ')
tab_movel, tab_altas, tab_migracao = st.tabs(['GERAL', 'ALTAS', 'MIGRAÇÃO PRÉ-PÓS'])

with tab_movel:
    plot(planilha = 'MÓVEL', revenda = selectbox_revenda, ano = selectbox_ano, tipo='GERAL')

with tab_altas:
    plot(planilha = 'MÓVEL', revenda = selectbox_revenda, ano = selectbox_ano, tipo='ALTAS')

with tab_migracao:
    plot(planilha = 'MÓVEL', revenda = selectbox_revenda, ano = selectbox_ano, tipo='MIGRAÇÃO PRÉ-PÓS')
    