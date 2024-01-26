import pandas as pd 

df_movel = pd.read_excel('dataframes/vendas concluidas - movel - 2023 e 2022.xlsx')

df_movel.replace({
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

df_movel.rename(columns={
    'TIPO VENDA': 'TIPO'
}, inplace=True)


def altas_e_migracoes(revenda, ano, tipo, aggregate = True | False):
    df_altas_e_migracoes = df_movel[
        (df_movel['ANO'] == int(ano) if (
            ano != 'Todos' and ano != 'Geral'
        ) else df_movel['ANO'] == df_movel['ANO']) &
        (df_movel['REVENDA'] == revenda if revenda != 'Geral' else df_movel['REVENDA'] == df_movel['REVENDA']) &
        (df_movel['TIPO'] == tipo if tipo != 'GERAL' else df_movel['TIPO'] == df_movel['TIPO'])
    ]

    if aggregate:
        df_altas_e_migracoes = df_altas_e_migracoes.groupby('MÊS', as_index=False, sort=False).sum(numeric_only=True)

    return df_altas_e_migracoes