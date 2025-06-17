import pandas as pd
import streamlit as st

st.title("🍼 Visualizador de Matérias - Bebê Reborn")

# Nome simples do arquivo CSV
arquivo = "reborn.csv.csv"

try:
    df = pd.read_csv(arquivo)
    df.columns = df.columns.str.strip()  # remove espaços extras

    if "titulo" not in df.columns:
        st.error("A coluna 'titulo' não foi encontrada no CSV.")
    else:
        st.subheader("Selecione uma matéria:")
        opcoes = df["titulo"].dropna().unique()
        escolha = st.selectbox("Escolha um título:", opcoes)
        st.success(f"Você selecionou: {escolha}")

except FileNotFoundError:
    st.error(f"Arquivo '{arquivo}' não encontrado. Verifique o nome e o local do arquivo.")
