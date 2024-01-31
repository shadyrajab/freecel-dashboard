import streamlit as st
from dataframes.objects import get_consultores
from plots.scatter import plot_line

st.title('Consultores')

consultor = st.sidebar.selectbox('Selecionar Consultor', options = get_consultores())

plot_line(consultor)