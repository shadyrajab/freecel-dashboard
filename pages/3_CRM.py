import streamlit as st
import pandas as pd 
import re
from requests import request

import streamlit as st
from requests import request
from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN = getenv('tokenFreecel')

cnpj = st.text_input('Qual CNPJ do cliente')
telefone = st.text_input('Qual telefone do cliente')
consultor = st.text_input('Qual o nome do consultor que realizou a venda')
data = st.text_input('Qual a data da venda? (escreva no formato xx-xx-xxxx)')
gestor = st.text_input('Qual nome do gestor?')
plano = st.text_input('Qual nome do plano vendido')
quantidade_de_produtos = st.text_input('Qual a quantidade de produtos vendidos')
revenda = st.text_input('Qual escritório realizou a venda?')
tipo = st.text_input('Qual tipo de venda?')
uf = st.text_input('Qual a uf da venda?')
valor_do_plano = st.text_input('Qual o valor do plano?')
email = st.text_input('Qual o email do cliente?')

bt = st.button("Enviar", type = 'primary')

def enviar_dados():
    url = 'https://freecelapi-b44da8eb3c50.herokuapp.com/vendas'
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }

    params = {
        "cnpj": cnpj,
        "telefone": telefone,
        "consultor": consultor,
        "data": data,
        "gestor": gestor,
        "plano": plano,
        "quantidade_de_produtos": quantidade_de_produtos,
        "revenda": revenda,
        "tipo": tipo,
        "uf": uf,
        "valor_do_plano": valor_do_plano,
        "email": email
    }

    response = request('PUT', url = url, json = params, headers = headers)

    print(response.text)

if bt:
    enviar_dados()
