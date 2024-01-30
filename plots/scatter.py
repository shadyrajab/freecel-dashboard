import plotly.graph_objects as go
import plotly.express as px
from dataframes.stats.basic_stats import get_vendas_mensais_por_consultor
import streamlit as st

def plot_line(
    consultores
):  
    
    fig = go.Figure()

    for consultor in consultores:
        dataframe = get_vendas_mensais_por_consultor(2023, consultor)
        
        fig.add_trace(
            go.Scatter(
                dataframe,
                x = dataframe['MÊS'],
                y = dataframe['VALOR ACUMULADO']
            )
        )
    fig.show()
    # st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)