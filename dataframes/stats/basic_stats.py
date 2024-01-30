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

def get_rankings_consultores(ano, mes, tipo, key):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes) 
    ]

    if tipo != 'GERAL':
        dataframe = dataframe[dataframe['TIPO'] == tipo]

    ranking_consultores = dataframe.groupby('CONSULTOR', as_index = False).sum(numeric_only = True).sort_values(by = [key], ascending = False).reset_index()

    return ranking_consultores[0:16]

def get_media_mensal_por_consultor(ano, mes):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes) 
    ]

    consultores = len(list(dataframe['CONSULTOR'].unique()))
    valor_total = dataframe['VALOR ACUMULADO'].sum()

    media = valor_total / consultores

    return int(media) 

def get_delta_mensal_por_consultor(ano, mes):
    if ano == 2022 and mes == 'Janeiro':
        return 0
    
    ano_delta = ano - 1 if mes == 'Janeiro' else ano
    index_mes_passado = meses.index(mes) - 1
    mes_delta = meses[index_mes_passado]

    media_atual = get_media_mensal_por_consultor(ano, mes)
    media_mes_passado = get_media_mensal_por_consultor(ano_delta, mes_delta)

    return media_atual - media_mes_passado

def get_media_mensal_diaria(ano, mes):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes) 
    ]

    valor_total = dataframe['VALOR ACUMULADO'].sum()

    media = valor_total / 30

    return int(media)

def get_delta_mensal_diaria(ano, mes):
    if ano == 2022 and mes == 'Janeiro':
        return 0
    
    ano_delta = ano - 1 if mes == 'Janeiro' else ano
    index_mes_passado = meses.index(mes) - 1
    mes_delta = meses[index_mes_passado]

    media_atual = get_media_mensal_diaria(ano, mes)
    media_mes_passado = get_media_mensal_diaria(ano_delta, mes_delta)

    return media_atual - media_mes_passado

def get_ticket_medio_mensal(ano, mes):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['MÊS'] == mes) 
    ]

    valor_total = dataframe['VALOR ACUMULADO'].sum()

    ticket_medio = valor_total / dataframe.shape[0]

    return int(ticket_medio)

def get_delta_ticket_medio_mensal(ano, mes):
    if ano == 2022 and mes == 'Janeiro':
        return 0
    
    ano_delta = ano - 1 if mes == 'Janeiro' else ano
    index_mes_passado = meses.index(mes) - 1
    mes_delta = meses[index_mes_passado]

    media_atual = get_ticket_medio_mensal(ano, mes)
    media_mes_passado = get_ticket_medio_mensal(ano_delta, mes_delta)

    return media_atual - media_mes_passado

def get_vendas_mensais_por_consultor(ano, consultor):
    dataframe = dataframe_geral[
        (dataframe_geral['ANO'] == ano) &
        (dataframe_geral['CONSULTOR'] == consultor)
    ]

    dataframe = add_static_values(dataframe)

    vendas_mensais = dataframe.groupby('MÊS').sum(numeric_only = True)
    vendas_mensais_T = vendas_mensais.T

    vendas_mensais = vendas_mensais_T[meses].T.reset_index()

    return vendas_mensais


def add_static_values(dataframe):
    dataframe = dataframe[['MÊS', 'ANO', 'QUANTIDADE DE PRODUTOS', 'VALOR ACUMULADO']]

    for mes in meses:
        static = pd.DataFrame({
            'MÊS': [mes],
            'ANO': [2023],
            'QUANTIDADE DE PRODUTOS': [0],
            'VALOR ACUMULADO': [0]

        })

        dataframe = pd.concat([static, dataframe])

    return dataframe