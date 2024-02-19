import streamlit as st
from plots.scatter import plot_line
from plots.pie import plot_pie_consultor
from streamlit_extras.metric_cards import style_metric_cards

import plotly.express as px

from dataframe.consultor import Consultor
from dataframe.freecel import Stats

freecel = Stats()

consultor_st = st.sidebar.selectbox('Selecionar Consultor', options = freecel.consultores())

st.title(consultor_st)
st.markdown('-----')

m1, m2, m3 = st.columns(3)
m4, m5, m6 = st.columns(3)
st.markdown('-----')
col4, col5 = st.columns(2)

consultor = Consultor(consultor_st)

m1.metric(
    label = 'Receita Total',
    value = f'R$ {consultor.receita_total:,.0f}',
)

m2.metric(
    label = 'Receita Média Mensal',
    value = f'R$ {consultor.receita_media_mensal:,.0f}'
)

m3.metric(
    label = 'Ticket Médio',
    value = f'R$ {consultor.ticket_medio:,.0f}'
)

m4.metric(
    label = 'Quantidade Total',
    value = consultor.quantidade_vendida
)

m5.metric(
    label = 'Quantidade Média Mensal',
    value = int(consultor.quantidade_media_mensal)
)

m6.metric(
    label = 'Quantidade de Clientes',
    value = consultor.quantidade_clientes
)

style_metric_cards(border_left_color = '#000000')

st.markdown('-----')
plot_line(consultor.groupby_data, consultor.name)
st.markdown('-----')

ano = st.selectbox('Ano', options = consultor.years)
mes = st.selectbox('Mês', options = consultor.months)

with col4:
    plot_pie_consultor(
        consultor.vendas, 'tipo', 'valor_acumulado', 'Receita por Produtos',
        color = px.colors.sequential.RdBu
    )

with col5:
    plot_pie_consultor(
        consultor.vendas, 'tipo', 'quantidade_de_produtos', 'Quantidade de Produtos',
        color = px.colors.sequential.Aggrnyl
    )
