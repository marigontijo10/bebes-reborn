import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Ocorreu um erro ao ler o arquivo CSV: {e}")
        return pd.DataFrame()

def classificar_texto_comercial_ou_emocional(texto):
    texto = texto.lower()

    palavras_comercial = [
        'venda', 'comércio', 'comprar', 'produto', 'loja', 'negócio', 'anúncio',
        'marketing', 'mercado', 'cliente', 'preço', 'e-commerce', 'divulgação'
    ]
    palavras_emocional = [
        'mãe', 'filho', 'emoção', 'amor', 'carinho', 'sentimento', 'afetivo',
        'família', 'adoção', 'tristeza', 'felicidade', 'depressão', 'solidão',
        'psicológico', 'vínculo', 'empatia'
    ]

    if any(p in texto for p in palavras_emocional):
        return 'Emocional'
    elif any(p in texto for p in palavras_comercial):
        return 'Comercial'
    else:
        return 'Não definido'

st.title("🍼 Visualizador de Matérias - Bebê Reborn")

df = load_data("reborn.csv")
df.columns = df.columns.str.strip()

if "titulo" not in df.columns:
    st.error("A coluna 'titulo' não foi encontrada no CSV.")
else:
    st.subheader("Selecione uma matéria:")
    opcoes = df["titulo"].dropna().unique()
    escolha = st.selectbox("Escolha um título:", opcoes)

    materia = df[df["titulo"] == escolha].iloc[0]

    if "data" in df.columns:
        st.markdown(f"### 📅 Data: {materia['data']}")
    else:
        st.warning("Coluna 'data' não encontrada no CSV.")

    st.markdown("### 📰 Notícia:")
    st.write(materia["texto"])

    # Classificação Comercial ou Emocional
    classificacao = classificar_texto_comercial_ou_emocional(str(materia["texto"]))
    st.markdown("### 🏷️ Classificação (Automática):")
    st.success(classificacao)

    # Nuvem de palavras
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
        st.pyplot(plt)
    else:
        st.warning("O texto está vazio, impossível gerar a nuvem de palavras.")
