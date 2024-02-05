import plotly.graph_objects as go
import plotly.express as px
from dataframes.stats.basic_stats import get_vendas_mensais_por_consultor
import streamlit as st

def plot_line(
    consultor
):  
    
    fig = go.Figure()

    dataframe1 = get_vendas_mensais_por_consultor(consultor)
    fig.add_trace(
        go.Scatter(
            x = dataframe1['DATA'],
            y = dataframe1['VALOR ACUMULADO'],
            mode = 'lines+markers',
            name = '2023',
            line = {
                "color": "firebrick",
                "width": 2
            }
        )
    )

    fig.update_layout(
        title = f'Vendas anuais por mês - {consultor}',
        xaxis_title = 'Receita',
        yaxis_title = 'Mês'
    )

    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)