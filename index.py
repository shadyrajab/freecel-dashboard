import asyncio
from datetime import datetime, timedelta
from typing import Optional

import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

from dataframe.rankings import Rankings
from dataframe.stats import Stats
from dataframe.vendas import Vendas
from plots.rankings import plot_rankings
from utils.utils import MONTHS, equipes, format_tab_name, month_by_numbers


async def load_data(data_inicio, data_fim, equipe: Optional[str] = None):
    async def load_stats():
        return Stats(data_inicio, data_fim, equipe)

    async def load_rankings():
        return Rankings(data_inicio, data_fim, equipe)

    async def load_vendas():
        return Vendas()

    tasks = [load_stats(), load_rankings(), load_vendas()]
    stats, rankings, vendas = await asyncio.gather(*tasks)
    return stats, rankings, vendas


class App:
    def __init__(self) -> None:
        self.__set_page_config()
        self.__set_css_style()
        self.__inicialize_sidebar()
        self.stats, self.rankings, self.vendas = asyncio.run(
            load_data(
                self.data_inicio.strftime("%d-%m-%Y"),
                self.data_fim.strftime("%d-%m-%Y"),
                (self.equipe if self.equipe != "Todos" else None),
            )
        )
        self.__set_cards_style()
        (
            self.metric1,
            self.metric2,
            self.metric3,
            self.metric4,
            self.metric5,
            self.metric6,
        ) = self.__get_metric_cards()
        self.__set_basic_metrics()
        self.__set_mean_metrics()
        self.__plot_ranking_consultores()

    def __set_page_config(self):
        st.set_page_config(
            page_title="Home - Freecel",
            page_icon="https://i.imgur.com/pidHoxz.png",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={"About": "https://github.com/shadyrajab/freecel-dashboard"},
        )

    def __set_css_style(self):
        with open("styles/styles.css", "r") as styles:
            css = styles.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    def __inicialize_sidebar(self):
        now = datetime.now()
        diff = now - timedelta(days=30)
        min_date = datetime(2022, 1, 1)
        with st.sidebar:
            self.data_inicio = st.date_input(
                label="Data Inicial",
                value=diff,
                min_value=min_date,
                max_value=now,
                format="DD/MM/YYYY",
            )
            self.data_fim = st.date_input(
                label="Data Final",
                value=now,
                min_value=min_date,
                max_value=now,
                format="DD/MM/YYYY",
            )
            self.equipe = st.selectbox(label="Equipe", options=["Todos"] + equipes)

    def __set_cards_style(self):
        style_metric_cards(border_left_color="#ffffff", border_radius_px=20)

    def __get_metric_cards(self):
        metric1, metric2, metric3 = st.columns(3)
        metric4, metric5, metric6 = st.columns(3)

        return metric1, metric2, metric3, metric4, metric5, metric6

    def __set_basic_metrics(self):
        self.metric1.metric(
            label=f"Receita Total",
            value=f"R$ {self.stats.receita:,.0f}",
            delta=int(self.stats.delta_receita),
        )

        self.metric2.metric(
            label=f"Quantidade de Produtos",
            value=int(self.stats.volume),
            delta=int(self.stats.delta_volume),
        )

        self.metric3.metric(
            label="Quantidade de Clientes",
            value=int(self.stats.clientes),
            delta=int(self.stats.delta_clientes),
        )

    def __set_mean_metrics(self):
        self.metric4.metric(
            label="Média por Consultor",
            value=f"R$ {self.stats.media_consultor_geral:,.0f}",
            delta=int(self.stats.delta_media_consultor_geral),
        )

        self.metric5.metric(
            label="Ticket Médio",
            value=f"R$ {self.stats.ticket_medio:,.0f}",
            delta=int(self.stats.delta_ticket_medio),
        )

        self.metric6.metric(
            label="Receita Média",
            value=f"R$ {self.stats.receita_media:,.0f}",
            delta=int(self.stats.delta_receita_media),
        )

    def __plot_ranking_consultores(self):
        tab_names = [
            "Geral",
            "Altas",
            "Portabilidade",
            "Migração",
            "Fixa",
            "Avançada",
            "VVN",
        ]
        with st.container(border=True):
            tabs = st.tabs(tab_names)
            for tipo, tab in zip(tab_names, tabs):
                formated_tipo = format_tab_name(tipo)
                with tab:
                    try:
                        fig = plot_rankings(
                            dataframe=self.rankings[formated_tipo].sort_values(
                                by="receita", ascending=False
                            )[0:16],
                            title=f"Ranking {tipo}",
                            key="consultor",
                            media=self.stats[f"media_consultor_{formated_tipo}"],
                            color=["red", "blue", "#3E35AB"],
                        )
                        st.plotly_chart(
                            fig, theme="streamlit", use_container_width=True
                        )

                    except:
                        st.error(body="Não há dados para a sua solicitação")


if __name__ == "__main__":
    App()
