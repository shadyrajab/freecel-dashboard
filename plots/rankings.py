import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from dataframes.stats.basic_stats import get_rankings_consultores

def plot_rankings(
    ano, mes, tipo, key, title
):
    dataframe = get_rankings_consultores(ano, mes, tipo)

    fig = go.Figure(
        px.bar(
            dataframe,
            y = 'CONSULTOR',
            x = key,
            orientation = 'h',
            title = title,
            text_auto = '.2s'
        )
    )

    fig.update_layout(yaxis = dict(autorange = "reversed"))

    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)