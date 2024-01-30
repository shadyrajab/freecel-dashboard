from dataframes.objects import dataframe_geral, meses
import pandas as pd

def get_receita_total(retorno, ano = None, mes = None, escritorio = None, consultor = None):
    dataframe = dataframe_geral

    if ano:
        dataframe = dataframe[dataframe['ANO'] == ano]

    if mes:
        dataframe = dataframe[dataframe['MÊS'] == mes]

    if escritorio and escritorio != 'Todos':
        dataframe = dataframe[dataframe['REVENDA'] == escritorio]
    
    if consultor:
        dataframe = dataframe[dataframe['CONSULTOR'] == consultor]

    return dataframe[retorno].sum()

def get_consultor_do_mes(ano, mes):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes) 
    ]

    ranking_consultores = dataframe.groupby('CONSULTOR', as_index = False).sum(numeric_only = True)
    maior_valor_vendido = ranking_consultores['VALOR ACUMULADO'].max()
    consultor_do_mes = ranking_consultores[ranking_consultores['VALOR ACUMULADO'] == maior_valor_vendido]

    return consultor_do_mes

def get_maior_venda_mes(key):
    dataframe = dataframe_geral
    dataframe['DATA'] = dataframe['MÊS'] + dataframe_geral['ANO'].astype(str)
    dataframe = dataframe.groupby('DATA', as_index = False).sum(numeric_only = False)

    return dataframe[key].max()

def get_maior_venda_consultor(ano):
   ranking_consultores = get_ranking_meses(ano, 'CONSULTOR')

   return ranking_consultores['VALOR MÁXIMO'].max()

def get_maior_venda_escritorio(ano):
    ranking_escritorio = get_ranking_meses(ano, 'REVENDA')

    return ranking_escritorio['VALOR MÁXIMO'].max()

def get_ranking_meses(ano, key):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) 
    ]

    def valor_maximo(mes):
        df_mes = dataframe[dataframe['MÊS'] == mes]
        df_grouped = df_mes.groupby(key, as_index = False).sum(numeric_only = True)

        return df_grouped['VALOR ACUMULADO'].max()
    
    ranking_meses = pd.DataFrame(meses)
    ranking_meses.rename(columns = {0: 'MÊS'}, inplace = True)
    ranking_meses['VALOR MÁXIMO'] = ranking_meses['MÊS'].apply(lambda m: valor_maximo(m))

    return ranking_meses

def get_rankings_consultores(ano, mes, tipo):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes) 
    ]

    if tipo != 'GERAL':
        dataframe = dataframe_geral[dataframe_geral['TIPO'] == tipo]

    ranking_consultores = dataframe.groupby('CONSULTOR', as_index = False).sum(numeric_only = True).sort_values(by = ['VALOR ACUMULADO'], ascending = False).reset_index()

    return ranking_consultores[0:16]

def get_media_mensal_por_consultor(ano, mes):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes) 
    ]

    consultores = len(list(dataframe['CONSULTOR'].unique()))
    valor_total = dataframe['VALOR ACUMULADO'].sum()

    media = valor_total / consultores

    return 'R$ ' + str(int(media)) 

def get_media_mensal_diaria(ano, mes):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes) 
    ]

    valor_total = dataframe['VALOR ACUMULADO'].sum()

    media = valor_total / 30

    return 'R$ ' + str(int(media)) 

def get_ticket_medio_mensal(ano, mes):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes) 
    ]

    valor_total = dataframe['VALOR ACUMULADO'].sum()

    ticket_medio = valor_total / dataframe.shape[0]

    return 'R$ ' + str(int(ticket_medio)) 