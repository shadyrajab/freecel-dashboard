from utils.utils import (
    months, 
    tipo_vendas, 
    equipes, 
    UFS, 
    DDDS, 
    order, 
    default_index, 
    formatar_nome
)

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

@st.cache_data
def load_data():
    vendas = Vendas().data.astype(str)
    consultores = Stats.consultores()
    produtos = Stats.produtos()

    return vendas, consultores, produtos

vendas, consultores, produtos = load_data()

# Criar formulário para a adição de vendas na API
def get_form():
    cnpj = st.text_input('Qual CNPJ do cliente?', max_chars = 14, placeholder = 'CNPJ')
    ddd = st.selectbox('Qual DDD do cliente?', options = DDDS)
    telefone = st.text_input('Qual telefone do cliente? (Com DDD)', max_chars = 11, placeholder = 'TELEFONE')
    consultor = st.selectbox('Qual o nome do consultor que realizou a venda?', options = consultores)
    data = st.date_input('Qual a data da venda?', format = 'DD/MM/YYYY', max_value = today)
    gestor = st.text_input('Qual nome do gestor?', max_chars = 32, placeholder = 'GESTOR')
    equipe = st.selectbox('Qual equipe realizou a venda?', options = equipes)
    tipo = st.selectbox('Qual tipo de venda?', options = tipo_vendas)
    uf = st.selectbox('Qual a UF da venda?', options = UFS)
    email = st.text_input('Qual o email do cliente?', max_chars = 32, placeholder = 'EMAIL')
    quantidade_de_produtos = st.text_input('Qual a quantidade de produtos vendidos?', max_chars = 2, placeholder = 'Quantidade')

    return cnpj, ddd, telefone, consultor, data, gestor, equipe, tipo, uf, email, quantidade_de_produtos

# Painel de vendas
with st.container(border = True):
    # Filtro para o painel 
    with st.expander('Adicionar Filtro'):
         with st.form('filtro_vendas'):
            ano = st.multiselect(label = 'Ano', options = list(vendas['ano'].unique()))
            mes = st.multiselect(
                label = 'Mês', 
                options = sorted(
                    list(vendas['mês'].unique()), 
                    key = lambda x: months.index(x)
                )
            )
            tipo = st.multiselect(label = 'Tipo', options = list(vendas['tipo'].unique()))
            consultor = st.multiselect(label = 'Consultor', options = list(vendas['consultor'].unique()))
            plano = st.multiselect(label = 'Plano', options = list(vendas['plano'].unique()))
            uf = st.multiselect(label = 'UF', options = list(vendas['uf'].unique()))
            municipio = st.multiselect(label = 'Município', options = list(vendas['municipio'].unique()))
            equipe = st.multiselect(label = 'Equipe', options = list(vendas['revenda'].unique()))
            default_index = st.multiselect(
                label = 'Selecionar colunas', 
                options = vendas.columns.to_list(), 
                default = default_index
            )
            
            submit = st.form_submit_button('Filtrar')

            if submit:
                # Criar uma máscara booleana para cada condição de filtro
                mask_ano = vendas['ano'].isin(ano) if len(ano) else True
                mask_mes = vendas['mês'].isin(mes) if len(mes) else True
                mask_tipo = vendas['tipo'].isin(tipo) if len(tipo) else True
                mask_consultor = vendas['consultor'].isin(consultor) if len(consultor) else True
                mask_plano = vendas['plano'].isin(plano) if len(plano) else True
                mask_uf = vendas['uf'].isin(uf) if len(uf) else True
                mask_municipio = vendas['municipio'].isin(municipio) if len(municipio) else True
                mask_equipe = vendas['revenda'].isin(equipe) if len(equipe) else True

                mask = mask_ano & mask_mes & mask_tipo & mask_consultor & mask_uf & mask_municipio & mask_equipe
                
                if type(mask) == bool:
                    vendas = vendas
                else:
                    vendas = vendas[mask]

                columns_ordered = sorted(default_index, key = lambda x: order.index(x))
                vendas = vendas[columns_ordered]

    # Formatando o index e formato das colunas do dataframe
    vendas = vendas[default_index]
    vendas['quantidade_de_produtos'] = vendas['quantidade_de_produtos'].astype(int)
    vendas['valor_acumulado'] = vendas['valor_acumulado'].astype(float)
    vendas['data'] = pd.to_datetime(vendas['data'])
    vendas[['consultor', 'gestor']] = vendas[['consultor', 'gestor']].map(formatar_nome)
    vendas['email'] = vendas['email'].apply(lambda email: email.lower() if email != 'Não Informado' else email)

    # Alterando o estilo do dataframe
    vendas = vendas.style.apply(lambda x: ['background-color: white']*len(x), axis=0)
    
    # Exibindo e configurando o Painel de Vendas
    st.dataframe(
        data = vendas, 
        hide_index = True,
        use_container_width = True,
        column_config = {
            "quantidade_de_produtos": st.column_config.ProgressColumn(
                label = "Volume",
                help = "Quantidade de Produtos Vendidos.",
                format = "%f",
                min_value = 0,
                max_value = 10,
            ),
            "valor_do_plano": st.column_config.NumberColumn(
                label = "Preço",
                help = "Valor do Plano Vendido",
                format = "R$ %f",
                min_value = 0,
                max_value = 600
            ),
            "valor_acumulado": st.column_config.ProgressColumn(
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
        novo, migracao = st.tabs(['Novo', 'Migração'])

        today = datetime.today().date()

        with novo:
            with st.form('adicionar_venda_novo', clear_on_submit = True):
                cnpj, ddd, telefone, consultor, data, gestor, equipe, tipo, uf, email, quantidade_de_produtos = get_form()
                plano = st.selectbox('Qual nome do plano vendido?', options = produtos)
                token = st.text_input('Informe seu token de acesso à API.', type = 'password', placeholder = 'TOKEN')
                submit = st.form_submit_button('Adicionar')
                
                if submit:
                    valor_do_plano = produtos[produtos['nome'] == plano]['preco'].iloc[0]
                    status_code = Vendas.add_venda(
                        cnpj = cnpj, ddd = ddd, telefone = telefone, consultor = consultor, data = data, 
                        gestor = gestor, plano = plano, quantidade_de_produtos = quantidade_de_produtos, 
                        equipe = equipe, tipo = tipo, uf = uf, email = email, valor_do_plano = valor_do_plano,
                        token = token
                    )

                    if status_code == 200:

                        st.success('Venda adicionada com sucesso.')

                    else:
                        st.error('Ocorreu um erro ao adicionar esta venda.')

        with migracao:
            with st.form('adicionar_venda_migracao', clear_on_submit = True):
                cnpj, ddd, telefone, consultor, data, gestor, equipe, tipo, uf, email, quantidade_de_produtos = get_form()
                plano = st.text_input('Qual nome do plano vendido?', max_chars = 30, placeholder = 'PLANO')
                valor_do_plano = st.text_input('Qual valor do plano? (Informe o valor integral)', max_chars = 8, placeholder = 'VALOR')
                token = st.text_input('Informe seu token de acesso à API.', type = 'password', placeholder = 'TOKEN')
                submit = st.form_submit_button('Adicionar')

                if submit:
                    status_code = Vendas.add_venda(
                        cnpj = cnpj, ddd = ddd, telefone = telefone, consultor = consultor, data = data, 
                        gestor = gestor, plano = plano, quantidade_de_produtos = quantidade_de_produtos, 
                        equipe = equipe, tipo = tipo, uf = uf, email = email, valor_do_plano = valor_do_plano,
                        token = token
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