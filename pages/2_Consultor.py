import streamlit as st
from dataframes.objects import get_consultores
from plots.scatter import plot_line
from plots.pie import plot_pie_consultor
from dataframes.stats.basic_stats import *
from streamlit_extras.metric_cards import style_metric_cards

import plotly.express as px

from dataframes.objects import get_years, meses


consultor = st.sidebar.selectbox('Selecionar Consultor', options = get_consultores())

st.title(consultor)
st.markdown('-----')

m1, m2, m3 = st.columns(3)
m4, m5, m6 = st.columns(3)
st.markdown('-----')
col4, col5 = st.columns(2)

receita_total = int(get_receita_total('VALOR ACUMULADO', consultor = consultor))
receita_media_mensal = int(get_media_vendas_consultor(consultor, 'VALOR ACUMULADO'))
ticket_medio_consultor = int(get_ticket_medio_consultor(consultor))

qtd_clientes = int(get_quantidade_clientes(consultor))

qtd_vendida = int(get_receita_total('QUANTIDADE DE PRODUTOS', consultor = consultor))
media_qtd_vendida = int(get_media_vendas_consultor(consultor, 'QUANTIDADE DE PRODUTOS'))

m1.metric(
    label = 'Receita Total',
    value = f'R$ {receita_total:,.0f}'
)

m2.metric(
    label = 'Receita Média Mensal',
    value = f'R$ {receita_media_mensal:,.0f}'
)

m3.metric(
    label = 'Ticket Médio',
    value = f'R$ {ticket_medio_consultor:,.0f}'
)

m4.metric(
    label = 'Quantidade Total',
    value = qtd_vendida
)

m5.metric(
    label = 'Quantidade Média Mensal',
    value = media_qtd_vendida
)

m6.metric(
    label = 'Quantidade de Clientes',
    value = qtd_clientes
)

style_metric_cards(border_left_color = '#000000')

st.markdown('-----')
plot_line(consultor)
st.markdown('-----')

ano = st.selectbox('Ano', options = get_years(consultor))
mes = st.selectbox('Mês', options = meses)

with col4:
    plot_pie_consultor(
        consultor, 'TIPO', 'VALOR ACUMULADO', 'Receita por Produtos',
        color = px.colors.sequential.RdBu
    )

with col5:
    plot_pie_consultor(
        consultor, 'TIPO', 'QUANTIDADE DE PRODUTOS', 'Quantidade de Produtos',
        color = px.colors.sequential.Aggrnyl
    )
