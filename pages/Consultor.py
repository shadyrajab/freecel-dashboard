import streamlit as st
from plots.scatter import plot_line
from plots.pie import plot_pie
from streamlit_extras.metric_cards import style_metric_cards

import plotly.express as px

from dataframe.consultor import Consultor
from dataframe.freecel import Stats

with open('styles/styles.css', 'r') as styles:
    css = styles.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

@st.cache_data
def get_consultores():
    freecel = Stats()

    return freecel.consultores()

consultores = get_consultores()

consultor_st = st.sidebar.selectbox('Selecionar Consultor', options = consultores)

st.title(consultor_st)

m1, m2, m3 = st.columns(3)
m4, m5, m6 = st.columns(3)

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

style_metric_cards(border_left_color = '#ffffff', border_radius_px = 20)


with st.container(border = True):
    plot_line(consultor.groupby_data, consultor.name)

with st.container(border = True):
    tab_valor, tab_vol, tab_clientes = st.tabs(['Receita', 'Volume', 'Clientes'])
    with tab_valor:
        plot_pie(
            consultor.vendas, 'tipo', 'valor_acumulado', 'Receita por Produtos',
            color = px.colors.sequential.RdBu
        )

    with tab_vol:
        plot_pie(
            consultor.vendas, 'tipo', 'quantidade_de_produtos', 'Quantidade de Produtos',
            color = px.colors.sequential.Aggrnyl
        )

    with tab_clientes:
        plot_pie(
            consultor.vendas, 'tipo', 'clientes', 'Quantidade de Vendas',
            color = px.colors.sequential.Aggrnyl
        )
