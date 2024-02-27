from streamlit_extras.metric_cards import style_metric_cards
from datetime import datetime
import streamlit as st
import os

from dataframe.rankings import Rankings
from dataframe.vendas import Vendas
from dataframe.stats import Stats

from plots.rankings import plot_rankings
from plots.scatter import plot_line
from plots.pie import plot_pie

from utils.utils import months, month_by_numbers


# Configurando o layout da página
st.set_page_config(
    page_title = "Home - Freecel",
    page_icon = "https://i.imgur.com/pidHoxz.png",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {
        'About': "https://github.com/shadyrajab/freecel-dashboard"
    }
)

with open('styles/styles.css', 'r') as styles:
    css = styles.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

@st.cache_data
def load_dates():
    dates = Stats().dates

    return dates

@st.cache_data
def load_data(ano: int, mes: str):
    ano = None if ano == 'Todos' else ano
    mes = None if mes == 'Todos' else mes

    stats = Stats(ano, mes)
    rankings = Rankings(ano, mes)
    vendas = Vendas()

    return stats, rankings, vendas

dates = load_dates()

# Barra lateral com filtragem de ano e mês
with st.sidebar:
    mes = None
    # Selecionando todos os anos no qual houveram vendas registradas
    years = ['Todos', 2024] + [list(year.keys())[0] for year in dates]
    ano = st.sidebar.selectbox(
        label = 'Ano', 
        options = years, 
        index = years.index(datetime.now().year)
    )

    if ano != 'Todos':
        # Selecionando todos os meses de um determinado ano no qual houveram vendas registradas
        months = ['Todos'] + sorted([month for year_dict in dates if ano in year_dict for month in year_dict[ano]], key = months.index)
        mes = st.selectbox(
            label = 'Mês: ', 
            options = months, 
            index = months.index(month_by_numbers[datetime.now().month])
        )

st.title(
    body = (
        f'Relatório de Vendas - {ano}' if ano and mes == 'Todos' else
        f'Relatório de Vendas - {mes}/{ano}' if ano and mes else
        f'Relatório de Vendas - Geral'
    )
)

# Definir o estilo dos metric cards
style_metric_cards(border_left_color = '#ffffff', border_radius_px = 20)

stats, rankings, vendas = load_data(ano, mes)

metric1, metric2, metric3 = st.columns(3)
metric4, metric5, metric6 = st.columns(3)

metric1.metric(
    label = f'Receita Total',
    value = f'R$ {stats.receita_total:,.0f}',
    delta = int(stats.delta_receita_total)
)

metric2.metric(
    label = f'Quantidade de Produtos',
    value = int(stats.quantidade_vendida),
    delta = int(stats.delta_quantidade_produtos)
)

metric3.metric(
    label = 'Quantidade de Clientes',
    value = int(stats.quantidade_clientes),
    delta = int(stats.delta_quantidade_clientes)
)

metric4.metric(
    label = 'Média por Consultor',
    value = f'R$ {stats.media_por_consultor_geral:,.0f}',
    delta = int(stats.delta_media_por_consultor)
)

metric5.metric(
    label = 'Ticket Médio',
    value = f'R$ {stats.ticket_medio:,.0f}',
    delta = int(stats.delta_ticket_medio)
)

metric6.metric(
    label = 'Média Diária',
    value = f'R$ {stats.receita_media_diaria:,.0f}',
    delta = int(stats.delta_media_diaria)
)


# Ranking de Consultores
with st.container(border = True):
    tab_geral, tab_altas, tab_migracao, tab_fixa, tab_avancada, tab_vvn = st.tabs(
            ['Geral', 'Altas', 'Migração Pré-Pós', 'Fixa', 'Avançada', 'VVN']
        )
    
    with tab_geral:
        try:
            plot_rankings(
                dataframe = rankings.ranking_consultores.sort_values(
                    by = 'valor_acumulado', ascending = False
                )
                [0:16], title ='Ranking Geral', key = 'consultor', media = stats.media_por_consultor_geral, color = ["red", "blue", "#3E35AB"]
            )
        
        except:
            st.error(body = 'Não há dados para a sua solicitação')

    with tab_altas:
        try:
            dataframe = plot_rankings(
                rankings.ranking_altas.sort_values(
                    by = 'valor_acumulado', ascending = False
                )
                [0:16], title = 'Ranking Altas', key = 'consultor', media = stats.media_por_consultor_altas, color = ["red", "blue", "#3E35AB"]
            )

        except:
            st.error(body = 'Não há dados para a sua solicitação')

    with tab_migracao:
        try:
            plot_rankings(
                dataframe = rankings.ranking_migracao.sort_values(
                    by = 'valor_acumulado', ascending = False
                )
                [0:16], title = 'Ranking Migração Pré-pós', key = 'consultor',  media = stats.media_por_consultor_migracao, color = ["red", "blue", "#3E35AB"]
            )
        
        except:
            st.error(body = 'Não há dados para a sua solicitação')

    with tab_fixa:
        try:
            plot_rankings(
                dataframe = rankings.ranking_fixa.sort_values(
                    by = 'valor_acumulado', ascending = False
                )
                [0:16], title = 'Ranking Fixa', key = 'consultor',  media = stats.media_por_consultor_fixa, color = ["red", "blue", "#3E35AB"]
            )
        
        except:
            st.error(body = 'Não há dados para a sua solicitação')

    with tab_avancada:
        # try:
            plot_rankings(
                dataframe = rankings.ranking_avancada.sort_values(
                    by = 'valor_acumulado', ascending = False
                )
                [0:16], title = 'Ranking Avançada', key = 'consultor',  media = stats.media_por_consultor_avancada, color = ["red", "blue", "#3E35AB"]
            )
        
        # except:
        #     st.error(body = 'Não há dados para a sua solicitação')

    with tab_vvn:
        try:
            plot_rankings(
                dataframe = rankings.ranking_vvn.sort_values(
                    by = 'valor_acumulado', ascending = False
                )
                [0:16], title = 'Ranking VVN', key = 'consultor',  media = stats.media_por_consultor_vvn, color = ["red", "blue", "#3E35AB"]
            )

        except:
            st.error(body = 'Não há dados para a sua solicitação')


# Colunas para os gráficos de tipos de produto e equipe
pie1, pie2 = st.columns(2)


# Equipe
with pie1:
    with st.container(border = True):
        tab_valor, tab_vol, tab_clientes = st.tabs(['Receita', 'Volume', 'Clientes'])
        group = True if ano == 'Todos' else False

        with tab_valor:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group), 
                'revenda', 'valor_acumulado', 'Receita por Equipe', 
                color = ["#FFC102", "#FF4560", "#1A374B", "#70DC9E"]
            )

        with tab_vol:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group), 
                'revenda', 'quantidade_de_produtos', 'Volume por Equipe',
                color = ["#FFC102", "#FF4560", "#1A374B", "#70DC9E"]
            )

        with tab_clientes:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group), 
                'revenda', 'clientes', 'Clientes por Equipe',
                color = ["#FFC102", "#FF4560", "#1A374B", "#70DC9E"]
            )


# Tipo de Produto
with pie2:
    with st.container(border = True):
        tab_valor, tab_vol, tab_clientes = st.tabs(['Receita', 'Volume', 'Clientes'])
        group = True if ano == 'Todos' else False

        with tab_valor:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group), 
                'tipo', 'valor_acumulado', 'Receita por Tipo de Produto',
                color = ["#FFC102", "#FF4560", "#1A374B", "#70DC9E"]
            )

        with tab_vol:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group), 
                'tipo', 'quantidade_de_produtos', 'Volume por Tipo de Produto', 
                color = ["#FFC102", "#FF4560", "#1A374B", "#70DC9E"]
            )

        with tab_clientes:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group), 
                'tipo', 'clientes', 'Clientes por Tipo de Produto', 
                color = ["#FFC102", "#FF4560", "#1A374B", "#70DC9E"]
            )


# Ranking de Planos
with st.container(border = True):
    plot_rankings(
        dataframe = rankings.ranking_planos.sort_values(
            by = 'valor_acumulado', ascending = False
        )
        [0:16], title = 'Ranking Planos', key = 'plano', color = ["yellow", "orange", "red"]
    )


# Gráfico Vendas Mensais
with st.container(border = True):
    plot_line(vendas.vendas_by_data(), 'geral')


# Porta Heroku
PORT = int(os.environ.get('PORT', 8501))