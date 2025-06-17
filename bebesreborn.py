pip install wordcloud

import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Visualizador Reborn", layout="centered")

st.title("🍼 Visualizador de Matérias - Bebê Reborn")

# Nome do arquivo CSV
arquivo = "reborn.csv.csv"

try:
    df = pd.read_csv(arquivo)
    df.columns = df.columns.str.strip()

    if "titulo" not in df.columns:
        st.error("A coluna 'titulo' não foi encontrada no CSV.")
    else:
        st.subheader("Selecione uma matéria:")
        opcoes = df["titulo"].dropna().unique()
        escolha = st.selectbox("Escolha um título:", opcoes)

        materia = df[df["titulo"] == escolha].iloc[0]

        # Mostrar dados da matéria
        st.markdown("### 📰 Notícia:")
        st.write(materia["texto"])

        st.markdown("### 🏷️ Classificação:")
        st.success(materia["classificação"])

        st.markdown("### 📅 Data:")
        st.info(materia["data"])

        # Gerar nuvem de palavras
        st.markdown("### ☁️ Nuvem de Palavras da Matéria:")

        texto = materia["texto"]
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

except FileNotFoundError:
    st.error(f"Arquivo '{arquivo}' não encontrado. Verifique o nome e o local do arquivo.")
