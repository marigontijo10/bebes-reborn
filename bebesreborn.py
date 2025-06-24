import pandas as pd
import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend compatível com Streamlit Cloud

# Configurações de página
st.set_page_config(
    page_title="Classificador de Notícias - Bebês Reborn",
    page_icon="🍼",
    layout="wide"
)

# Funções
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
    else:
        return '💰 Comercial'  # padrão quando não encontra palavras emocionais

# Título do App
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #000000;">🍼 Classificador de Notícias - Bebês Reborn</h1>
        <p style="font-size: 18px; color: #555;">Explore as notícias, entenda os temas por trás das reportagens e visualize os termos mais recorrentes!</p>
    </div>
""", unsafe_allow_html=True)

# Carregamento de dados
df = load_data("reborn.csv")
df.columns = df.columns.str.strip()

if "titulo" not in df.columns:
    st.error("A coluna 'titulo' não foi encontrada no CSV.")
else:
    col1, col2 = st.columns([1, 2.5], gap="large")

    with col1:
        st.subheader("🗂️ Escolha uma notícia:")
        opcoes = df["titulo"].dropna().unique()
        escolha = st.selectbox("Selecione o título da notícia:", opcoes)

    noticia = df[df["titulo"] == escolha].iloc[0]

    with col2:
        st.markdown("### 📰 Notícia completa")
        st.markdown(f"""
            <div style="background-color: #F3E5F5; padding: 20px; border-radius: 10px; color: #4A148C;">
                <p style="margin-bottom: 10px;"><strong>📅 Data:</strong> {noticia.get("data", "Data não disponível")}</p>
                <p style="text-align: justify;">{noticia["texto"]}</p>
            </div>
        """, unsafe_allow_html=True)

    # Classificação automática
    st.markdown("### 🏷️ Classificação da notícia:")
    classificacao = classificar_texto(str(noticia["texto"]))
    st.success(classificacao)

    # Nuvem de palavras
    st.markdown("### ☁️ Palavras mais frequentes na notícia:")

    texto = str(noticia["texto"])
    if texto.strip():
        stopwords = set(STOPWORDS)
        # Adicione mais palavras irrelevantes se quiser, por exemplo:
        # stopwords.update(["reborn", "boneca", "diz"])

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            stopwords=stopwords,
            collocations=False
        ).generate(texto)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning("O texto está vazio. Nuvem de palavras não pode ser gerada.")

