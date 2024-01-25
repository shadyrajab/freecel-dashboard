import plotly.express as px
import plotly.graph_objects as go

from utils.movel_utils import group_and_concat

def plot_movel(dataframe, general = True | False):
    fig = go.Figure()
    dataframe_final, anos = group_and_concat(dataframe)
    fig.update_layout(title = f'Vendas Concluídas - Geral',
        xaxis_title = 'Mês',
        yaxis_title = 'Receita Total'
    )

    if general:
        dataframe = dataframe.groupby(
            'MÊS', as_index=False, sort=False).sum(numeric_only=True
        )
        fig.add_trace(
            go.Scatter(
                x = dataframe['MÊS'], y = dataframe['VALOR ACUMULADO']
            )
        )

        return fig

    else:
        for ano in anos:
            dataframe_figure = dataframe_final[dataframe_final['ANO'] == ano]
            fig.add_trace(
                go.Scatter(
                    x = dataframe_figure['MÊS'], y = dataframe_figure['VALOR ACUMULADO'], name = str(ano)
                )
            )

        return fig