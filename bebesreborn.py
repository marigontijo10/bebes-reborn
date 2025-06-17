import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("🍼 Visualizador de Matérias - Bebê Reborn")

arquivo = "reborn.csv.csv"  # Nome exatamente como o seu arquivo

try:
    df = pd.read_csv(arquivo)
    df.columns = df.columns.str.strip()  # Remove espaços dos nomes das colunas

    if "titulo" not in df.columns:
        st.error("A coluna 'titulo' não foi encontrada no CSV.")
    else:
        st.subheader("Selecione uma matéria:")
        opcoes = df["titulo"].dropna().unique()
        escolha = st.selectbox("Escolha um título:", opcoes)

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

        # Geração da nuvem de palavras
        st.markdown("### ☁️ Nuvem de Palavras:")

        texto = str(materia["texto"])
        if texto.strip():
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                stopwords=None,
                collocations=False
            ).generate(texto)

            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot()
        else:
            st.warning("O texto está vazio, impossível gerar a nuvem de palavras.")

except FileNotFoundError:
    st.error(f"Arquivo '{arquivo}' não encontrado.")
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")

