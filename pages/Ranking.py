import streamlit as st
from dataframe.rankings import Rankings
from dataframe.stats import Stats
from datetime import datetime
from utils.utils import month_by_numbers, months
from typing import Optional
import pandas as pd
from io import StringIO

# Configurando o layout da página
st.set_page_config(
    page_title = "Rankings - Freecel",
    page_icon = "https://i.imgur.com/pidHoxz.png",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {
        'About': "https://github.com/shadyrajab/freecel-dashboard"
    }
)

def load_data(ano: Optional[int] = None, mes: Optional[str] = None):
    rankings = Rankings(ano, mes)
    return rankings

def load_dates():
    dates = Stats().dates
    return dates

dates = load_dates()

# Barra lateral com filtragem de ano e mês
with st.sidebar:
    mes = None
    # Selecionando todos os anos no qual houveram vendas registradas
    years = ['Todos'] + sorted([list(year.keys())[0] for year in dates], reverse = True)
    ano = st.sidebar.selectbox(
        label = 'Ano', 
        options = years, 
        index = years.index(str(datetime.now().year))
    )

    if ano != 'Todos':
        # Selecionando todos os meses de um determinado ano no qual houveram vendas registradas
        months = ['Todos'] + sorted([month for year_dict in dates if ano in year_dict for month in year_dict[ano]], key = months.index)
        mes = st.selectbox(
            label = 'Mês: ', 
            options = months, 
            index = months.index(month_by_numbers[datetime.now().month - 1]) 
        )

st.title(
    body = (
        f'Rankings - {ano}' if ano and mes == 'Todos' else
        f'Rankings - {mes}/{ano}' if ano and mes else
        f'Rankings - Geral'
    )
)

rankings = load_data(ano, mes)
df = rankings.full_ranking
df.fillna(0, inplace=True)
categories = ['Altas', 'Total', 'VVN', 'Avançada', 'Migração Pré-Pós', 'Fixa']
sub_categories = ['Volume', 'Receita']
multi_index = pd.MultiIndex.from_product([categories, sub_categories])

# Removendo a primeira coluna 'consultor' para aplicar o MultiIndex nas demais
df.set_index('Consultor', inplace=True)
cell_hover = {  # for row hover use <tr> instead of <td>
    'selector': 'td:hover',
    'props': [('background-color', 'lightgreen')]
}
index_names = {
    'selector': '.index_name',
    'props': 'font-style: italic; color: darkgrey; font-weight:normal;',
}
headers = {
    'selector': 'th:not(.index_name)',
    'props': 'background-color: white; color: black; text-align: center;',
    'border': None
}

# Definindo o MultiIndex para o DataFrame
df.columns = multi_index
df.reset_index(inplace=True)
df = df[['Consultor', 'Altas', 'Avançada', 'VVN', 'Migração Pré-Pós', 'Fixa', 'Total']].sort_values(
    by=('Total', 'Receita'), ascending=False
)

total = (df.iloc[:1].style
        .format({
        ('Altas', 'Receita'): 'R$ {:.1f}',
        ('Total', 'Receita'): 'R$ {:.1f}',
        ('Fixa', 'Receita'): 'R$ {:.1f}',
        ('Avançada', 'Receita'): 'R$ {:.1f}',
        ('VVN', 'Receita'): 'R$ {:.1f}',
        ('Migração Pré-Pós', 'Receita'): 'R$ {:.1f}',
        ('Altas', 'Volume'): '{:.0f}',
        ('Avançada', 'Volume'): '{:.0f}',
        ('Fixa', 'Volume'): '{:.0f}',
        ('Migração Pré-Pós', 'Volume'): '{:.0f}',
        ('Total', 'Volume'): '{:.0f}',
        ('VVN', 'Volume'): '{:.0f}'
    }) 
    .apply(lambda x: ['background-color: lightgreen; font-weight: bold']*len(x), axis=1)
)

df = (df.iloc[1:].style
    .set_properties(**{'background-color': 'white', 'border': None})
    .set_table_styles([cell_hover, index_names, headers])
    .hide(axis='index')
    .background_gradient(subset = [
        ('Altas', 'Receita'),
        ('VVN', 'Receita'),
        ('Avançada', 'Receita'),
        ('Migração Pré-Pós', 'Receita'),
        ('Fixa', 'Receita')
    ], cmap = 'Blues')
    .background_gradient(subset = [
        ('Altas', 'Volume'),
        ('Migração Pré-Pós', 'Volume'),
        ('VVN', 'Volume'),
        ('Avançada', 'Volume'),
        ('Fixa', 'Volume')
    ], cmap = 'Reds')
    .background_gradient(subset = ['Total'], cmap = 'Greys')
    .format({
        ('Altas', 'Receita'): 'R$ {:.1f}',
        ('Total', 'Receita'): 'R$ {:.1f}',
        ('Fixa', 'Receita'): 'R$ {:.1f}',
        ('Avançada', 'Receita'): 'R$ {:.1f}',
        ('VVN', 'Receita'): 'R$ {:.1f}',
        ('Migração Pré-Pós', 'Receita'): 'R$ {:.1f}',
        ('Altas', 'Volume'): '{:.0f}',
        ('Avançada', 'Volume'): '{:.0f}',
        ('Fixa', 'Volume'): '{:.0f}',
        ('Migração Pré-Pós', 'Volume'): '{:.0f}',
        ('Total', 'Volume'): '{:.0f}',
        ('VVN', 'Volume'): '{:.0f}'
    })
)

ranking = df.concat(total)
html = ranking.to_html(index=False).replace('\n', ' ').replace('<td', '<td style="white-space: nowrap;"')

# Exibindo o HTML em Markdown
st.markdown(f"""
    <div style="overflow-x: auto; overflow-y: auto; height: 500px;">
        {html}
""", unsafe_allow_html=True)
