import pandas as pd

# from dataframes.objects import dataframe_geral

dataframe_movel = pd.read_excel('dataframes/excel/vendas concluidas - movel - 2023 e 2022.xlsx')
dataframe_fixa = pd.read_excel('dataframes/excel/vendas concluidas - fixa - 2023 e 2022.xlsx')
dataframe_geral = pd.concat([dataframe_movel, dataframe_fixa])

dataframe_geral.replace({
    'd': '3 A 9 COLABORADORES',
    'n': 'R$ 81001,00 a R$ 3600000,00'
}, inplace = True)

def get_cnaes():
    cnae_values = dataframe_geral['CNAE'].value_counts().reset_index()

    cnae_df = pd.DataFrame(cnae_values)

    def formatar_cnae(cnae):

        try:
            cnae = cnae.split(' - ')

            return [cnae[0], cnae[1]]
        
        except:
            return 'undefined'
    
    cnae_df['CÓDIGO'] = cnae_df['CNAE'].apply(lambda cnae: formatar_cnae(cnae)[0])
    cnae_df['NOME'] = cnae_df['CNAE'].apply(lambda cnae: formatar_cnae(cnae)[1])

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