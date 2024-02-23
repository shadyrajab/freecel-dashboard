import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def plot_rankings(
    dataframe, title, line = None
):
    y = 'plano' if title == 'Planos' else "consultor"
    color = ["yellow", "orange", "red"] if title == 'Planos' else ["red", "blue", "#3E35AB"]

    fig = go.Figure(
        px.bar(
            dataframe,
            y = y,
            x = 'valor_acumulado',
            orientation = 'h',
            title = title,
            hover_data = ['valor_acumulado', 'quantidade_de_produtos'],
            color = 'valor_acumulado',
            text_auto = '.1s',
            range_color = [dataframe['valor_acumulado'].min(), dataframe['valor_acumulado'].max()],
            color_continuous_scale = color,
        )
    )

    if line:
        media_vendas = dataframe['valor_acumulado'].mean()
        print(media_vendas)

        # Adicionar linha separadora para a média de vendas
        fig.add_vline(x=media_vendas, label=dict(text='Média', textposition='middle', yanchor="top", font=dict(size=14, color="black")))

    fig.update_layout(
        yaxis = dict(autorange = "reversed"),
        plot_bgcolor="#ffffff", 
        paper_bgcolor = "#ffffff",
        bargap = 0.2,
    )
    fig.update_traces(
        texttemplate='%{x:.1f}', 
        textposition='outside',
    )

    st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)