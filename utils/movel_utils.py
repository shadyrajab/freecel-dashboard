import pandas as pd 

def group_and_concat(dataframe):
    concat_list = []

    anos = list(dataframe['ANO'].unique())

    for ano in anos:
        dataframe_ano = dataframe[dataframe['ANO'] == ano]
        dataframe_grouped = dataframe_ano.groupby(
            'MÊS', as_index=False, sort=False).sum(numeric_only=True
        )

        dataframe_grouped['ANO'] = ano

        concat_list.append(dataframe_grouped)
    
    dataframe_final = pd.concat(concat_list)

    return [dataframe_final, anos]

