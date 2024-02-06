import streamlit as st
import pandas as pd 

df = pd.read_excel('dataframes/excel/crm 05-02.xlsx')

st.dataframe(df)