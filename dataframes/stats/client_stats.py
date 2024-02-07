import pandas as pd

# from dataframes.objects import dataframe_geral

dataframe_geral = pd.read_excel('dataframes/excel/df_full.xlsx')

dataframe_geral.replace({
    'd': '3 A 9 COLABORADORES',
    'n': 'R$ 81001,00 a R$ 3600000,00'
}, inplace = True)

def get_cnaes():
    cnae_values = dataframe_geral[['NOME CNAE', 'COD CNAE']].value_counts().reset_index()

    cnae_df = pd.DataFrame(cnae_values)

    cnae_df.rename(columns = {
        'count': 'QUANTIDADE VENDIDA'
    }, inplace = True)

    return cnae_df

def get_faturamentos():
    faturamentos = dataframe_geral['FATURAMENTO'].value_counts().reset_index()

    df_faturamentos = pd.DataFrame(faturamentos)

    df_faturamentos.rename(columns = {
        'count': 'QUANTIDADE VENDIDA'
    }, inplace = True)

    return df_faturamentos

def get_funcionarios():

    funcionarios = dataframe_geral['COLABORADORES'].value_counts().reset_index()

    df_funcionarios = pd.DataFrame(funcionarios)

    df_funcionarios.rename(columns = {
        'count': 'QUANTIDADE VENDIDA'
    }, inplace = True)

    return df_funcionarios