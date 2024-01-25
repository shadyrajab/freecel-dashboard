from plots.generate_plot_movel import plot_movel
from handler.handler_movel import altas_e_migracoes
from handler.handler_fixa import fixa_avancada
import streamlit as st

def st_plot(dataframe, general = True | False):
    fig = plot_movel(dataframe, general)
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

def plot(planilha, ano, revenda, tipo):
    general = True if ano == 'Geral' else False
    print(general)
    if planilha == 'MÓVEL':
        dataframe = altas_e_migracoes(revenda = revenda, ano = ano, tipo = tipo, aggregate = False)
        st_plot(dataframe, general)
    
    if planilha == 'FIXA':
        dataframe = fixa_avancada(revenda=revenda, ano = ano, tipo = tipo, aggregate = False)
        st_plot(dataframe, general)
