from dotenv import load_dotenv
from os import getenv

load_dotenv()

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
    'id', 'cnpj', 'plano', 'tipo', 'quantidade_de_produtos', 'valor_do_plano', 'valor_acumulado', 
    'consultor', 'cep', 'uf', 'municipio', 'bairro', 'telefone', 'email', 'ano', 'mês', 'data',
    'revenda', 'gestor', 'cnae', 'faturamento', 'quadro_funcionarios', 'capital_social', 'porte',
    'natureza_juridica', 'matriz', 'situacao_cadastral', 'regime_tributario'
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