import plotly.graph_objects as go
import streamlit as st
from dataframes.stats.basic_stats import get_maior_venda_escritorio, get_receita_total, get_consultor_do_mes, get_maior_venda_consultor, get_maior_venda_mes
import random

def plot_metric(
    ano, mes, escritorio, indicator_color, prefix, metric = None
):  
    title_indicator = mes
    receita = get_receita_total('VALOR ACUMULADO', ano, mes, escritorio)

    if metric == 'CONSULTORES':
        consultor_do_mes = get_consultor_do_mes(ano, mes)
        receita = int(consultor_do_mes['VALOR ACUMULADO'])
        title_indicator = list(consultor_do_mes['CONSULTOR'])[0]
    
    if metric == 'REVENDA':
        receita = get_receita_total('VALOR ACUMULADO')

    if metric == 'PRODUTOS':
        receita = get_receita_total('QUANTIDADE DE PRODUTOS', ano, mes, escritorio)

    fig = go.Figure(
        go.Indicator(
            value = receita,
            gauge = { 
                "axis": {"visible": False}, 
            },

            title = {
                "text": title_indicator,
                "font": {"size": 28}
            },
            number = {
                "prefix": prefix,
                "font": {"size": 28},
                "font_color": 'black'
            }
        )
    )

    fig.add_trace(
        go.Scatter(
            y = random.sample(range(0, 101), 30),
            hoverinfo = 'skip',
            fill = 'tozeroy', 
            marker = None,
            line = dict(color = indicator_color)
        )
    )

    fig.update_xaxes(visible = False, fixedrange = True)
    fig.update_yaxes(visible = False, fixedrange = True)

    fig.update_layout(
        margin = dict(t = 30, b = 0),
        showlegend = False,
        plot_bgcolor = 'white',
        height = 70,
        
    )

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)



def plot_gauge(
    ano, mes, escritorio, indicator_color, prefix, metric = None
):
    receita = get_receita_total('VALOR ACUMULADO', ano, mes, escritorio)
    axis_range = get_maior_venda_mes('VALOR ACUMULADO')

    if metric == 'CONSULTORES':
        consultor_do_mes = get_consultor_do_mes(ano, mes)
        receita = int(consultor_do_mes['VALOR ACUMULADO'])

        axis_range = get_maior_venda_consultor(ano)
    
    if metric == 'REVENDA':
        axis_range = get_maior_venda_escritorio(ano)
    
    if metric == 'PRODUTOS':
        receita = get_receita_total('QUANTIDADE DE PRODUTOS', ano, mes, escritorio)
        axis_range = get_maior_venda_mes('QUANTIDADE DE PRODUTOS')

    fig = go.Figure(
        go.Indicator(
            value = receita,
            mode = "gauge+number",
            number = {
                "prefix": prefix
            },  
            gauge = {
                "axis": { "range": [0, axis_range], "tickwidth": 2},
                "bar": { "color": indicator_color}
            },
            title = {
                "text": "Relação Atual",
                "font": {"size": 20}
            }
        )
    )

    fig.update_layout(
        margin = dict(t = 50, b = 10),
        showlegend = False,
        plot_bgcolor = 'white',
        height = 150,
    )

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)