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

def altas_e_migracoes(ano, revenda, tipo, aggregate = True | False):
    ano = int(ano) if ano.isnumeric() else ano
    df_altas_e_migracoes = df_movel[
        (df_movel['ANO'] == ano if ano != 'Todos' else df_movel['ANO'] == df_movel['ANO']) &
        (df_movel['REVENDA'] == revenda if revenda != 'Todos' else df_movel['REVENDA'] == df_movel['REVENDA']) &
        (df_movel['TIPO VENDA'] == tipo if tipo != 'GERAL' else df_movel['TIPO VENDA'] == df_movel['TIPO VENDA'])
    ]

    if aggregate:
        df_altas_e_migracoes = df_altas_e_migracoes.groupby('MÊS', as_index=False, sort=False).sum(numeric_only=True)

    return df_altas_e_migracoes