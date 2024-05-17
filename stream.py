import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configurações da página
st.set_page_config(page_title="Minha Aplicação Streamlit", page_icon=":bar_chart:")

# Título da aplicação
st.title("Minha Aplicação Streamlit")

# Gerar dados aleatórios
np.random.seed(0)
data = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100)
})

# Gráfico de dispersão
st.write("## Gráfico de Dispersão")
st.write("Este é um gráfico de dispersão simples gerado com dados aleatórios.")
st.write(data)

fig, ax = plt.subplots()
ax.scatter(data['x'], data['y'])
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Exibir o gráfico
st.pyplot(fig)
