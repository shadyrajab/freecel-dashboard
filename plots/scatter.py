import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def plot_line(
    dataframe, consultor
):  
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x = dataframe['data'],
            y = dataframe['valor_acumulado'],
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