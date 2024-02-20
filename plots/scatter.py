import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def plot_line(dataframe, consultor):  
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dataframe['data'],
            y=dataframe['valor_acumulado'],
            mode='lines+markers',
            name='2023',
            line=dict(color="firebrick", width=2),
            fill='tozeroy',  # Preencher abaixo da linha
            fillcolor='rgba(255, 0, 0, 0.2)'  # Cor de preenchimento vermelha com transparência
        )
    )

    fig.update_layout(
        title=f'Vendas anuais por mês - {consultor}',
        xaxis_title='Mês',
        yaxis_title='Receita',
        plot_bgcolor='white',  # Cor de fundo do gráfico
        font=dict(color='black'),  # Cor do texto
        margin=dict(l=50, r=50, t=80, b=50),  # Margens do gráfico
        hovermode='x',  # Modo de exibição de informações ao passar o mouse
        xaxis=dict(
            tickmode='linear',
            dtick='M1',  # Define o espaçamento entre os ticks para 1 mês
            tickformat='%b\n%Y'  # Formato de exibição dos ticks (abreviação do mês e ano)
        ),
        yaxis=dict(range=[0, dataframe['valor_acumulado'].max() * 1.1])
    )

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)