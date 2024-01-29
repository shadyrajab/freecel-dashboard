import pandas as pd

dataframe_movel = pd.read_excel('dataframes/excel/vendas concluidas - movel - 2023 e 2022.xlsx')
dataframe_fixa = pd.read_excel('dataframes/excel/vendas concluidas - fixa - 2023 e 2022.xlsx')
dataframe_geral = pd.concat([dataframe_movel, dataframe_fixa])

dataframe_geral.replace({
    'JÁ CLIENTE': 'ALTAS', 
    'NOVO': 'ALTAS', 
    'PORTABILIDADE': 'ALTAS',
    'PORTABILIDADE PF + TT PF/PJ - VIVO TOTAL': 'ALTAS',
    'INTERNET': 'ALTAS',
    'PORTABILIDADE - VIVO TOTAL': 'ALTAS',
    'PORTABILIDADE PF + TT PF/PJ': 'ALTAS',
    'NOVO - VIVO TOTAL': 'ALTAS',
    'PORTABILIDADE CNPJ – CNPJ': 'ALTAS',

    'MIGRAÇÃO PRÉ/PÓS': 'MIGRAÇÃO PRÉ-PÓS',
    'MIGRAÇÃO PRÉ/PÓS - VIVO TOTAL': 'MIGRAÇÃO PRÉ-PÓS',

    'MIGRAÇÃO': 'MIGRAÇÃO PRÉ-PÓS'

}, inplace=True)

dataframe_geral.replace({
    'JAN': 'Janeiro',
    'FEV': 'Fevereiro', 
    'MAR': 'Março', 
    'ABR': 'Abril',
    'MAI': 'Maio',
    'JUN': 'Junho',
    'JUL': 'Julho',
    'AGO': 'Agosto',
    'SET': 'Setembro',
    'OUT': 'Outubro',
    'NOV': 'Novembro',
    'DEZ': 'Dezembro'
}, inplace = True)

def formatar_nome(nome):
    nome_splited = nome.split(' ')
    try:
        nome = nome_splited[0] + ' ' + nome_splited[1]
    except:
        pass

    return nome

dataframe_geral['CONSULTOR'] = dataframe_geral['CONSULTOR'].apply(lambda n: formatar_nome(n))


meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

def get_years():
    return list(dataframe_geral['ANO'].unique())

def get_months(ano):
    dataframe = dataframe_geral[dataframe_geral['ANO'] == ano]

    return list(dataframe['MÊS'].unique())

def get_consultores():
    return list(dataframe_geral['CONSULTOR'].unique())

def get_escritorios():
    return list(dataframe_geral['REVENDA'].unique())

def grouped_by_mes(planilha, ano):
    dataframe = ''
    match planilha:
        case 'GERAL':
            dataframe = dataframe_geral[dataframe_geral['ANO'] == ano]
        
        case 'FIXA':
            dataframe = dataframe_fixa[dataframe_fixa['ANO'] == ano]

        case 'MÓVEL':
            dataframe = dataframe_movel[dataframe_movel['ANO'] == ano]

    grouped_dataframe = dataframe.groupby('MÊS', as_index = False).sum(numeric_only = True)
    grouped_dataframe['ANO'] = ano

    return grouped_dataframe
