import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

st.title("Análise de Distribuição de Classes")

csv_url = 'https://github.com/Claridade74/ecmi/blob/main/animals.csv'

response = requests.get(csv_url)
if response.status_code == 200:
    st.write("O arquivo CSV foi encontrado e está acessível.")
else:
    st.error("Não foi possível acessar o arquivo CSV. Verifique a URL e as permissões.")

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
