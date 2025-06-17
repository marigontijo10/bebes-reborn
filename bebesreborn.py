import pandas as pd
import streamlit as st

st.title("🍼 Visualizador de Matérias - Bebê Reborn")

# Nome do arquivo CSV (certifique-se de que está no mesmo diretório)
arquivo = "reborn.csv"

try:
    df = pd.read_csv(arquivo)
    df.columns = df.columns.str.strip()  # Remove espaços em branco nos nomes

    if "titulo" not in df.columns:
        st.error("A coluna 'titulo' não foi encontrada no CSV.")
    else:
        st.subheader("Selecione uma matéria:")
        opcoes = df["titulo"].dropna().unique()
        escolha = st.selectbox("Escolha um título:", opcoes)

        # Filtrar o DataFrame para a linha escolhida
        materia = df[df["titulo"] == escolha].iloc[0]

        # Exibir notícia e classificação
        st.markdown("### 📰 Notícia:")
        st.write(materia["texto"])

        st.markdown("### 🏷️ Classificação:")
        st.success(materia["classificação"])

except FileNotFoundError:
    st.error(f"Arquivo '{arquivo}' não encontrado. Verifique o nome e o local do arquivo.")

