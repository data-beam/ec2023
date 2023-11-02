import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

from comparacao import Comparacao, ResetFiltrosComparacao
from dados import lerDados
from geral import Geral, ResetFiltrosGeral

st.set_page_config(layout="wide", page_title='EC 2023 - Doação de Órgãos no Mundo', page_icon=':heart:')
    
df = lerDados()

if 'paisGeral' not in st.session_state or 'ano' not in st.session_state:
    ResetFiltrosGeral()

if 'paisComparacao' not in st.session_state:
    ResetFiltrosComparacao()

st.title("Doação de Órgãos no Mundo")

tab1, tab2 = st.tabs(["Geral", "Comparação"])

with tab1:
    Geral(df)

with tab2:
    Comparacao(df)