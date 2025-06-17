import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

nome_arquivo_csv = 'Reborn.csv'

coluna_de_texto = 'texto'
coluna_de_classificacao = 'classificação'

try:
  df = pd.read_csv(nome_arquivo_csv) 
finally: 
  write("Arquivo CSV carregado com sucesso!")

df.columns = df.columns.str.strip()
write("\nNomes das colunas corrigidas (sem espaços):")
write(df.columns.tolist())


if coluna_de_texto not in df.columns:
  write(f"ERRO: A coluna '{coluna_de_texto}' não foi encontrada no arquivo.")
exit()

if coluna_de_classificacao not in df.columns:
  write(f"ERRO: A coluna '{coluna_de_classificacao}' não foi encontrada no arquivo.")
exit()

write("\nPrimeiras 5 linhas dos dados:")
write(df[[coluna_de_texto, coluna_de_classificacao]].head())

df.dropna(subset=[coluna_de_texto, coluna_de_classificacao], inplace=True)
write(f"\nNúmero de amostras após remover valores ausentes: {len(df)}")

write(f"ERRO: O arquivo '{nome_arquivo_csv}' não foi encontrado.")
exit()

write(f"Ocorreu um erro ao ler o arquivo CSV: {e}")
exit()

df["classificação"].unique()

for column in df.columns:

  if df[column].dtype == 'object':

    df[column] = df[column].str.strip()

X = df[coluna_de_texto]
y = df[coluna_de_classificacao]

if len(y.unique()) < 2:
write("\nERRO: A coluna de classificação precisa ter pelo menos duas classes distintas (ex: 'Comercial', 'Emocional').")
write(f"Classes encontradas: {y.unique()}")
exit()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

write(f"\nTotal de amostras: {len(df)}")
write(f"Número de amostras de treino: {len(X_train)}")
write(f"Número de amostras de teste: {len(X_test)}")
write(f"\nDistribuição das classes no conjunto original:\n{y.value_counts(normalize=True)}")
write(f"\nDistribuição das classes no conjunto de TREINO:\n{y_train.value_counts(normalize=True)}")
write(f"\nDistribuição das classes no conjunto de TESTE:\n{y_test.value_counts(normalize=True)}")
