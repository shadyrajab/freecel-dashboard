import streamlit as st
from dataframe.freecel import Stats
from utils.utils import formatar_cnpj, formatar_telefone, remover_ponto
from requests import request
from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv('tokenFreecel')

vendas = Stats.vendas().astype(str)
vendas['cnpj'] = vendas['cnpj'].apply(lambda cnpj: formatar_cnpj(cnpj))
vendas['telefone'] = vendas['telefone'].apply(lambda telefone: formatar_telefone(telefone))
vendas[['matriz', 'porte', 'capital_social', 'situacao_cadastral', 'cep']] = vendas[
    ['matriz', 'porte', 'capital_social', 'situacao_cadastral', 'cep']
].map(remover_ponto)

vendas = vendas[
    [
        'id', 'cnpj', 'plano', 'tipo', 'quantidade_de_produtos', 'valor_do_plano', 'valor_acumulado', 
        'consultor', 'cep', 'uf', 'municipio', 'bairro', 'telefone', 'email', 'ano', 'mês', 'data',
        'revenda', 'gestor', 'cnae', 'faturamento', 'quadro_funcionarios', 'capital_social', 'porte',
        'natureza_juridica', 'matriz', 'situacao_cadastral', 'regime_tributario'
    ]
] 

ano = st.selectbox(label = 'Qual ano deseja filtrar?', options = ['2024', '2023', '2022'])
mes = st.selectbox(label = 'Qual mês deseja filtrar?', options = ['Janeiro', 'Fevereiro', 'Março'])

st.dataframe(vendas)

add_venda, remove_venda = st.tabs(['Adicionar venda', 'Remover venda'])

url = f'https://freecelapi-b44da8eb3c50.herokuapp.com/vendas'

headers = {
    'Authorization': f'Bearer {TOKEN}'
}

with add_venda:
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

    if st.button('Adicionar'):
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
        st.success('Venda adicionada com sucesso.')

with remove_venda:
    id_venda = st.text_input('Qual o ID da venda que deseja remover?')

    if st.button('Remover'):
        response = request('DELETE', url = url, headers=headers, json = {'id': id_venda})
        st.success('Venda removida com sucesso.')