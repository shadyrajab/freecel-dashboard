import plotly.express as px
import plotly.graph_objects as go

from utils.movel_utils import group_and_concat

def plot_movel(dataframe, general = True | False):
    fig = go.Figure()
    dataframe_final, anos = group_and_concat(dataframe)

    fig.update_layout(title = f'Vendas Concluídas - Geral',
        xaxis_title = 'Mês',
        yaxis_title = 'Receita Total',
        transition_duration=50
        # yaxis = dict(
        #     tickmode = 'array',
        #     tickvals = [2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000, 18000, 20000, 22000, 24000, 26000, 28000, 30000, 32000, 34000],
        #     ticktext = ['2K R$', '4K R$', '6K R$', '8K R$', '10K R$', '12K R$', '14K R$', '16K R$', '18K R$', '20K R$', '22K R$', '24K R$', '26K R$', '28K R$', '30K R$', '32K R$', '34K R$']
        # )
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