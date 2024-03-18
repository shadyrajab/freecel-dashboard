import tempfile
from datetime import datetime
from typing import Optional

import pandas as pd
import streamlit as st

from dataframe.rankings import Rankings
from dataframe.stats import Stats
from utils.utils import month_by_numbers, months

# Configurando o layout da página
st.set_page_config(
    page_title="Rankings - Freecel",
    page_icon="https://i.imgur.com/pidHoxz.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "https://github.com/shadyrajab/freecel-dashboard"},
)

with open("styles/styles.css", "r") as styles:
    css = styles.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_data(ano: Optional[int] = None, mes: Optional[str] = None):
    rankings = Rankings(ano, mes)
    return rankings

@st.cache_data
def load_dates():
    dates = Stats().dates
    return dates


dates = load_dates()

# Barra lateral com filtragem de ano e mês
with st.sidebar:
    mes = None
    # Selecionando todos os anos no qual houveram vendas registradas
    years = ["Todos"] + sorted([list(year.keys())[0] for year in dates], reverse=True)
    ano = st.sidebar.selectbox(
        label="Ano", options=years, index=years.index(str(datetime.now().year))
    )

    if ano != "Todos":
        # Selecionando todos os meses de um determinado ano no qual houveram vendas registradas
        months = ["Todos"] + sorted(
            [
                month
                for year_dict in dates
                if ano in year_dict
                for month in year_dict[ano]
            ],
            key=months.index,
        )
        mes = st.selectbox(
            label="Mês: ",
            options=months,
            index=months.index(month_by_numbers[datetime.now().month - 1]),
        )

st.title(
    body=(
        f"Rankings - {ano}"
        if ano and mes == "Todos"
        else f"Rankings - {mes}/{ano}" if ano and mes else f"Rankings - Geral"
    )
)

rankings = load_data(ano, mes)
df = rankings.full_ranking
df.fillna(0, inplace=True)
categories = ["Altas", "Total", "VVN", "Avançada", "Migração Pré-Pós", "Fixa"]
sub_categories = ["Volume", "Receita"]
multi_index = pd.MultiIndex.from_product([categories, sub_categories])

# Removendo a primeira coluna 'consultor' para aplicar o MultiIndex nas demais
df.set_index("Consultor", inplace=True)
headers = {
    "selector": "th:not(.index_name)",
    "props": "background-color: white; color: black; text-align: center; border:None; border-radius: 30px;",
}

td = {"selector": "tr", "props": "border: None;"}

# Definindo o MultiIndex para o DataFrame
df.columns = multi_index
df.reset_index(inplace=True)
df = df[
    ["Consultor", "Altas", "Avançada", "VVN", "Migração Pré-Pós", "Fixa", "Total"]
].sort_values(by=("Total", "Receita"), ascending=False)

total = (
    df.iloc[:1]
    .style.apply(
        lambda x: ["background-color: lightgreen; font-weight: bold"] * len(x), axis=1
    )
    .set_properties(**{"border": None, "border-radius": "30px"})
    .format(
        {
            ("Altas", "Receita"): "R$ {:.1f}",
            ("Total", "Receita"): "R$ {:.1f}",
            ("Fixa", "Receita"): "R$ {:.1f}",
            ("Avançada", "Receita"): "R$ {:.1f}",
            ("VVN", "Receita"): "R$ {:.1f}",
            ("Migração Pré-Pós", "Receita"): "R$ {:.1f}",
            ("Altas", "Volume"): "{:.0f}",
            ("Avançada", "Volume"): "{:.0f}",
            ("Fixa", "Volume"): "{:.0f}",
            ("Migração Pré-Pós", "Volume"): "{:.0f}",
            ("Total", "Volume"): "{:.0f}",
            ("VVN", "Volume"): "{:.0f}",
        }
    )
)

df = (
    df.iloc[1:]
    .style.set_properties(
        **{
            "background-color": "#f2f2f2",
            "border": None,
            "border-top": None,
            "border-radius": "20px",
            "font-weight": "bold",
        }
    )
    .set_table_styles([headers, td])
    .hide(axis="index")
    .background_gradient(
        subset=["Total", "Fixa", "Avançada", "VVN", "Altas", "Migração Pré-Pós"],
        cmap="Greys",
    )
    .format(
        {
            ("Altas", "Receita"): "R$ {:.1f}",
            ("Total", "Receita"): "R$ {:.1f}",
            ("Fixa", "Receita"): "R$ {:.1f}",
            ("Avançada", "Receita"): "R$ {:.1f}",
            ("VVN", "Receita"): "R$ {:.1f}",
            ("Migração Pré-Pós", "Receita"): "R$ {:.1f}",
            ("Altas", "Volume"): "{:.0f}",
            ("Avançada", "Volume"): "{:.0f}",
            ("Fixa", "Volume"): "{:.0f}",
            ("Migração Pré-Pós", "Volume"): "{:.0f}",
            ("Total", "Volume"): "{:.0f}",
            ("VVN", "Volume"): "{:.0f}",
        }
    )
)

ranking = df.concat(total)
# teste = pd.concat([df.data, total.data])
html = (
    ranking.to_html(index=False)
    .replace("\n", " ")
    .replace("<td", '<td style="white-space: nowrap;"')
)

# Exibindo o HTML em Markdown

with st.container(border=True):
    st.markdown(
        f"""
        <div style="overflow-x: auto; overflow-y: auto; height: 500px;">
            {html}
    """,
        unsafe_allow_html=True,
    )


def download_excel():
    ranking = pd.concat([df.data, total.data])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp:
        ranking.to_excel(temp.name)
        temp.close()

        # Ler e retornar os dados do arquivo Excel
        with open(temp.name, "rb") as f:
            data = f.read()

    return data


st.download_button(
    "Exportar Planilha",
    download_excel(),
    file_name="ranking.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
