from plots.generate_fig import generate_fig, generate_bar_fig
from handler.handler_movel import altas_e_migracoes
import plotly.express as px
from handler.handler_fixa import fixa_avancada
import streamlit as st

def st_plot(dataframe, general = True | False):
    fig = generate_fig(dataframe, general)
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

def st_plot_bar(dataframe, general = True | False):
    dataframe = dataframe.groupby(
            'MÊS', as_index=False, sort=False).sum(numeric_only=True
        )
    
    fig = px.bar(
        dataframe,
        x = 'MÊS',
        y = 'VALOR ACUMULADO'
    )

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

def plot(planilha, ano, revenda, tipo):
    general = True if ano == 'Geral' else False
    if planilha == 'MÓVEL':
        dataframe = altas_e_migracoes(revenda = revenda, ano = ano, tipo = tipo, aggregate = False)
        st_plot(dataframe, general)
        st_plot_bar(dataframe, general)
    
    if planilha == 'FIXA':
        dataframe = fixa_avancada(revenda=revenda, ano = ano, tipo = tipo, aggregate = False)
        st_plot(dataframe, general)
        st_plot_bar(dataframe, general)
