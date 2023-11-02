import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

from apoio import addText

def ResetFiltrosGeral():
    st.session_state.paisGeral = ['Brazil', 'United States of America', 'Spain']
    st.session_state.ano = '2022'
    
def Geral(df):
    col1, col2, col3 = st.columns([0.2, 0.7, 0.1])

    periodos = df['Ano'].unique().tolist()
    periodos.sort(reverse=True)

    paises = df['Pais'].unique().tolist()
    paises.sort()

    with col1:
        year = st.selectbox('Selecione o ano', periodos, key='ano', help="Selecione o ano para filtrar os dados")

    with col2:
        pais = st.multiselect('Selecione o(s) país(es)', paises, key='paisGeral', help="Selecione um mais países para filtrar os dados")

    with col3:
        st.write(' ')
        st.write(' ')
        st.button('Reset', type='primary', help="Retorna o ano e países ao padrão", on_click=ResetFiltrosGeral)


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
