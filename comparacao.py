import numpy as np
import pandas as pd
import streamlit as st
import altair as alt


def ResetFiltrosComparacao():
    st.session_state.paisComparacao = ['Brazil', 'Spain', 'United States of America']

def Grafico(df, titulo, valor, titulo_valor, angle=300, dx=0, dy=0):
    base = alt.Chart(df).encode(
        alt.Color('Pais').legend(None),
    ).properties(
        height=400,
        title={
            'text': ['', titulo],
        },
    )
    line = base.mark_line().encode(
        alt.X('Ano'),
        alt.Y(valor, title=titulo_valor),
        # tooltip=['Pais', 'Ano', valor]
    )

    ultimo_ano = base.mark_circle().encode(
        alt.X("last_year['Ano']:O", title="Ano"),
        alt.Y(f"last_year['{valor}']:Q", title=titulo_valor),
        # tooltip=['Pais', 'Ano', valor]
    ).transform_aggregate(
        last_year='argmax(Ano)',
        groupby=['Pais']
    )

    nome_pais = ultimo_ano.mark_text(
        align='left',
        baseline='middle',
        dx=7
    ).encode(
        text='Pais'
    )

    texto = line.mark_text(
        align='left', 
        baseline='bottom', 
        dx=dx,
        dy=dy,
        font='monospace',
        fontWeight='bold',
        fontSize=12,
        angle=angle,
    )

    chart = (line + ultimo_ano + nome_pais + texto).configure_axis(
        labelFontSize=14,
        titleFontSize=16
    ).configure_title(
        fontSize=20,
        anchor='middle',
        subtitleFontSize=14,
    )

    return chart


def Comparacao(df):
    paises = df['Pais'].unique().tolist()
    paises.sort()


    col1, col2 = st.columns([0.9, 0.1])

    with col1:
        pais = st.multiselect('Selecione o(s) país(es)', paises, key='paisComparacao', help="Selecione um mais países para comparar os dados")

    with col2:
        st.write(' ')
        st.write(' ')
        st.button('Reset ', type='primary', help="Retorna o ano e países ao padrão", on_click=ResetFiltrosComparacao)


    filtro_pais = pais if len(pais) > 0 else paises

    df_filtrado = df[df['Pais'].isin(filtro_pais)]
    # st.write(df_filtrado)

    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        st.altair_chart(Grafico(df_filtrado, 'Comparação Doadores Mortos', 'PMP Mortos', 'Doações por Milhão de Pessoas'), use_container_width=True)
        st.altair_chart(Grafico(df_filtrado, 'Transplantes de RIM', 'Rim', 'Total de Transplantes'), use_container_width=True)
        st.altair_chart(Grafico(df_filtrado, 'Transplantes de Fígado', 'Figado', 'Total de Transplantes'), use_container_width=True)
        st.altair_chart(Grafico(df_filtrado, 'Outros Transplantes', 'Outros', 'Total de Transplantes'), use_container_width=True)

    with col2:
        st.altair_chart(Grafico(df_filtrado, 'Comparação Doadores Mortos', 'Doadores Mortos', 'Total Doadores'), use_container_width=True)
        st.altair_chart(Grafico(df_filtrado, 'Transplantes de Coração', 'Coracao', 'Total de Transplantes'), use_container_width=True)
        st.altair_chart(Grafico(df_filtrado, 'Transplantes de Pulmão', 'Pulmao', 'Total de Transplantes'), use_container_width=True)
        st.altair_chart(Grafico(df_filtrado, 'População', 'Populacao', 'Total de Transplantes'), use_container_width=True)
