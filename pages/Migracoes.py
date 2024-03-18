import asyncio
from datetime import datetime
from math import ceil

import pandas as pd
import streamlit as st

from dataframe.stats import Stats
from dataframe.vendas import Vendas
from utils.utils import (
    STATUS,
    UFS,
    colorir_adabas,
    colorir_equipes,
    colorir_null_values,
    colorir_tipo_venda,
    compare_and_update,
    default_index,
    equipes,
    formatar_nome,
    mask_dataframe,
    months,
    tipo_vendas,
    order,
    new_order
)

# Configurando o layout da página
st.set_page_config(
    page_title="Vendas - Freecel",
    page_icon="https://i.imgur.com/pidHoxz.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "https://github.com/shadyrajab/freecel-dashboard"},
)

with open("styles/vendas.css", "r") as styles:
    css = styles.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


async def load_data():
    async def load_vendas():
        return Vendas().migracoes.astype(str)

    async def load_consultores():
        return Stats.consultores()

    async def load_produtos():
        return Stats.produtos()

    tasks = [load_vendas(), load_consultores(), load_produtos()]
    vendas, consultores, produtos = await asyncio.gather(*tasks)
    return vendas, consultores, produtos


# Sistema de paginação do DataFrame
def split_frame(df, rows):
    df.reset_index(drop=True, inplace=True)
    dataframe = [df.loc[i : i + rows - 1, :] for i in range(0, len(df), rows)]
    return dataframe


vendas, consultores, produtos = asyncio.run(load_data())
st.session_state["cnpj"] = ""
st.session_state["n_pedido"] = ""
# Painel de Filtragem dos Dados
with st.sidebar:
    ano = st.multiselect(label="Ano", options=list(vendas["Ano"].unique()))
    mes = st.multiselect(
        label="Mês",
        options=sorted(list(vendas["Mês"].unique()), key=lambda x: months.index(x)),
    )
    tipo = st.multiselect(label="Tipo", options=list(vendas["Tipo"].unique()))
    status = st.multiselect(label="Status", options=list(vendas["Status"].unique()))
    consultor = st.multiselect(
        label="Consultor", options=list(vendas["Consultor"].unique())
    )
    plano = st.multiselect(label="Plano", options=list(vendas["Plano"].unique()))
    m = st.multiselect(label="M", options=list(vendas["M"].unique()))
    uf = st.multiselect(label="UF", options=list(vendas["UF"].unique()))
    municipio = st.multiselect(
        label="Município", options=list(vendas["Município"].unique())
    )
    equipe = st.multiselect(label="Equipe", options=list(vendas["Equipe"].unique()))
    adabas = st.multiselect(label="ADABAS", options=list(vendas["ADABAS"].unique()))
    default_index = st.multiselect(
        label="Selecionar colunas",
        options=vendas.columns.to_list(),
        default=default_index(new_order),
    )
    # Criar uma máscara booleana para cada condição de filtro
    vendas = mask_dataframe(
        vendas,
        ano,
        mes,
        tipo,
        consultor,
        plano,
        equipe,
        municipio,
        uf,
        adabas,
        status,
        m,
        default_index=default_index,
        order=new_order
    )
    vendas["Volume"] = vendas["Volume"].astype(int)
    vendas["Receita"] = vendas["Receita"].astype(float)
    vendas["Preço"] = vendas["Preço"].astype(float)
    vendas["Data"] = pd.to_datetime(vendas["Data"]).dt.strftime("%d %b %Y")
    vendas[["Consultor", "Gestor"]] = vendas[["Consultor", "Gestor"]].map(formatar_nome)
    vendas["Email"] = vendas["Email"].apply(
        lambda email: email.lower() if email != "Não Informado" else email
    )

# Barra de pesquisa
menu_superior = st.columns((4, 1, 1))
with menu_superior[2]:
    st.session_state["cnpj"] = st.text_input(
        "Pesquisar CNPJ", placeholder="CNPJ", value=st.session_state["cnpj"]
    )
    if st.session_state["cnpj"]:
        vendas = vendas[vendas["CNPJ"] == st.session_state["cnpj"]]

with menu_superior[1]:
    st.session_state["n_pedido"] = st.text_input(
        "Pesquisar nº Pedido",
        placeholder="Nº Pedido",
        value=st.session_state["n_pedido"],
    )
    if st.session_state["n_pedido"]:
        vendas = vendas[vendas["Número do Pedido"] == st.session_state["n_pedido"]]
# Menu inferior para a navegação nas páginas do DataFrame
painel_de_vendas = st.container()
menu_inferior = st.columns((4, 1, 1))

with menu_inferior[2]:
    page_size = st.selectbox("Tamanho", options=[25, 50, 100])

with menu_inferior[1]:
    total_pages = ceil(len(vendas) / page_size)
    current_page = st.number_input(
        label="Página", min_value=1, max_value=total_pages, step=1
    )


with menu_inferior[0]:
    st.markdown(f"Página **{current_page}** de **{total_pages}** ")

pages = split_frame(vendas, page_size)
vendas = pages[current_page - 1]
altura = min(len(vendas) * 50, 700)
# Definindo o estilo do DataFrame
vendas = (
    vendas.style.set_properties(**{"background-color": "white"})
    .background_gradient(subset=["Receita"], cmap="Reds")
    ._compute()
    .background_gradient(subset=["Preço"], cmap="Greens")
    ._compute()
    .background_gradient(subset=["Volume"], cmap="Blues")
    ._compute()
    .background_gradient(subset=["ID"], cmap="Grays")
    ._compute()
    .map(colorir_tipo_venda, subset=["Tipo"])
    ._compute()
    .map(colorir_equipes, subset=["Equipe"])
    ._compute()
    .map(colorir_null_values, subset=["Telefone", "Email"])
    ._compute()
    .map(colorir_adabas, subset=["ADABAS"])
    ._compute()
    .format({"Preço": "R$ {:.2f}"})
)

painel = painel_de_vendas.data_editor(
    data=vendas,
    disabled=[
        "ID",
        "CNPJ",
        "Plano",
        "Preço",
        "ADABAS",
        "CEP",
        "Município",
        "Bairro",
        "Data",
        "Número do Pedido",
        "M",
        "UF",
        "DDD",
    ],
    hide_index=True,
    height=altura,
    use_container_width=True,
    column_config={
        "Volume": st.column_config.ProgressColumn(
            label="Volume",
            help="Quantidade de Produtos Vendidos.",
            format="%f",
            min_value=0,
            max_value=10,
        ),
        "Preço": st.column_config.NumberColumn(
            label="Preço",
            help="Valor do Plano Vendido",
            format="R$ %f",
            min_value=0,
            max_value=600,
        ),
        "Receita": st.column_config.ProgressColumn(
            label="Receita",
            help="Valor Total Vendido",
            format="R$ %f",
            min_value=0,
            max_value=1000,
        ),
        "Equipe": st.column_config.SelectboxColumn(
            label="Equipe",
            help="A equipe que realizou a venda",
            options=equipes,
            required=True,
        ),
        "Tipo": st.column_config.SelectboxColumn(
            label="Tipo", help="O tipo de venda", options=tipo_vendas, required=True
        ),
        "Consultor": st.column_config.SelectboxColumn(
            label="Consultor",
            help="O consultor que fez a venda",
            options=consultores,
            required=True,
        ),
        "Status": st.column_config.SelectboxColumn(
            label="Status",
            help="O status da venda",
            options=STATUS,
            required=True,
        ),
        "Já Cliente?": st.column_config.SelectboxColumn(
            label="Já Cliente?",
            help="True para Sim e False para Não",
            options=["True", "False"],
            required=True,
        ),
        "UF": st.column_config.SelectboxColumn(
            label="UF", help="A UF da venda", options=UFS, required=True
        ),
        "Telefone": st.column_config.TextColumn(
            label="Telefone", help="Telefone do Cliente", max_chars=11, required=True
        ),
    },
)

compare_and_update(vendas.data, painel)
