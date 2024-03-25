import asyncio

import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards


class App:
    def __init__(self) -> None:
        self.__set_page_config()
        self.__set_css_style()
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

    def __set_cards_style(self):
        style_metric_cards(border_left_color="#ffffff", border_radius_px=20)

    def __get_metric_cards(self):
        metric1, metric2, metric3 = st.columns(3)
        metric4, metric5, metric6 = st.columns(3)

        return metric1, metric2, metric3, metric4, metric5, metric6

    def __set_basic_metrics(self):
        self.metric1.metric(
            label=f"Receita Total",
            value=f"R$ {stats.receita:,.0f}",
            delta=int(stats.delta_receita),
        )

        self.metric2.metric(
            label=f"Quantidade de Produtos",
            value=int(stats.volume),
            delta=int(stats.delta_volume),
        )

        self.metric3.metric(
            label="Quantidade de Clientes",
            value=int(stats.clientes),
            delta=int(stats.delta_clientes),
        )

    def __set_mean_metrics(self):
        self.metric4.metric(
            label="Média por Consultor",
            value=f"R$ {stats.media_consultor_geral:,.0f}",
            delta=int(stats.delta_media_consultor_geral),
        )

        self.metric5.metric(
            label="Ticket Médio",
            value=f"R$ {stats.ticket_medio:,.0f}",
            delta=int(stats.delta_ticket_medio),
        )

        self.metric6.metric(
            label="Média Diária",
            value=f"R$ {stats.receita_media:,.0f}",
            delta=int(stats.delta_receita_media),
        )

    def __get_ranking_consultores(self):
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


if __name__ == "__main__":
    App()
