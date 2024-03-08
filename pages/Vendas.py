from utils.utils import (
    months, 
    colorir_equipes, 
    default_index, 
    formatar_nome,
    get_form, 
    colorir_tipo_venda,
    mask_dataframe,
    colorir_null_values,
    colorir_adabas
)
from math import ceil
from dataframe.vendas import Vendas
from dataframe.stats import Stats
from datetime import datetime
import streamlit as st
import pandas as pd

# Configurando o layout da página
st.set_page_config(
    page_title = "Vendas - Freecel",
    page_icon = "https://i.imgur.com/pidHoxz.png",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {
        'About': "https://github.com/shadyrajab/freecel-dashboard"
    }
)

with open('styles/vendas.css', 'r') as styles:
    css = styles.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def load_data():
    vendas = Vendas().data.astype(str)
    consultores = Stats.consultores()
    produtos = Stats.produtos()

    return vendas, consultores, produtos

# Sistema de paginação do DataFrame
def split_frame(df, rows):
    df.reset_index(drop = True, inplace = True)
    dataframe = [df.loc[i : i + rows - 1, :] for i in range(0, len(df), rows)]
    return dataframe

vendas, consultores, produtos = load_data()

# Painel de Filtragem dos Dados
with st.sidebar:
    ano = st.multiselect(label = 'Ano', options = list(vendas['Ano'].unique()))
    mes = st.multiselect(
        label = 'Mês', 
        options = sorted(
            list(vendas['Mês'].unique()), 
            key = lambda x: months.index(x)
        )
    )
    tipo = st.multiselect(label = 'Tipo', options = list(vendas['Tipo'].unique()))
    consultor = st.multiselect(label = 'Consultor', options = list(vendas['Consultor'].unique()))
    plano = st.multiselect(label = 'Plano', options = list(vendas['Plano'].unique()))
    uf = st.multiselect(label = 'UF', options = list(vendas['UF'].unique()))
    municipio = st.multiselect(label = 'Município', options = list(vendas['Município'].unique()))
    equipe = st.multiselect(label = 'Equipe', options = list(vendas['Equipe'].unique()))
    adabas = st.multiselect(label = 'ADABAS', options = list(vendas['ADABAS'].unique()))
    default_index = st.multiselect(
        label = 'Selecionar colunas', 
        options = vendas.columns.to_list(), 
        default = default_index
    )
    # Criar uma máscara booleana para cada condição de filtro
    vendas = mask_dataframe(vendas, ano, mes, tipo, consultor, plano, equipe, municipio, uf, adabas, default_index)
    vendas['Volume'] = vendas['Volume'].astype(int)
    vendas['Receita'] = vendas['Receita'].astype(float)
    vendas['Preço'] = vendas['Preço'].astype(float)
    vendas['Data'] = pd.to_datetime(vendas['Data']).dt.strftime('%d %b %Y')
    vendas[['Consultor', 'Gestor']] = vendas[['Consultor', 'Gestor']].map(formatar_nome)
    vendas['Email'] = vendas['Email'].apply(lambda email: email.lower() if email != 'Não Informado' else email)

# Menu inferior para a navegação nas páginas do DataFrame
painel_de_vendas = st.container()
menu_inferior = st.columns((4, 1, 1))

with menu_inferior[2]:
    page_size = st.selectbox("Tamanho", options = [25, 50, 100])

with menu_inferior[1]:
    total_pages = ceil(len(vendas) / page_size)
    current_page = st.number_input(
        label = "Página", 
        min_value = 1,
        max_value = total_pages, 
        step = 1
    )


with menu_inferior[0]:
    st.markdown(f"Página **{current_page}** de **{total_pages}** ")

pages = split_frame(vendas, page_size)
vendas = pages[current_page - 1]
altura = min(len(vendas) * 50, 700)
# Definindo o estilo do DataFrame
vendas = (vendas.style
    .set_properties(**{'background-color': 'white'})
    .background_gradient(subset = ['Receita'], cmap = 'Reds')._compute()
    .background_gradient(subset = ['Preço'], cmap = 'Greens')._compute()
    .background_gradient(subset = ['Volume'], cmap = 'Blues')._compute()
    .background_gradient(subset = ['ID'], cmap = 'Grays')._compute()
    .map(colorir_tipo_venda, subset = ['Tipo'])._compute()
    .map(colorir_equipes, subset = ['Equipe'])._compute()
    .map(colorir_null_values, subset = ['Telefone', 'Email'])._compute()
    .map(colorir_adabas, subset = ['ADABAS'])._compute()
    .format({'Preço': 'R$ {:.2f}'})
)

painel_de_vendas.dataframe(
    data = vendas, 
    hide_index = True,
    height = altura,
    use_container_width = True,
    column_config = {
        "Volume": st.column_config.ProgressColumn(
            label = "Volume",
            help = "Quantidade de Produtos Vendidos.",
            format = "%f",
            min_value = 0,
            max_value = 10,
        ),
        "Preço": st.column_config.NumberColumn(
            label = "Preço",
            help = "Valor do Plano Vendido",
            format = "R$ %f",
            min_value = 0,
            max_value = 600
        ),
        "Receita": st.column_config.ProgressColumn(
            label = "Receita",
            help = "Valor Total Vendido",
            format = "R$ %f",
            min_value = 0,
            max_value = 1000
        ),
        "data": st.column_config.DatetimeColumn(
            label = "Data",
            help = "Data na qual a venda foi realizada",
            format = "D MMM YYYY",
        ),
        "equipe": st.column_config.Column(
            label = "Equipe",
            help = "A equipe que realizou a venda"
        )
    }
)

with st.expander('Adicionar Venda'):
    # Criando abas para adicionar vendas de acordo com o tipo de cliente
    novo, migracao = st.tabs(['Novo', 'Já cliente'])

    today = datetime.today().date()

    with novo:
        with st.form('adicionar_venda_novo', clear_on_submit = True):
            cnpj, telefone, consultor, data, gestor, equipe, tipo, email, volume = get_form(consultores, today)
            plano = st.selectbox('Qual nome do plano vendido?', options = produtos)
            token = st.text_input('Informe seu token de acesso à API.', type = 'password', placeholder = 'TOKEN')
            submit = st.form_submit_button('Adicionar')
            
            if submit:
                status_code = Vendas.add_venda(
                    cnpj = cnpj, telefone = telefone, consultor = consultor, data = data, 
                    gestor = gestor, plano = plano, volume = volume, 
                    equipe = equipe, tipo = tipo, email = email, token = token,
                    ja_cliente = False
                )

                if status_code == 200:

                    st.success('Venda adicionada com sucesso.')

                else:
                    st.error('Ocorreu um erro ao adicionar esta venda.')

    with migracao:
        with st.form('adicionar_venda_migracao', clear_on_submit = True):
            cnpj, telefone, consultor, data, gestor, equipe, tipo, email, volume = get_form(consultores, today)
            plano = st.text_input('Qual nome do plano vendido?')
            preco = st.number_input('Qual valor da migração?')
            token = st.text_input('Informe seu token de acesso à API.', type = 'password', placeholder = 'TOKEN')
            submit = st.form_submit_button('Adicionar')
            
            if submit:
                status_code = Vendas.add_venda(
                    cnpj = cnpj, telefone = telefone, consultor = consultor, data = data, 
                    gestor = gestor, plano = plano, volume = volume, 
                    equipe = equipe, tipo = tipo, email = email, token = token,
                    ja_cliente = True, preco = preco
                )

                if status_code == 200:
                    st.success('Venda adicionada com sucesso.')

                else:
                    st.error('Ocorreu um erro ao adicionar esta venda.')

with st.expander('Remover Venda'):
    with st.form('remover_venda', clear_on_submit = True):
        id_venda = st.text_input(
            label = 'Qual o ID da venda que deseja remover?',
            placeholder = 'ID'
        )

        token = st.text_input('Informe seu token de acesso à API.', type = 'password', placeholder = 'TOKEN')
        submit = st.form_submit_button('Remover')

        if submit:
            status_code = Vendas.remove_venda(id = id_venda, token = token)
            if status_code == 200:
                st.success('Venda removida com sucesso.')
            
            else:
                st.error('Ocorreu um erro ao remover esta venda.')