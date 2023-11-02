import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(layout="wide")

# This function receive an number as string and clear it removing commas and dots in 
# wrong position. After that returns an float number.
# this examples shows how the function must behave:
# Input: 1,456.80   Output: 1456.80
# Input: 5          Output: 5.00
# Input: 46,7       Output: 46.70
# Input: 215,4      Output: 215.40
# Input: 334,8      Output: 334.80
def clear_number(number):
    # If the number is empty, return 0
    if number == '':
        return 0
    
    # Remove all blank and special characters
    number = number.replace(' ', '')
    number = number.replace('\n', '')
    number = number.replace('\t', '')
    number = number.replace('\r', '')
    number = number.replace('(', '')
    number = number.replace(')', '')
    
    try:
        valor = float(number)
        return valor
    except ValueError:
        pass
    
    if number.count(',') == 1:
        number = number.replace(',', '.')

    try:
        valor = float(number)
        return valor
    except ValueError:
        pass
    

    # find position of the last dot
    pos = number.rfind('.')
    
    #remove all dots where position is before the last dot (pos)
    number = number[:pos].replace('.', '') + number[pos:]

    try:
        valor = float(number)
        return valor
    except ValueError:
        pass

    print("Error: ", number)
    return number

@st.cache_data
def lerDados():
    # df = pd.read_csv("dados.csv", header='infer', sep=';')
    df = pd.read_csv("https://raw.githubusercontent.com/data-beam/ec2023/main/dados.csv", header='infer', sep=';')
    df.fillna(value=0, inplace=True)

    df_final = df[['REPORTYEAR', 'REGION', 'COUNTRY', 'POPULATION', 'TOTAL Actual DD', 'TOTAL Kidney Tx', 'TOTAL Liver TX', 'Total Heart TX', 'TOTAL Lung Tx']]
    df_final['Outros'] = df['Pancreas Tx'] + df['Kidney Pancreas Tx'] + df['Small Bowel Tx']
    # Rename columns
    df_final.columns = ['Ano', 'Regiao', 'Pais', 'Populacao', 'Doadores Mortos', 'Rim', 'Figado', 'Coracao', 'Pulmao', 'Outros']
    # Adicionar o total de transplantes
    df_final['Total'] = df_final['Rim'] + df_final['Figado'] + df_final['Coracao'] + df_final['Pulmao'] + df_final['Outros']
    df_final['Populacao'] = df_final['Populacao'].apply(lambda x: clear_number(x)).astype(float)

    df_final['PMP Mortos'] = df_final['Doadores Mortos'] / df_final['Populacao']
    df_final['PMP Mortos'] = df_final['PMP Mortos'].apply(lambda x: round(x, 2))

    df_final['Total PMP'] = df_final['Total'] / df_final['Populacao']
    df_final['Total PMP'] = df_final['Total PMP'].apply(lambda x: round(x, 2))

    return df_final


def reset_filtros():
    st.session_state.pais = ['Brazil', 'United States of America', 'Spain']
    st.session_state.ano = 2022
    
# Adiciona um texto ao gráfico    
def addText(chart,angle=300, dx=0, dy=0):
    combined = chart.mark_bar() + chart.mark_text(
        align='left', 
        baseline='bottom', 
        dx=dx,
        dy=dy,
        font='monospace',
        fontWeight='bold',
        fontSize=12,
        angle=angle, 
    )
    combined = combined.configure_axis(
        labelFontSize=14,
        titleFontSize=16
    ).configure_title(
        fontSize=20,
        anchor='middle',
        subtitleFontSize=14,
    )
    return combined    
df = lerDados()

if 'pais' not in st.session_state or 'ano' not in st.session_state:
    reset_filtros()

st.title("Doação de Órgãos no Mundo")
col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

periodos = df['Ano'].unique().tolist()
periodos.sort(reverse=True)

regioes = df['Regiao'].unique().tolist()
regioes.sort()

paises = df['Pais'].unique().tolist()
paises.sort()

with col1:
    year = st.selectbox('Selecione o ano', periodos, key='ano')

with col2:
    pais = st.multiselect('Selecione o(s) país(es)', paises, key='pais')

with col3:
    st.write(' ')
    st.write(' ')
    st.button('Resetar Filtros', type='primary', on_click=reset_filtros)


filtro_pais = pais if len(pais) > 0 else paises

df_filtrado = df[(df['Ano'] == year) & (df['Pais'].isin(filtro_pais))]

# st.write(df_filtrado)

st.write('---')

chart = alt.Chart(df_filtrado).encode(
    alt.X('Pais', sort='-y'),
    alt.Y('PMP Mortos', title='Doações por Milhão de Pessoas'),
    text='PMP Mortos',
    color=alt.condition(
        alt.datum.Pais == 'Brazil',
        alt.value('orange'),
        alt.value('steelblue')
    )
).transform_window(
    rank='rank(count)',
    sort=[alt.SortField('PMP Mortos', order='descending')]
).transform_filter(
    alt.datum.rank < 30    
).properties(
    title={
        'text': ['', 'Ranking Doadores Mortos por País- Ano: ' + str(year)],
        'subtitle': ['PMP - Por milhão de Pessoas'],
        'subtitleColor': 'gray'
    },
    height=400,
)

st.altair_chart(addText(chart), use_container_width=True)

st.write('---')
df_tipo = df_filtrado[['Ano', 'Regiao', 'Pais', 'Rim', 'Figado', 'Coracao', 'Pulmao', 'Outros']]
df_tipo = df_tipo.melt(id_vars=['Ano', 'Regiao', 'Pais'], var_name='Tipo', value_name='Quantidade')

chart = alt.Chart(df_tipo).encode(
    alt.X('Pais', sort='-y'),
    alt.Y('Quantidade', title='Quantidade de Transplantes'),
    text='Quantidade',
    color='Tipo:N', 
    xOffset='Tipo:N',
).transform_window(
    rank='rank(count)',
    sort=[alt.SortField('Quantidade', order='descending')]
).transform_filter(
    alt.datum.rank < 30    
).properties(
    title={
        'text': ['', 'Comparativo de Transplantes por Órgão - Ano: ' + str(year)],
    },
    height=400,
)

st.altair_chart(addText(chart, angle=270, dx=5, dy=9), use_container_width=True)