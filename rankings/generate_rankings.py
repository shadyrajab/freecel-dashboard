import pandas as pd

df_fixa = pd.read_excel('dataframes/vendas concluidas - fixa - 2023 e 2022.xlsx')
df_fixa = df_fixa[df_fixa['ANO'] == 2023]
df_movel = pd.read_excel('dataframes/vendas concluidas - movel - 2023 e 2022.xlsx')

months = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']

def filtrar_consultor(planilha, consultor):
    consultores = []

    for ct in consultor:
        if planilha == 'FIXA':
            dataframe = df_fixa[df_fixa['CONSULTOR'] == ct]
            fixa = add_static_values(dataframe, 2022)
            consultores.append(fixa)

        if planilha == 'MÓVEL':
            consultores.append(consultor = df_movel[df_movel['CONSULTOR'] == ct])

    return consultores

def add_static_values(dataframe, ano):
    for month in months:
        static_values = pd.DataFrame({'UF': ['STATIC'], 
            'CNPJ': ['STATIC'], 
            'MÊS': [month], 
            'ANO': [ano], 
            'TIPO': ['STATIC'], 
            'VALOR DO PLANO': [0],
            'QUANTIDADE DE PRODUTOS': [0],
            'VALOR ACUMULADO': [0],
            'GESTOR': [0],
            'CONSULTOR': [0],
            'REVENDA': [0] 
        })

        dataframe = pd.concat([dataframe, static_values])

    return dataframe