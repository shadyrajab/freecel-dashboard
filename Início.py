import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from plots.rankings import plot_rankings
from plots.pie import plot_pie
from plots.scatter import plot_line

from dataframe.freecel import Stats

# Configurando o Layout e título de página
st.set_page_config(layout="wide")
st.title('Dashboard Freecel')

with open('styles/styles.css', 'r') as styles:
    css = styles.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.markdown('----')

ano = st.sidebar.selectbox('Ano: ', options = Stats.years())
mes = st.sidebar.selectbox('Mês: ', options = Stats.months())

freecel = Stats(ano, mes)

col1, col2, col3 = st.columns(3)
metric1, metric2, metric3 = st.columns(3)
st.markdown('----')
col4, col5 = st.columns(2)
st.markdown('----')

col1.metric(
    label = f'Receita Total - {mes}',
    value = f'R$ {freecel.receita_total:,.0f}',
    delta = int(freecel.delta_receita_total)
)

col2.metric(
    label = f'Quantidade de Produtos - {mes}',
    value = f'{freecel.quantidade_vendida:,.0f}',
    delta = freecel.delta_quantidade_produtos
)

col3.metric(
    label = 'Média Diária', 
    value = f'R$ {freecel.receita_media_diaria:,.0f}', 
    delta = int(freecel.delta_media_diaria)
)
metric1.metric(
    label = 'Média Mensal por Consultor', 
    value = f'R$ {freecel.media_por_consultor:,.0f}', 
    delta = int(freecel.delta_media_por_consultor)
)
metric2.metric(
    label = 'Ticket Médio', 
    value = f'R$ {freecel.ticket_medio:,.0f}', 
    delta = int(freecel.delta_ticket_medio)
)

metric3.metric(
    label = 'Quantidade de Clientes',
    value = int(freecel.quantidade_clientes),
    delta = freecel.delta_quantidade_clientes
)

style_metric_cards(border_left_color = '#000000')

with st.container(border = True):
    plot_line(freecel.vendas(groupby = 'data'), 'geral')

with col4:
    with st.container(border = True):
        tab_valor, tab_qtd = st.tabs(['Receita', 'Quantidade'])

        with tab_valor:
            plot_pie(freecel.vendas(ano, mes), 'consultor', 'valor_acumulado', 'Consultor')

        with tab_qtd:
            plot_pie(freecel.vendas(ano, mes), 'consultor', 'quantidade_de_produtos', 'Consultor')

with col5:
    with st.container(border = True):
        tab_valor, tab_qtd = st.tabs(['Receita', 'Quantidade'])

        with tab_valor:
            plot_pie(freecel.vendas(ano, mes), 'tipo', 'valor_acumulado', 'Tipo de Produto')
        
        with tab_qtd:
            plot_pie(freecel.vendas(ano, mes), 'tipo', 'quantidade_de_produtos', 'Tipo de Produto')


with st.container(border = True):
    retorno = st.selectbox('Ordenar por', options = ['Receita', 'Quantidade'])
    sortby = 'valor_acumulado' if retorno == 'Receita' else 'quantidade_de_produtos'

    tab_geral, tab_altas, tab_migracao, tab_fixa, tab_soho, tab_vvn = st.tabs(
        ['Geral', 'Altas', 'Migração Pré-Pós', 'Fixa', 'SOHO', 'VVN']
    )

    with tab_geral:
        plot_rankings(freecel.ranking_consultores(sortby, 'ranking_consultores', ano, mes), sortby, 'Ranking de Consultores')

    with tab_altas:
        plot_rankings(freecel.ranking_consultores(sortby, 'ranking_altas', ano, mes), sortby, 'Ranking de Consultores')

    with tab_migracao:
        plot_rankings(freecel.ranking_consultores(sortby, 'ranking_migracao', ano, mes), sortby, 'Ranking de Consultores')

    with tab_fixa:
        plot_rankings(freecel.ranking_consultores(sortby, 'ranking_fixa', ano, mes), sortby, 'Ranking de Consultores')

    with tab_soho:
        plot_rankings(freecel.ranking_consultores(sortby, 'ranking_avancada', ano, mes), sortby, 'Ranking de Consultores')

    with tab_vvn:
        try:
            plot_rankings(freecel.ranking_consultores(sortby, 'ranking_vvn', ano, mes), sortby, 'Ranking de Consultores')
        except:
            st.write('Não há dados para sua solicitação')

st.markdown('### Estatísticas de clientes')
st.markdown('----')

st.markdown('Vendas por CNAE')
st.dataframe(freecel.qtd_vendas_por_cnae)

st.markdown('----')

st.markdown('Vendas por FATURAMENTO DE EMPRESA')
st.dataframe(freecel.qtd_vendas_por_faturamento)

st.markdown('----')

st.markdown('Vendas por QUANTIDADE DE FUNCIONÁRIOS DA EMPRESA')
st.dataframe(freecel.qtd_vendas_por_colaboradores)