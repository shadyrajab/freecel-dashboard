import pandas as pd

df_fixa = pd.read_excel('dataframes/vendas concluidas - fixa - 2023 e 2022.xlsx')

def fixa_avancada(revenda, ano, tipo, aggregate = True | False):
    df_fixa_avancada = df_fixa[
        (df_fixa['ANO'] == int(ano) if (
            ano != 'Todos' and ano != 'Geral'
        ) else df_fixa['ANO'] == df_fixa['ANO']) &
        (df_fixa['REVENDA'] == revenda if revenda != 'Geral' else df_fixa['REVENDA'] == df_fixa['REVENDA']) &
        (df_fixa['TIPO'] == tipo if tipo != 'GERAL' else df_fixa['TIPO'] == df_fixa['TIPO'])
    ]

    if aggregate:
        df_fixa_avancada = df_fixa_avancada.groupby('MÊS', as_index=False, sort=False).sum(numeric_only=True)

    return df_fixa_avancada