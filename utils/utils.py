from dotenv import load_dotenv
from os import getenv
import streamlit as st

load_dotenv()

# Criar formulário para a adição de vendas na API
def get_form(consultores, today):
    cnpj = st.text_input('Qual CNPJ do cliente?', max_chars = 14, placeholder = 'CNPJ')
    ddd = st.selectbox('Qual DDD do cliente?', options = DDDS)
    telefone = st.text_input('Qual telefone do cliente? (Com DDD)', max_chars = 11, placeholder = 'TELEFONE')
    consultor = st.selectbox('Qual o nome do consultor que realizou a venda?', options = consultores)
    data = st.date_input('Qual a data da venda?', format = 'DD/MM/YYYY', max_value = today)
    gestor = st.text_input('Qual nome do gestor?', max_chars = 32, placeholder = 'GESTOR')
    equipe = st.selectbox('Qual equipe realizou a venda?', options = equipes)
    tipo = st.selectbox('Qual tipo de venda?', options = tipo_vendas)
    uf = st.selectbox('Qual a UF da venda?', options = UFS)
    email = st.text_input('Qual o email do cliente?', max_chars = 32, placeholder = 'EMAIL')
    quantidade_de_produtos = st.number_input('Qual a quantidade de produtos vendidos?', min_value = 1, max_value = 100, placeholder = 'Quantidade')

    return cnpj, ddd, telefone, consultor, data, gestor, equipe, tipo, uf, email, quantidade_de_produtos

def formatar_cnpj(cnpj):
    cnpj = cnpj.zfill(14)

    cnpj_formatado = '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])
    return cnpj_formatado

def formatar_telefone(telefone):
    telefone = telefone.replace('.0','')
    return telefone

def remover_ponto(string):
    string = string.replace('.', '')
    return string

def formatar_nome(nome):
    nome = nome.split(' ')
    if len(nome) <= 1:
        return nome[0]
    
    if nome[1] == 'DOS' or nome[1] == 'DA' or nome[1] == 'DE': 
        nome_final = f'{nome[0]} {nome[1]} {nome[2]}'
        return nome_final
    
    nome_final = f'{nome[0]} {nome[1]}'
    return nome_final

TOKEN = getenv('tokenFreecel')

headers = {
    'Authorization': f'Bearer {TOKEN}'
}

rankings_url = 'https://freecelapi-b44da8eb3c50.herokuapp.com/rankings'
stats_url = 'https://freecelapi-b44da8eb3c50.herokuapp.com/stats'
vendas_url = 'https://freecelapi-b44da8eb3c50.herokuapp.com/vendas'
consultores_url = 'https://freecelapi-b44da8eb3c50.herokuapp.com/consultores/'
produtos_url = 'https://freecelapi-b44da8eb3c50.herokuapp.com/produtos'

months = [
    'Todos',
    'Janeiro', 
    'Fevereiro', 
    'Março', 
    'Abril',
    'Maio', 
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro'
]

month_by_numbers = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

tipo_vendas = ["FIXA", "AVANÇADA", "MIGRAÇÃO PRÉ-PÓS", "VVN","ALTAS"]
equipes = ['FREECEL', 'VALPARAISO', 'PARCEIRO', 'ESCRITORIO']

UFS = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO"
]

order = [
    'ID', 'CNPJ', 'Plano', 'Tipo', 'Volume', 'Preço', 'Receita', 
    'Consultor', 'CEP', 'UF', 'Município', 'Bairro', 'Telefone', 'Email', 'Ano', 'Mês', 'Data',
    'Equipe', 'Gestor', 'CNAE', 'Faturamento', 'Quadro de Funcionários', 'Capital', 'Porte',
    'Natureza Jurídica', 'Matriz', 'Situação Cadastral', 'Regime Tributário'
]

DDDS = [
    '61', '62', '64', '65', '67', '82', '71', '73', '74', '75', '77', '85', '88', '98', '99', '83',
    '81', '87', '86', '89', '84', '79', '68', '96', '92', '97', '91', '93', '94', '69', '95', '63', 
    '27', '28', '31', '32', '33', '34', '35', '37', '38', '21', '22', '24', '11', '12', '13', '14', 
    '15', '16', '17', '18', '19', '41', '42', '43', '44', '45', '46', '51', '53', '54', '55', '47', '48', '49'
]

DDDS_valor_inteiro = [
    '61', '62', '63', '64', '65', '66', '67', '68', '69', '91', '92', '93', '94', '95', '96,' '97', '98', '99'
]

values_to_remove = [
    'CNAE', 'Faturamento', 'Quadro de Funcionários', 'Capital', 'Porte', 'Natureza Jurídica', 
    'Matriz', 'Situação Cadastral', 'Regime Tributário', 'Ano', 'Mês'
]

default_index = list(filter(lambda x: x not in values_to_remove, order))
