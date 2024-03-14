from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.utils import formatar_nome


def plot_rankings(
    dataframe: pd.DataFrame,
    title: str,
    key: str,
    media: Optional[int] = None,
    color: Optional[list] = None,
):
    if key == "consultor":
        dataframe["consultor"] = dataframe["consultor"].apply(
            lambda nome: formatar_nome(nome)
        )

    dataframe.rename(columns={"receita": "Receita"}, inplace=True)

    if dataframe.shape[0] == 0:
        return st.error("Não há dados para a sua solicitação")

    fig = go.Figure(
        px.bar(
            dataframe,
            y=key,
            x="Receita",
            orientation="h",
            title=title,
            hover_data=["Receita", "volume"],
            color="Receita",
            text_auto=".1s",
            range_color=[dataframe["Receita"].min(), dataframe["Receita"].max()],
            color_continuous_scale=color,
        )
    )

    if media:
        # Adicionar linha separadora para a média de vendas
        fig.add_vline(
            x=media,
            line_dash="dash",
            line_color="black",
            annotation={"text": "<b>Média<b>", "font": {"size": 14, "color": "black"}},
            annotation_position="top",
        )

    fig.update_layout(
        yaxis={
            "autorange": "reversed",
            "title": "Consultor" if key == "consultor" else "Planos",
        },
        xaxis={"title": "Receita"},
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        bargap=0.2,
        showlegend=False,
    )

    fig.update_traces(
        texttemplate="%{x:.1f}",
        textposition="outside",
    )

    return st.plotly_chart(fig, theme="streamlit", use_container_width=True)
