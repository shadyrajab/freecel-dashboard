import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from dataframes.objects import get_years, get_months, get_escritorios
from plots.indicators import plot_metric, plot_gauge
from plots.rankings import plot_rankings
from plots.pie import plot_pie

from dataframes.stats.basic_stats import get_media_mensal_por_consultor, get_media_mensal_diaria, get_ticket_medio_mensal

# Configurando o Layout e título de página
st.set_page_config(layout="wide")
st.title('Dashboard Freecel')

st.markdown('----')

ano = st.sidebar.selectbox('Ano: ', options=get_years())
mes = st.sidebar.selectbox('Mês: ', options=get_months(ano))
revenda = st.sidebar.selectbox('Revenda: ', options=['Todos'] + get_escritorios())

col1, col2, col3 = st.columns(3)
st.markdown('----')
col7, col8, col9 = st.columns(3)
st.markdown('----')
col4, col5, col6 = st.columns(3)

col7.metric(label = 'Média Diária', value = get_media_mensal_diaria(ano, mes), delta = 1200)
col8.metric(label = 'Média Mensal por Consultor', value = get_media_mensal_por_consultor(ano, mes), delta = 1200)
col9.metric(label = 'Ticket Médio', value = get_ticket_medio_mensal(ano, mes), delta = 1200)

style_metric_cards(border_left_color = '#000000')

with col1:
    st.markdown('##### Receita Total')
    plot_metric(ano, mes, revenda, '#add8e6', prefix = 'R$')
    plot_gauge(ano, mes, revenda, '#add8e6', prefix = 'R$')

with col2:
    st.markdown('##### Quantidade de Produtos ')
    plot_metric(ano, mes, revenda, '#00FF00', prefix = '', metric = 'PRODUTOS')
    plot_gauge(ano, mes, revenda, '#00FF00', prefix = '', metric = 'PRODUTOS')

with col3:
    st.markdown('##### Consultor do mês')
    plot_metric(ano, mes, revenda, '#ff6961', prefix = 'R$', metric = 'CONSULTORES')
    plot_gauge(ano, mes, revenda, '#ff6961', prefix = 'R$', metric = 'CONSULTORES')

with col4:
    plot_rankings(ano, mes, 'GERAL')

with col5:
    plot_pie(ano, mes, 'TIPO')

with col6:
    plot_pie(ano, mes, 'REVENDA')