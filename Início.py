import streamlit as st
from dataframes.objects import get_years, get_months, get_escritorios
from plots.indicators import plot_metric, plot_gauge

# Configurando o Layout e título de página
st.set_page_config(layout="wide")
st.title('Dashboard de Vendas Freecel')

st.markdown('----')

selectbox_ano = st.sidebar.selectbox('Ano: ', options=get_years())
selectbox_mes = st.sidebar.selectbox('Mês: ', options=get_months(selectbox_ano))
selectbox_revenda = st.sidebar.selectbox('Revenda: ', options=['Todos'] + get_escritorios())

tab_fixa, tab_avancada, tab_soho, tab_vvn = st.tabs(['GERAL', 'AVANÇADA', 'SOHO', 'VVN'])

col1, col2, col3 = st.columns(3)
st.markdown('----')
col4, col5 = st.columns(2)

with col1:
    st.markdown('##### Receita Total')
    plot_metric(selectbox_ano, selectbox_mes, selectbox_revenda, '#add8e6', prefix = 'R$')
    plot_gauge(selectbox_ano, selectbox_mes, selectbox_revenda, '#add8e6', prefix = 'R$')

with col2:
    st.markdown('##### Quantidade de Produtos ')
    plot_metric(selectbox_ano, selectbox_mes, selectbox_revenda, '#00FF00', prefix = '', metric = 'PRODUTOS')
    plot_gauge(selectbox_ano, selectbox_mes, selectbox_revenda, '#00FF00', prefix = '', metric = 'PRODUTOS')

with col3:
    st.markdown('##### Consultor do mês')
    plot_metric(selectbox_ano, selectbox_mes, selectbox_revenda, '#ff6961', prefix = 'R$', metric = 'CONSULTORES')
    plot_gauge(selectbox_ano, selectbox_mes, selectbox_revenda, '#ff6961', prefix = 'R$', metric = 'CONSULTORES')

with col4:
    pass