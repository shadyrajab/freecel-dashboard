import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from dataframes.stats.basic_stats import get_rankings_consultores

def plot_rankings(
    ano, mes, tipo, key, title
):
    dataframe = get_rankings_consultores(ano, mes, tipo, key)

    fig = go.Figure(
        px.bar(
            dataframe,
            y = 'CONSULTOR',
            x = key,
            orientation = 'h',
            title = title,
            hover_data = ['VALOR ACUMULADO', 'QUANTIDADE DE PRODUTOS'],
            color = key,
            text_auto = '.1s',
            range_color = [dataframe[key].min(), dataframe[key].max()],
            color_continuous_scale = ["blue", "purple", "red", "yellow"]
        )
    )

    fig.update_layout(yaxis = dict(autorange = "reversed"))
    fig.update_traces(texttemplate='%{x:.1f}', textposition='outside')
    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)