import pandas as pd
import streamlit as st
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import string

df = pd.read_csv('letras_musicas.csv')

def gerar_nuvem_e_opcoes(df):
    musica = df.sample(1).iloc[0]
    letra = musica['letra']
    artista_correto = musica['artista']
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(letra)
    
    outros_artistas = df[df['artista'] != artista_correto]['artista'].sample(4).tolist()
    
    opcoes = outros_artistas + [artista_correto]
    random.shuffle(opcoes)
    
    return wordcloud, artista_correto, opcoes

wordcloud, artista_correto, opcoes = gerar_nuvem_e_opcoes(df)

st.title("Adivinhe o Artista!")
st.subheader("Tente adivinhar quem é o artista desta música:")
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

escolha = st.radio("Quem é o artista desta música?", opcoes)

if st.button("Verificar"):
    if escolha == artista_correto:
        st.success("Parabéns! Você acertou!")
    else:
        st.error(f"Que pena! A resposta correta é {artista_correto}.")
