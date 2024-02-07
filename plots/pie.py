import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from dataframes.objects import dataframe_geral

def plot_pie(
    ano, mes, tipo, key, title
):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes)
    ]

    fig = go.Figure(
        px.pie(
            dataframe,
            values = key,
            names = tipo,
            title = title
        )
    )

    fig.update_traces(textposition='inside', textinfo='value')
    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)

def plot_pie_consultor(
    consultor, tipo, key, title, color
):
    
    dataframe = dataframe_geral[
        (dataframe_geral['CONSULTOR'] == consultor)
    ]

    fig = go.Figure(
        px.pie(
            dataframe,
            values = key,
            names = tipo,
            title = title,
            color_discrete_sequence = color
        )
    )

    fig.update_traces(textposition='inside', textinfo='value')

    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)