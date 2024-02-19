import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def plot_pie(
    dataframe, tipo, key, title
):

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
    dataframe, tipo, key, title, color
):

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