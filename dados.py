import streamlit as st
import pandas as pd

from apoio import clear_number

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

    df_final['Ano'] = df_final['Ano'].astype(str)
    return df_final

