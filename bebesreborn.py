import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Bebês Reborn - Visualizador de Notícias",
    page_icon="🍼",
    layout="wide"
)

# --- Funções ---
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

def classificar_texto(texto):
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
        return '🧠 Emocional'
    elif any(p in texto for p in palavras_comercial):
        return '💰 Comercial'
    else:
        return '🔍 Não definido'

# --- Título principal ---
st.markdown("<h1 style='text-align: center; color: #6a1b9a;'>🍼 Visualizador de Matérias sobre Bebês Reborn</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Explore notícias, veja classificações e descubra os temas mais frequentes com uma nuvem de palavras.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Carregamento dos dados ---
df = load_data("reborn.csv")
df.columns = df.columns.str.strip()

# --- Interface principal ---
if "titulo" not in df.columns:
    st.error("A coluna 'titulo' não foi encontrada no CSV.")
else:
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("🗂️ Selecione uma notícia:")
        opcoes = df["titulo"].dropna().unique()
        escolha = st.selectbox("Escolha um título:", opcoes)

    materia = df[df["titulo"] == escolha].iloc[0]

    with col2:
        if "data" in df.columns:
            st.markdown(f"<p style='font-size: 16px;'>📅 <strong>Data:</strong> {materia['data']}</p>", unsafe_allow_html=True)
        else:
            st.warning("Coluna 'data' não encontrada no CSV.")

        st.markdown("### 📰 Notícia:")
        st.markdown(f"<div style='background-color: #f6f6f6; padding: 15px; border-radius: 10px;'>{materia['texto']}</div>", unsafe_allow_html=True)

        # Classificação automática
        classificacao = classificar_texto(str(materia["texto"]))
        st.markdown("### 🏷️ Classificação:")
        st.success(classificacao)

    # --- Nuvem de palavras ---
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

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning("O texto está vazio, impossível gerar a nuvem de palavras.")

# --- Rodapé ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 14px;'>Feito com ❤️ usando Streamlit | Projeto Bebês Reborn</p>",
    unsafe_allow_html=True
)
