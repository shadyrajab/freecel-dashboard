import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from dataframes.objects import dataframe_geral

def plot_pie(
    ano, mes, key
):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes)
    ]

    fig = go.Figure(
        px.pie(
            dataframe,
            values = 'VALOR ACUMULADO',
            names = key
        )
    )

    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)