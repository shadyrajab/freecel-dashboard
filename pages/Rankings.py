import streamlit as st 
from rankings.generate_rankings import filtrar_consultor
import plotly.express as px
import plotly.graph_objects as go

st.title('Ranking Consultores - 2022 e 2023')
st.write('---------------------------------------')

st.write('#### Avançada ')
tab_fixa, tab_avancada, tab_soho, tab_vvn = st.tabs(['GERAL', 'AVANÇADA', 'SOHO', 'VVN'])

st.write('#### Móvel ')
tab_movel, tab_altas, tab_migracao = st.tabs(['GERAL', 'ALTAS', 'MIGRAÇÃO PRÉ-PÓS'])

consultor_selecionado = st.sidebar.multiselect('Selecionar Consultores', ['CAIQUE RIBEIRO GUEDES', 'LUIZ CESAR AGUIAR DE LEMOS', 'PEDRO HENRIQUE', 'FLAVIO HENRIQUE LEMOS DOS NASCIMENTO', 'WILLIAM GOMIDES DE MORAES', 'ANA CAROLINE BORGES DE MORAIS'])

with tab_fixa:
    consultores = filtrar_consultor('FIXA', consultor_selecionado)

    fig = go.Figure()

    for consultor in consultores:
        dataframe = consultor.groupby(
            'MÊS', sort=False).sum(numeric_only=True
        )

        dataframe = dataframe.T[['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']]
        dataframe = dataframe.T
        dataframe = dataframe.reset_index()

        fig.add_trace(
            go.Scatter(
                x = dataframe['MÊS'],
                y = dataframe['VALOR ACUMULADO']
            )
        )

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
