from os import getenv

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("tokenFreecel")

headers = {"Authorization": f"Bearer {TOKEN}"}

rankings_url = "https://freecelapi-b44da8eb3c50.herokuapp.com/rankings"
stats_url = "https://freecelapi-b44da8eb3c50.herokuapp.com/stats"
vendas_url = "https://freecelapi-b44da8eb3c50.herokuapp.com/vendas"
consultores_url = "https://freecelapi-b44da8eb3c50.herokuapp.com/consultores/"
produtos_url = "https://freecelapi-b44da8eb3c50.herokuapp.com/produtos"
migracoes_url = "https://freecelapi-b44da8eb3c50.herokuapp.com/migracoes"


def format_param(param):
    return {"True": True, "False": False}.get(param, param.upper())


def format_key(key):
    return {
        "Já Cliente?": "ja_cliente",
        "Valor Renovação": "valor_renovacao",
        "Valor Inovação": "valor_inovacao",
        "Valor Atual": "valor_atual",
        "Pacote Inovação": "pacote_inovacao",
        "Volume Inovação": "volume_inovacao"
    }.get(key, key.lower().replace(" ", "_"))


def compare_and_update(original: pd.DataFrame, updated: pd.DataFrame, type: str):
    original.set_index("ID", inplace=True)
    updated.set_index("ID", inplace=True)
    url = vendas_url if type == "Vendas" else migracoes_url
    alteracoes = original.compare(updated).reset_index()
    if len(alteracoes) > 0:
        id = int(alteracoes["ID"].iloc[0])
        key = alteracoes.columns[1][0]
        value = alteracoes[key]["other"].iloc[0]
        params = {"id": id, format_key(key): format_param(value)}

        print(params)
        response = requests.put(url, headers=headers, json=params)
        print(response.text)


def format_tab_name(string):
    string = string.lower().replace("ç", "c").replace("ã", "a")
    return string


def mask_dataframe(
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
    default_index,
    order,
):
    mask_ano = vendas["Ano"].isin(ano) if len(ano) else True
    mask_mes = vendas["Mês"].isin(mes) if len(mes) else True
    mask_tipo = vendas["Tipo"].isin(tipo) if len(tipo) else True
    mask_consultor = vendas["Consultor"].isin(consultor) if len(consultor) else True
    mask_plano = vendas["Plano"].isin(plano) if len(plano) else True
    mask_uf = vendas["UF"].isin(uf) if len(uf) else True
    mask_municipio = vendas["Município"].isin(municipio) if len(municipio) else True
    mask_equipe = vendas["Equipe"].isin(equipe) if len(equipe) else True
    mask_adabas = vendas["ADABAS"].isin(adabas) if len(adabas) else True
    mask_status = vendas["Status"].isin(status) if len(status) else True
    mask_m = vendas["M"].isin(m) if len(m) else True

    mask = (
        mask_adabas
        & mask_ano
        & mask_mes
        & mask_tipo
        & mask_consultor
        & mask_uf
        & mask_municipio
        & mask_equipe
        & mask_plano
        & mask_status
        & mask_m
    )

    if type(mask) == bool:
        vendas = vendas
    else:
        vendas = vendas[mask]

    columns_ordered = sorted(default_index, key=lambda x: order.index(x))
    vendas = vendas[columns_ordered]
    vendas = vendas[default_index]

    return vendas


def colorir_tipo_venda(val):
    cores = {
        "FIXA": "lightblue",
        "AVANÇADA": "lightgreen",
        "MIGRAÇÃO PRÉ-PÓS": "lightcoral",
        "VVN": "lightsalmon",
        "ALTAS": "lightyellow",
        "PORTABILIDADE": "lightcyan",
    }
    cor = cores.get(val, "white")
    return f"background-color: {cor}"


def colorir_adabas(val):
    cores = {
        "DFP4059-001": "azure",
        "GOP4096-001": "beige",
        "DFPAE0005-1": "bisque",
        "GOPAE0031-1": "blanchedalmond",
    }
    cor = cores.get(val, "white")
    return f"background-color: {cor}"


def colorir_equipes(val):
    cores_equipes = {
        "FREECEL": "lightblue",
        "VALPARAISO": "lightgreen",
        "PARCEIRO": "lightcoral",
        "GOIÂNIA": "lightsalmon",
    }
    cor_equipe = cores_equipes.get(val, "white")
    return f"background-color: {cor_equipe}"


def colorir_null_values(val):
    cores_null = {"Não Informado": "#f2f2f2"}
    cores_null = cores_null.get(val, "white")
    return f"background-color: {cores_null}"


def get_form(consultores, today):
    cnpj = st.text_input("Qual CNPJ do cliente?", max_chars=14, placeholder="CNPJ")
    telefone = st.text_input(
        "Qual telefone do cliente? (Com DDD)", max_chars=11, placeholder="TELEFONE"
    )
    ddd = st.selectbox("Qual DDD do cliente?", options=DDDS)
    consultor = st.selectbox(
        "Qual o nome do consultor que realizou a venda?", options=consultores
    )
    numero_pedido = st.text_input("Qual número do Pedido?", placeholder="Nº Pedido")
    data = st.date_input("Qual a data da venda?", format="DD/MM/YYYY", max_value=today)
    gestor = st.text_input("Qual nome do gestor?", max_chars=32, placeholder="GESTOR")
    equipe = st.selectbox("Qual equipe realizou a venda?", options=equipes)
    tipo = st.selectbox("Qual tipo de venda?", options=tipo_vendas)
    email = st.text_input("Qual o email do cliente?", max_chars=32, placeholder="EMAIL")
    quantidade_de_produtos = st.number_input(
        "Qual a quantidade de produtos vendidos?",
        min_value=1,
        max_value=100,
        placeholder="Quantidade",
    )
    status = st.selectbox("Status da venda", options=STATUS)

    return (
        cnpj,
        telefone,
        consultor,
        data,
        gestor,
        equipe,
        tipo,
        email,
        quantidade_de_produtos,
        status,
        ddd,
        numero_pedido,
    )


def formatar_cnpj(cnpj):
    cnpj = cnpj.zfill(14)

    cnpj_formatado = "{}.{}.{}/{}-{}".format(
        cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:]
    )
    return cnpj_formatado


def formatar_telefone(telefone):
    telefone = telefone.replace(".0", "")
    return telefone


def remover_ponto(string):
    string = string.replace(".", "")
    return string


def formatar_nome(nome):
    nome = nome.split(" ")
    if len(nome) <= 1:
        return nome[0]

    if nome[1] == "DOS" or nome[1] == "DA" or nome[1] == "DE":
        nome_final = f"{nome[0]} {nome[1]} {nome[2]}"
        return nome_final

    nome_final = f"{nome[0]} {nome[1]}"
    return nome_final


months = [
    "Todos",
    "JANEIRO",
    "FEVEREIRO",
    "MARÇO",
    "ABRIL",
    "MAIO",
    "JUNHO",
    "JULHO",
    "AGOSTO",
    "SETEMBRO",
    "OUTUBRO",
    "NOVEMBRO",
    "DEZEMBRO",
]

month_by_numbers = {
    1: "JANEIRO",
    2: "FEVEREIRO",
    3: "MARÇO",
    4: "ABRIL",
    5: "MAIO",
    6: "JUNHO",
    7: "JULHO",
    8: "AGOSTO",
    9: "SETEMBRO",
    10: "OUTUBRO",
    11: "NOVEMBRO",
    12: "DEZEMBRO",
}

tipo_vendas = [
    "FIXA",
    "AVANÇADA",
    "MIGRAÇÃO PRÉ-PÓS",
    "VVN",
    "ALTAS",
    "PORTABILIDADE",
    "MIGRAÇÃO",
]
equipes = ["FREECEL", "VALPARAISO", "PARCEIRO", "GOIÂNIA", "SAMAMBAIA"]

UFS = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]

order = [
    "ID",
    "CNPJ",
    "Data",
    "Número do Pedido",
    "Plano",
    "Tipo",
    "Volume",
    "Preço",
    "Receita",
    "Status",
    "Equipe",
    "ADABAS",
    "Consultor",
    "M",
    "Já Cliente?",
    "CEP",
    "DDD",
    "Telefone",
    "UF",
    "Município",
    "Bairro",
    "Email",
    "Ano",
    "Mês",
    "Gestor",
    "CNAE",
    "Faturamento",
    "Quadro de Funcionários",
    "Capital",
    "Porte",
    "Natureza Jurídica",
    "Matriz",
    "Regime Tributário",
]

DDDS = [
    "61",
    "62",
    "64",
    "65",
    "67",
    "82",
    "71",
    "73",
    "74",
    "75",
    "77",
    "85",
    "88",
    "98",
    "99",
    "83",
    "81",
    "87",
    "86",
    "89",
    "84",
    "79",
    "68",
    "96",
    "92",
    "97",
    "91",
    "93",
    "94",
    "69",
    "95",
    "63",
    "27",
    "28",
    "31",
    "32",
    "33",
    "34",
    "35",
    "37",
    "38",
    "21",
    "22",
    "24",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "51",
    "53",
    "54",
    "55",
    "47",
    "48",
    "49",
]

DDDS_valor_inteiro = [
    "61",
    "62",
    "63",
    "64",
    "65",
    "66",
    "67",
    "68",
    "69",
    "91",
    "92",
    "93",
    "94",
    "95",
    "96," "97",
    "98",
    "99",
]

values_to_remove = [
    "CNAE",
    "Faturamento",
    "Quadro de Funcionários",
    "Capital",
    "Porte",
    "Natureza Jurídica",
    "Matriz",
    "Situação Cadastral",
    "Regime Tributário",
    "Ano",
    "Mês",
]


def default_index(order):
    return list(filter(lambda x: x not in values_to_remove, order))


STATUS = [
    "AGUARDANDO CHAMADO",
    "CREDITO NEGADO",
    "AGUARDANDO CONSULTOR",
    "AGUARDANDO GERAÇÃO DO CONTRATO",
    "AGUARDANDO SS",
    "ANALISE BKO",
    "ANALISE DE CREDITO",
    "CHECK LIST PENDENTE",
    "CHECKLIST",
    "CONCLUÍDO",
    "CONCLUÍDO-EXECUTADO PARCIALMENTE",
    "CREDITO REPROVADO",
    "EXECUTADO PARCIALMENTE",
    "FATURANDO",
    "FATURANDO-PORTABILIDADE",
    "INPUT",
    "MESA DE FRAUDE",
    "REPROVADO POR FRAUDE",
    "SEM ESTOQUE",
    "BACKOFFICE REPROVADO",
    "AGUARDANDO CASO",
    "REFAZER",
    "PENDENTE",
    "EXPIRADO",
    "EM ANALISE",
    "AGUARDANDO SAV",
    "FATURANDO- INSTALADO",
    "AGUARDANDO 1º PEDIDO",
    "ABERTA",
    "CONCLUÍDO / PAGO",
    "Simulação Reprovada",
    "SIMPLIFIQUE",
    "VALIDAÇÃO DE DOCUMENTOS",
    "PORTABILIDADE NEGADA* CHAMADO",
    "PORTABILIDADE CANCELADA",
    "ATIVO",
    "ATIVO/PAGO",
    "CABEAMENTO",
    "CAIXA OBSTRUIDA",
    "TT PJ/PJ",
    "TT PF/PJ",
    "CANCELADO",
    "CONTRATO ENVIADO PARA ÁREA COMERCIAL",
    "ENVIADO",
    "INDISPONIVEL",
    "NECESSIDADE DE CABEAMENTO",
    "PORTA QUEIMADA",
    "RACO",
    "REPROVADO",
    "REPROVADO NO SAV",
    "SUPORTE",
    "RETIDO",
    "SAV",
    "MIGRAÇAO DE TECNOLOGIA",
    "AGUARDANDO CHAMADO",
    "ATIVO MIGRAÇÃO",
    "ANALISE DE CREDITO",
    "MESA DE FRAUDE",
    "MESA DE CRÉDITO",
    "AGUARDANDO INPUT",
    "FATURANDO",
    "ENVIADO MIGRAÇÃO",
    "ATIVO METALICO",
    "ENVIADO-PAGO",
    "FATURANDO INSTALADO",
    "ENVIADO METALICO",
    "PENDENCIA TECNICA",
    "REPROVADO SUPORTE",
    "CREDITO REPROVADO",
    "TOTALIZAÇÃO",
]

new_order = order.copy()
new_order.insert(9, "Valor Atual")
new_order.insert(10, "Valor Renovação")
new_order.insert(11, "Pacote Inovação")
new_order.insert(12, "Valor Inovação")
new_order.insert(13, "Volume Inovação")
