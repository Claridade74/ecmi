import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Análise de Distribuição de Classes")

# URL do arquivo CSV no GitHub
csv_url = 'https://raw.githubusercontent.com/usuario/repositorio/main/caminho/para/o/arquivo.csv'

# Lê o arquivo CSV diretamente do GitHub
df = pd.read_csv(csv_url)

st.write("Visualização das primeiras linhas do arquivo:")
st.write(df.head())

class_counts = df['Class'].value_counts()

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=class_counts.index, y=class_counts.values, palette="viridis")
ax.set_title('Distribuição das Classes', fontsize=15)
ax.set_xlabel('Classe', fontsize=12)
ax.set_ylabel('Frequência', fontsize=12)

st.pyplot(plt)
