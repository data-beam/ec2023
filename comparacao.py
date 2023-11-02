import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

from apoio import addText

def ResetFiltrosComparacao():
    st.session_state.paisComparacao = ['Brazil', 'Spain']

def Comparacao(df):
    paises = df['Pais'].unique().tolist()
    paises.sort()

    pais = st.multiselect('Selecione o(s) país(es)', paises, key='paisComparacao', help="Selecione um mais países para comparar os dados")

    filtro_pais = pais if len(pais) > 0 else paises

    df_filtrado = df[df['Pais'].isin(filtro_pais)]

    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        line = alt.Chart(df_filtrado).mark_line().encode(
            alt.X('Ano'),
            alt.Y('PMP Mortos', title='Doações por Milhão de Pessoas'),
            alt.Color('Pais').legend(None),
            tooltip=['Pais', 'Ano', 'PMP Mortos']
        )

        st.altair_chart(line, use_container_width=True)

        '---'

        st.write(df_filtrado)