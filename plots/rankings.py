from utils.utils import formatar_nome
import plotly.graph_objects as go
from typing import Optional
import plotly.express as px
import streamlit as st
import pandas as pd

def plot_rankings(dataframe: pd.DataFrame, title: str, key: str, media: Optional[int] = None, color: Optional[list] = None):
    if key == 'consultor':
        dataframe['consultor'] = dataframe['consultor'].apply(lambda nome: formatar_nome(nome))

    fig = go.Figure(
        px.bar(
            dataframe,
            y = key,
            x = 'valor_acumulado',
            orientation = 'h',
            title = title,
            hover_data = ['valor_acumulado', 'quantidade_de_produtos'],
            color = 'valor_acumulado',
            text_auto = '.1s',
            range_color = [dataframe['valor_acumulado'].min(), dataframe['valor_acumulado'].max()],
            color_continuous_scale = color,
        )
    )

    if media :
        # Adicionar linha separadora para a média de vendas
        fig.add_vline(
            x = media, 
            line_dash = "dash", 
            line_color = 'black', 
            annotation = {
                "text": '<b>Média<b>', 
                "font": {
                    "size": 14, 
                    "color": "black"
                } 
            }, 
            annotation_position = 'top'
        )

    fig.update_layout(
        yaxis = {
            "autorange": "reversed"
        },
        plot_bgcolor = "#ffffff", 
        paper_bgcolor = "#ffffff",
        bargap = 0.2,
    )

    fig.update_traces(
        texttemplate = '%{x:.1f}', 
        textposition = 'outside',
    )

    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)