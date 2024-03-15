import asyncio
import os
from datetime import datetime

import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

from dataframe.rankings import Rankings
from dataframe.stats import Stats
from dataframe.vendas import Vendas
from plots.pie import plot_pie
from plots.rankings import plot_rankings
from plots.scatter import plot_line
from utils.utils import format_tab_name, month_by_numbers, months

# Configurando o layout da página
st.set_page_config(
    page_title="Home - Freecel",
    page_icon="https://i.imgur.com/pidHoxz.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "https://github.com/shadyrajab/freecel-dashboard"},
)

with open("styles/styles.css", "r") as styles:
    css = styles.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


@st.cache_data
def load_dates():
    dates = Stats().dates

    return dates


async def load_data(ano: int, mes: str):
    ano = None if ano == "Todos" else ano
    mes = None if mes == "Todos" else mes

    async def load_stats():
        return Stats(ano, mes)

    async def load_rankings():
        return Rankings(ano, mes)

    async def load_vendas():
        return Vendas()

    tasks = [load_stats(), load_rankings(), load_vendas()]
    stats, rankings, vendas = await asyncio.gather(*tasks)
    return stats, rankings, vendas


dates = load_dates()

# Barra lateral com filtragem de ano e mês
with st.sidebar:
    mes = None
    # Selecionando todos os anos no qual houveram vendas registradas
    years = ["Todos"] + sorted([list(year.keys())[0] for year in dates], reverse=True)
    ano = st.sidebar.selectbox(
        label="Ano", options=years, index=years.index(str(datetime.now().year))
    )

    if ano != "Todos":
        # Selecionando todos os meses de um determinado ano no qual houveram vendas registradas
        months = ["Todos"] + sorted(
            [
                month
                for year_dict in dates
                if ano in year_dict
                for month in year_dict[ano]
            ],
            key=months.index,
        )
        mes = st.selectbox(
            label="Mês: ",
            options=months,
            index=months.index(month_by_numbers[datetime.now().month - 1]),
        )

st.title(
    body=(
        f"Relatório de Vendas - {ano}"
        if ano and mes == "Todos"
        else (
            f"Relatório de Vendas - {mes}/{ano}"
            if ano and mes
            else f"Relatório de Vendas - Geral"
        )
    )
)

# Definir o estilo dos metric cards
style_metric_cards(border_left_color="#ffffff", border_radius_px=20)

stats, rankings, vendas = asyncio.run(load_data(ano, mes))

metric1, metric2, metric3 = st.columns(3)
metric4, metric5, metric6 = st.columns(3)

metric1.metric(
    label=f"Receita Total",
    value=f"R$ {stats.receita:,.0f}",
    delta=int(stats.delta_receita),
)

metric2.metric(
    label=f"Quantidade de Produtos",
    value=int(stats.volume),
    delta=int(stats.delta_volume),
)

metric3.metric(
    label="Quantidade de Clientes",
    value=int(stats.clientes),
    delta=int(stats.delta_clientes),
)

metric4.metric(
    label="Média por Consultor",
    value=f"R$ {stats.media_consultor_geral:,.0f}",
    delta=int(stats.delta_media_consultor_geral),
)

metric5.metric(
    label="Ticket Médio",
    value=f"R$ {stats.ticket_medio:,.0f}",
    delta=int(stats.delta_ticket_medio),
)

metric6.metric(
    label="Média Diária",
    value=f"R$ {stats.receita_media:,.0f}",
    delta=int(stats.delta_receita_media),
)

tab_names = ["Geral", "Altas", "Portabilidade", "Migração", "Fixa", "Avançada", "VVN"]

# Ranking de Consultores
with st.container(border=True):
    # Cria uma aba para cada valor em tab_names
    tabs = st.tabs(tab_names)
    for tipo, tab in zip(tab_names, tabs):
        with tab:
            formated_tipo = format_tab_name(tipo)
            try:
                plot_rankings(
                    dataframe=rankings[formated_tipo].sort_values(
                        by="receita", ascending=False
                    )[0:16],
                    title=f"Ranking {tipo}",
                    key="consultor",
                    media=stats[f"media_consultor_{formated_tipo}"],
                    color=["red", "blue", "#3E35AB"],
                )

            except:
                st.error(body="Não há dados para a sua solicitação")

# Colunas para os gráficos de tipos de produto e equipe
pie1, pie2 = st.columns(2)


# Equipe
with pie1:
    with st.container(border=True):
        tab_valor, tab_vol, tab_clientes = st.tabs(["Receita", "Volume", "Clientes"])
        group = True if ano == "Todos" else False

        with tab_valor:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group),
                "Equipe",
                "Receita",
                "Receita por Equipe",
                color=["#FFC102", "#FF4560", "#1A374B", "#70DC9E"],
            )

        with tab_vol:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group),
                "Equipe",
                "Volume",
                "Volume por Equipe",
                color=["#FFC102", "#FF4560", "#1A374B", "#70DC9E"],
            )

        with tab_clientes:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group),
                "Equipe",
                "Clientes",
                "Clientes por Equipe",
                color=["#FFC102", "#FF4560", "#1A374B", "#70DC9E"],
            )


# Tipo de Produto
with pie2:
    with st.container(border=True):
        tab_valor, tab_vol, tab_clientes = st.tabs(["Receita", "Volume", "Clientes"])
        group = True if ano == "Todos" else False

        with tab_valor:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group),
                "Tipo",
                "Receita",
                "Receita por Tipo de Produto",
                color=["#FFC102", "#FF4560", "#1A374B", "#70DC9E"],
            )

        with tab_vol:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group),
                "Tipo",
                "Volume",
                "Volume por Tipo de Produto",
                color=["#FFC102", "#FF4560", "#1A374B", "#70DC9E"],
            )

        with tab_clientes:
            plot_pie(
                vendas.vendas_by_data(ano, mes, group),
                "Tipo",
                "Clientes",
                "Clientes por Tipo de Produto",
                color=["#FFC102", "#FF4560", "#1A374B", "#70DC9E"],
            )


# Ranking de Planos
with st.container(border=True):
    plot_rankings(
        dataframe=rankings.planos.sort_values(by="receita", ascending=False)[0:16],
        title="Ranking Planos",
        key="plano",
        color=["yellow", "orange", "red"],
    )


# Gráfico Vendas Mensais
with st.container(border=True):
    plot_line(
        dataframe=vendas.vendas_by_data(),
        title="Receita por Data",
        x="Data",
        y="Receita",
    )


# Porta Heroku
PORT = int(os.environ.get("PORT", 8501))
