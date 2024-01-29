import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from dataframes.stats.basic_stats import get_rankings_consultores

def plot_rankings(
    ano, mes, tipo
):
    dataframe = get_rankings_consultores(ano, mes, tipo)

    fig = go.Figure(
        px.bar(
            dataframe,
            y = 'CONSULTOR',
            x = 'VALOR ACUMULADO',
            orientation = 'h'
        )
    )

    fig.update_layout(yaxis = dict(autorange = "reversed"))

    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)