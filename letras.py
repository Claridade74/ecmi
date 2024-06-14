import pandas as pd
import streamlit as st
import random
from wordcloud import WordCloud 
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import string
import nltk
from nltk.corpus import stopwords


df = pd.read_excel('letras_musicas.xlsx')

# Função para escolher uma letra de música aleatoriamente e criar uma nuvem de palavras
def gerar_nuvem_e_opcoes(df):
    # Escolher uma linha aleatoriamente
    musica = df.sample(1).iloc[0]
    letra = musica['letra']
    artista_correto = musica['artista']
    
    # Gerar a nuvem de palavras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(letra)
    
    # Escolher quatro outros artistas aleatórios para as opções
    outros_artistas = df[df['artista'] != artista_correto]['artista'].sample(4).tolist()
    
    # Combinar o artista correto com os outros artistas e embaralhar
    opcoes = outros_artistas + [artista_correto]
    random.shuffle(opcoes)
    
    return wordcloud, artista_correto, opcoes

# Gerar a nuvem de palavras e as opções de artista
wordcloud, artista_correto, opcoes = gerar_nuvem_e_opcoes(df)

# Exibir a nuvem de palavras
st.title("Adivinhe o Artista!")
st.subheader("Tente adivinhar quem é o artista desta música:")
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# Exibir as opções de artista para o usuário escolher
escolha = st.radio("Quem é o artista desta música?", opcoes)

# Verificar a escolha do usuário
if st.button("Verificar"):
    if escolha == artista_correto:
        st.success("Parabéns! Você acertou!")
    else:
        st.error(f"Que pena! A resposta correta é {artista_correto}.")
