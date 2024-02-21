import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from plots.rankings import plot_rankings
from plots.pie import plot_pie
from plots.scatter import plot_line

from dataframe.freecel import Stats
from dataframe.rankings import Ranking
from dataframe.vendas import Vendas
import os

# Configurando o Layout e título de página
st.set_page_config(layout="wide")
st.title('Dashboard Freecel')

with open('styles/styles.css', 'r') as styles:
    css = styles.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

ano = st.sidebar.selectbox('Ano: ', options=Stats.years())
mes = st.sidebar.selectbox('Mês: ', options=Stats.months())

@st.cache_data
def load_data(ano, mes):
    freecel = Stats(ano, mes)
    rankings = Ranking(ano, mes)
    vendas = Vendas()
    return freecel, rankings, vendas

freecel, rankings, vendas = load_data(ano, mes)

# Renderizar os elementos somente após os dados estarem carregados
with st.spinner('Carregando dados...'):
    m1, m2, m3 = st.columns(3)
    m4, m5, m6 = st.columns(3)
    st.write('-------')
    col4, col5 = st.columns(2)

    m1.metric(
        label=f'Receita Total - {mes}',
        value=f'R$ {freecel.receita_total:,.0f}',
        delta=int(freecel.delta_receita_total)
    )

    m2.metric(
        label=f'Quantidade de Produtos - {mes}',
        value=f'{freecel.quantidade_vendida:,.0f}',
        delta=freecel.delta_quantidade_produtos
    )

    m3.metric(
        label='Média Diária',
        value=f'R$ {freecel.receita_media_diaria:,.0f}',
        delta=int(freecel.delta_media_diaria)
    )
    m4.metric(
        label='Média Mensal por Consultor',
        value=f'R$ {freecel.media_por_consultor:,.0f}',
        delta=int(freecel.delta_media_por_consultor)
    )
    m5.metric(
        label='Ticket Médio',
        value=f'R$ {freecel.ticket_medio:,.0f}',
        delta=int(freecel.delta_ticket_medio)
    )

    m6.metric(
        label='Quantidade de Clientes',
        value=int(freecel.quantidade_clientes),
        delta=freecel.delta_quantidade_clientes
    )

    style_metric_cards(border_left_color='#ffffff', border_radius_px=20)

    with st.container(border=True):
        plot_line(vendas.vendas_by_data(), 'geral')

    with col4:
        with st.container(border=True):
            tab_valor, tab_qtd = st.tabs(['Receita', 'Quantidade'])

            with tab_valor:
                plot_pie(vendas.vendas_by_data(ano, mes), 'consultor', 'valor_acumulado', 'Consultor')

            with tab_qtd:
                plot_pie(vendas.vendas_by_data(ano, mes), 'consultor', 'quantidade_de_produtos', 'Consultor')

    with col5:
        with st.container(border=True):
            tab_valor, tab_qtd = st.tabs(['Receita', 'Quantidade'])

            with tab_valor:
                plot_pie(vendas.vendas_by_data(ano, mes), 'tipo', 'valor_acumulado', 'Tipo de Produto')

            with tab_qtd:
                plot_pie(vendas.vendas_by_data(ano, mes), 'tipo', 'quantidade_de_produtos', 'Tipo de Produto')

    with st.container(border=True):
        retorno = st.selectbox('Ordenar por', options=['Receita', 'Quantidade'])
        sortby = 'valor_acumulado' if retorno == 'Receita' else 'quantidade_de_produtos'

        tab_geral, tab_altas, tab_migracao, tab_fixa, tab_soho, tab_vvn = st.tabs(
            ['Geral', 'Altas', 'Migração Pré-Pós', 'Fixa', 'SOHO', 'VVN']
        )

        with tab_geral:
            plot_rankings(rankings.ranking_consultores.sort_values(
                by=sortby, ascending=False)[0:16], sortby, 'Ranking de Consultores')

        with tab_altas:
            plot_rankings(rankings.ranking_altas.sort_values(
                by=sortby, ascending=False)[0:16], sortby, 'Ranking de Consultores')

        with tab_migracao:
            plot_rankings(rankings.ranking_migracao.sort_values(
                by=sortby, ascending=False)[0:16], sortby, 'Ranking de Consultores')

        with tab_fixa:
            plot_rankings(rankings.ranking_fixa.sort_values(
                by=sortby, ascending=False)[0:16], sortby, 'Ranking de Consultores')

        with tab_soho:
            plot_rankings(rankings.ranking_avancada.sort_values(
                by=sortby, ascending=False)[0:16], sortby, 'Ranking de Consultores')

        with tab_vvn:
            try:
                plot_rankings(rankings.ranking_vvn.sort_values(
                    by=sortby, ascending=False)[0:16], sortby, 'Ranking de Consultores')
            except:
                st.write('Não há dados para sua solicitação')


port = int(os.environ.get('PORT', 8501))
