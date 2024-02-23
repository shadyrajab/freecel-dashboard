import streamlit as st
from dataframe.freecel import Stats
from utils.utils import formatar_cnpj, formatar_telefone, remover_ponto
from requests import request
from os import getenv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TOKEN = getenv('tokenFreecel')

vendas = Stats.vendas().astype(str)
vendas['cnpj'] = vendas['cnpj'].apply(lambda cnpj: formatar_cnpj(cnpj))
vendas['telefone'] = vendas['telefone'].apply(lambda telefone: formatar_telefone(telefone))
vendas[['matriz', 'porte', 'capital_social', 'situacao_cadastral', 'cep']] = vendas[
    ['matriz', 'porte', 'capital_social', 'situacao_cadastral', 'cep']
].map(remover_ponto)

with open('styles/vendas.css', 'r') as styles:
    css = styles.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

vendas = vendas[
    [
        'id', 'cnpj', 'plano', 'tipo', 'quantidade_de_produtos', 'valor_do_plano', 'valor_acumulado', 
        'consultor', 'cep', 'uf', 'municipio', 'bairro', 'telefone', 'email', 'ano', 'mês', 'data',
        'revenda', 'gestor', 'cnae', 'faturamento', 'quadro_funcionarios', 'capital_social', 'porte',
        'natureza_juridica', 'matriz', 'situacao_cadastral', 'regime_tributario'
    ]
] 

with st.container(border = True):
    ano = st.selectbox(label = 'Adicionar Filtro:', options = ['Nenhum', 'Ano', 'Mês', 'Tipo'])
    selected_columns = []
    with st.expander('Selecionar colunas'):
        for col in vendas.columns.to_list():
            selected = st.checkbox(col, value = True)
            if selected:
                selected_columns.append(col)

    vendas = vendas[selected_columns]

    st.dataframe(vendas)

url = f'https://freecelapi-b44da8eb3c50.herokuapp.com/vendas'

headers = {
    'Authorization': f'Bearer {TOKEN}'
}

with st.container(border = True):
    with st.expander('Adicionar venda'):
        today = datetime.today().date()
        
        with st.form("adicionar_venda"):
            cnpj = st.text_input('Qual CNPJ do cliente', max_chars = 14)
            telefone = st.text_input('Qual telefone do cliente')
            consultor = st.selectbox('Qual o nome do consultor que realizou a venda', options = Stats.consultores())
            data = st.date_input('Qual a data da venda?', format = 'DD/MM/YYYY', max_value=today)
            gestor = st.text_input('Qual nome do gestor?')
            plano = st.text_input('Qual nome do plano vendido')
            quantidade_de_produtos = st.text_input('Qual a quantidade de produtos vendidos')
            revenda = st.selectbox('Qual equipe realizou a venda?', options = ['FREECEL', 'VALPARAISO', 'PARCEIRO', 'ESCRITORIO'])
            tipo = st.selectbox('Qual tipo de venda?', options = ["FIXA", "AVANÇADA", "MIGRAÇÃO PRÉ-PÓS", "VVN","ALTAS"])
            uf = st.text_input('Qual a uf da venda?', max_chars = 2)
            valor_do_plano = st.text_input('Qual o valor do plano?')
            email = st.text_input('Qual o email do cliente?')

            submit = st.form_submit_button('Enviar')

            if submit:
                params = {
                    "cnpj": cnpj,
                    "telefone": telefone,
                    "consultor": consultor,
                    "data": str(datetime.strptime(str(data), '%Y-%m-%d').strftime('%d-%m-%Y')),
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

    with st.expander('Remover venda'):
        with st.form('remover_venda'):
            id_venda = st.text_input('Qual o ID da venda que deseja remover?')

            submit = st.form_submit_button('Remover')

            if submit:
                response = request('DELETE', url = url, headers=headers, json = {'id': id_venda})
                st.success('Venda removida com sucesso.')