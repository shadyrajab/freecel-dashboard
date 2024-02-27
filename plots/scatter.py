import plotly.graph_objects as go
import streamlit as st

def plot_line(dataframe, title, x, y):  
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x = dataframe[x],
            y = dataframe[y],
            mode = 'lines+markers',
            name = '2023',
            line = {
                "color": "#6495ED", 
                "width": 2, 
                "shape": 'spline'
            },
            fill = 'tozeroy',
            fillcolor = '#ADD8E6'
        )
    )

    fig.update_layout(
        title = title,
        xaxis_title = 'Mês',
        yaxis_title = 'Receita',
        plot_bgcolor = '#ffffff',
        font = {
            "color": 'black'
        }, 
        hovermode = 'x', 
        xaxis = {
            "tickmode": 'linear',
            "dtick": 'M1', 
            "tickformat": '%b\n%Y',
            "showgrid": False
        },
        yaxis={
            "range": [dataframe[y].min() / 1.5, dataframe[y].max() * 1.1], 
            "showgrid": False
        },
        paper_bgcolor = "#ffffff"
    )

    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)