import pandas as pd
import streamlit as st

# Título da página
st.title("🍼 Visualizador de Matérias - Bebê Reborn")

# Carregar o CSV
arquivo = "Planilha Bebê Reborn  - Sheet1 (1).csv"
df = pd.read_csv(arquivo)

# Ajustar os nomes das colunas
df.columns = df.columns.str.strip()

# Exibir as colunas para o usuário (opcional)
st.subheader("Colunas disponíveis no CSV:")
st.write(df.columns.tolist())

# Supondo que a coluna de título se chame "título" ou algo parecido
coluna_titulo = "título"  # ajuste se o nome for outro

if coluna_titulo not in df.columns:
    st.error(f"A coluna '{coluna_titulo}' não foi encontrada.")
else:
    st.subheader("Selecione uma matéria:")
    opcoes = df[coluna_titulo].dropna().unique()
    escolha = st.selectbox("Escolha um título:", opcoes)

    st.success(f"Você selecionou: {escolha}")

