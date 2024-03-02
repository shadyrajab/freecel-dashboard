from streamlit_extras.metric_cards import style_metric_cards
from plotly.colors import sequential
from typing import Optional
import streamlit as st

from plots.rankings import plot_rankings
from plots.scatter import plot_line
from plots.pie import plot_pie

from dataframe.consultor import Consultor
from dataframe.stats import Stats
from utils.utils import months

# Configurando o layout da página
st.set_page_config(
    page_title = "Consultor - Freecel",
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

@st.cache_data(show_spinner = False)
def load_consultores():
    consultores = Stats().consultores

    return consultores

@st.cache_data(show_spinner = False)
def load_data(consultor: str, ano: Optional[int] = None, mes: Optional[str] = None):
    ano = None if ano == 'Todos' else ano
    mes = None if mes == 'Todos' else mes
    consultor = Consultor(consultor, ano, mes)

    return consultor

consultores = load_consultores()

with st.sidebar:
    mes = None
    consultor = st.sidebar.selectbox(
        label = 'Selecionar Consultor', 
        options = consultores
    )

consultor = load_data(consultor = consultor)

with st.sidebar:
    # Selecionando todos os anos no qual o consultor realizou vendas
    years = ['Todos'] + [list(year.keys())[0] for year in consultor.dates]
    ano = st.selectbox(
        label = 'Ano', 
        options = years,
        index = years.index('Todos')
    )

    if ano != 'Todos':
        # Selecionando todos os meses do ano selecionado no qual o consultor realizou vendas
        months = ['Todos'] + sorted([month for year_dict in consultor.dates if ano in year_dict for month in year_dict[ano]], key = months.index)
        mes = st.selectbox(
            label = 'Mês',
            options = months,
            index = months.index('Todos')
        )
ano = None if ano == 'Todos' else ano
mes = None if mes == 'Todos' else mes

consultor = load_data(consultor = consultor.nome, ano = ano, mes = mes)

st.title(
    body = (
        f'{consultor.nome.title()} - {ano}' if ano and mes == 'Todos' else
        f'{consultor.nome.title()} - {mes}/{ano}' if ano and mes else
        f'{consultor.nome.title()} - Geral'
    )
)

# Definir o estilo dos metric cards
style_metric_cards(border_left_color = '#ffffff', border_radius_px = 20)

metric1, metric2, metric3 = st.columns(3)
metric4, metric5, metric6 = st.columns(3)

metric1.metric(
    label = f'Receita Total',
    value = f'R$ {consultor.receita_total(ano, mes):,.0f}',
    delta = int(consultor.delta_receita_total(ano, mes))
)

metric2.metric(
    label = f'Quantidade de Produtos',
    value = int(consultor.quantidade_vendida(ano, mes)),
    delta = int(consultor.delta_quantidade_produtos(ano, mes))
)

metric3.metric(
    label = 'Quantidade de Clientes',
    value = int(consultor.quantidade_clientes(ano, mes)),
    delta = int(consultor.delta_quantidade_clientes(ano, mes))
)

metric4.metric(
    label = 'Média Mensal',
    value = f'R$ {consultor.receita_media_mensal(ano, mes):,.0f}',
    delta = 0
)

metric5.metric(
    label = 'Ticket Médio',
    value = f'R$ {consultor.ticket_medio(ano, mes):,.0f}',
    delta = int(consultor.delta_ticket_medio(ano, mes))
)

metric6.metric(
    label = 'Média Diária',
    value = f'R$ {consultor.receita_media_diaria(ano, mes):,.0f}',
    delta = int(consultor.delta_media_diaria(ano, mes))
)

# Gráfico vendas mensais  
with st.container(border = True):
    plot_line(dataframe = consultor.groupby_data, title = f'Receita por Data - {consultor.nome.title()}', x = 'data', y = 'valor_acumulado')

# Gráfico de pizza Tipo de Produto
with st.container(border = True):
    tab_valor, tab_vol, tab_clientes = st.tabs(['Receita', 'Volume', 'Clientes'])
    with tab_valor:
        plot_pie(
            consultor.vendas, 
            'tipo', 'valor_acumulado', 'Receita por Produtos',
            color = sequential.Aggrnyl
        )

    with tab_vol:
        plot_pie(
            consultor.vendas, 
            'tipo', 'quantidade_de_produtos', 'Quantidade de Produtos',
            color = sequential.Aggrnyl
        )

    with tab_clientes:
        plot_pie(
            consultor.vendas, 
            'tipo', 'Clientes', 'Quantidade de Vendas',
            color = sequential.Aggrnyl
        )

# Ranking de Planos
with st.container(border = True):
    plot_rankings(
        dataframe = consultor.ranking_produtos.sort_values(
            by = 'valor_acumulado', ascending = False
        )
        [0:16], title = 'Ranking Planos', key = 'plano', color = ["yellow", "orange", "red"]
    )