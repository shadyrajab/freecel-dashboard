import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from dataframes.objects import get_years, get_months
from plots.indicators import plot_metric, plot_gauge
from plots.rankings import plot_rankings
from plots.pie import plot_pie

from dataframes.stats.basic_stats import *

# Configurando o Layout e título de página
st.set_page_config(layout="wide")
st.title('Dashboard Freecel')

st.markdown('----')

ano = st.sidebar.selectbox('Ano: ', options=get_years())
mes = st.sidebar.selectbox('Mês: ', options=get_months(ano))

col1, col2, col3 = st.columns(3)
st.markdown('----')
metric1, metric2, metric3 = st.columns(3)
st.markdown('----')
col4, col5 = st.columns(2)
st.markdown('----')

metric1.metric(
    label = 'Média Diária', 
    value = 'R$ ' + str(get_media_mensal_diaria(ano, mes)), 
    delta = get_delta_mensal_diaria(ano, mes)
)
metric2.metric(
    label = 'Média Mensal por Consultor', 
    value = 'R$ ' + str(get_media_mensal_por_consultor(ano, mes)), 
    delta = get_delta_mensal_por_consultor(ano, mes)
)
metric3.metric(
    label = 'Ticket Médio', 
    value = 'R$ ' + str(get_ticket_medio_mensal(ano, mes)), 
    delta = get_delta_ticket_medio_mensal(ano, mes)
)

style_metric_cards(border_left_color = '#000000')

with col1:
    st.markdown('##### Receita Total')
    plot_metric(ano, mes, '#add8e6', prefix = 'R$')
    plot_gauge(ano, mes, '#add8e6', prefix = 'R$')

with col2:
    st.markdown('##### Quantidade de Produtos ')
    plot_metric(ano, mes, '#00FF00', prefix = '', metric = 'PRODUTOS')
    plot_gauge(ano, mes, '#00FF00', prefix = '', metric = 'PRODUTOS')

with col3:
    st.markdown('##### Consultor do mês')
    plot_metric(ano, mes, '#ff6961', prefix = 'R$', metric = 'CONSULTORES')
    plot_gauge(ano, mes, '#ff6961', prefix = 'R$', metric = 'CONSULTORES')

with col4:
    tab_valor, tab_qtd = st.tabs(['Receita', 'Quantidade'])

    with tab_valor:
        plot_pie(ano, mes, 'CONSULTOR', 'VALOR ACUMULADO', 'Consultor')

    with tab_qtd:
        plot_pie(ano, mes, 'CONSULTOR', 'QUANTIDADE DE PRODUTOS', 'Consultor')

with col5:
    tab_valor, tab_qtd = st.tabs(['Receita', 'Quantidade'])

    with tab_valor:
        plot_pie(ano, mes, 'TIPO', 'VALOR ACUMULADO', 'Tipo de Produto')
    
    with tab_qtd:
        plot_pie(ano, mes, 'TIPO', 'QUANTIDADE DE PRODUTOS', 'Tipo de Produto')

retorno = st.selectbox('Ordenar por', options = ['Receita', 'Quantidade'])
retorno = 'VALOR ACUMULADO' if retorno == 'Receita' else 'QUANTIDADE DE PRODUTOS'

tab_geral, tab_altas, tab_migracao, tab_fixa, tab_soho, tab_vvn = st.tabs(
    ['Geral', 'Altas', 'Migração Pré-Pós', 'Fixa', 'SOHO', 'VVN']
)

with tab_geral:
    plot_rankings(ano, mes, 'GERAL', retorno, 'Ranking de Consultores')

with tab_altas:
    plot_rankings(ano, mes, 'ALTAS', retorno, 'Ranking de Consultores')

with tab_migracao:
    plot_rankings(ano, mes, 'MIGRAÇÃO PRÉ-PÓS', retorno, 'Ranking de Consultores')

with tab_fixa:
    plot_rankings(ano, mes, 'FIXA', retorno, 'Ranking de Consultores')

with tab_soho:
    plot_rankings(ano, mes, 'AVANÇADA', retorno, 'Ranking de Consultores')

with tab_vvn:
    plot_rankings(ano, mes, 'VVN', retorno, 'Ranking de Consultores')
