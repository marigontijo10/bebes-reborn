import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("🍼 Visualizador de Matérias - Bebê Reborn")

# Nome do arquivo CSV (certifique-se de que está no mesmo diretório)
arquivo = "reborn.csv.csv"

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

        # Exibir data, notícia e classificação
        if "data" in df.columns:
            st.markdown(f"### 📅 Data: {materia['data']}")
        else:
            st.warning("Coluna 'data' não encontrada no CSV.")

        st.markdown("### 📰 Notícia:")
        st.write(materia["texto"])

        st.markdown("### 🏷️ Classificação:")
        st.success(materia["classificação"])

        # Gerar nuvem de palavras
        st.markdown("### ☁️ Nuvem de Palavras:")
        if pd.notna(materia["texto"]):
            texto = materia["texto"]

            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                stopwords=None
            ).generate(texto)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.info("Texto da notícia vazio ou inválido.")

except FileNotFoundError:
    st.error(f"Arquivo '{arquivo}' não encontrado. Verifique o nome e o local do arquivo.")
