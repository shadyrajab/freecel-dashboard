import pandas as pd

dataframe_movel = pd.read_excel('dataframes/excel/vendas concluidas - movel - 2023 e 2022.xlsx')
dataframe_fixa = pd.read_excel('dataframes/excel/vendas concluidas - fixa - 2023 e 2022.xlsx')

dataframe_movel.replace({
    'JÁ CLIENTE': 'ALTAS', 
    'NOVO': 'ALTAS', 
    'PORTABILIDADE': 'ALTAS',
    'PORTABILIDADE PF + TT PF/PJ - VIVO TOTAL': 'ALTAS',
    'INTERNET': 'ALTAS',
    'PORTABILIDADE - VIVO TOTAL': 'ALTAS',
    'PORTABILIDADE PF + TT PF/PJ': 'ALTAS',

    'MIGRAÇÃO PRÉ/PÓS': 'MIGRAÇÃO PRÉ-PÓS',
    'MIGRAÇÃO PRÉ/PÓS - VIVO TOTAL': 'MIGRAÇÃO PRÉ-PÓS'

}, inplace=True)

dataframe_movel.replace({
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

dataframe_fixa.replace({
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

dataframe_geral = pd.concat([dataframe_movel, dataframe_fixa])

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
