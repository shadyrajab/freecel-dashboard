import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def plot_rankings(
    dataframe, key, title
):
    fig = go.Figure(
        px.bar(
            dataframe,
            y = 'consultor',
            x = key,
            orientation = 'h',
            title = title,
            hover_data = ['valor_acumulado', 'quantidade_de_produtos'],
            color = key,
            text_auto = '.1s',
            range_color = [dataframe[key].min(), dataframe[key].max()],
            color_continuous_scale = ["blue", "purple", "red", "yellow"]
        )
    )

    fig.update_layout(yaxis = dict(autorange = "reversed"), plot_bgcolor="#ffffff", paper_bgcolor = "#ffffff")
    fig.update_traces(texttemplate='%{x:.1f}', textposition='outside')
    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)