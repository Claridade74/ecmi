import pandas as pd
import numpy as np
import streamlit as st
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import string
import time

df = pd.read_csv('letras_musicas.csv')

def gerar_nuvem_e_opcoes(df):
    musica = df.sample(1).iloc[0]
    letra = musica['letra']
    artista_correto = musica['artista']
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(letra)

    artistas_unicos = df[df['artista'] != artista_correto]['artista'].unique()    
    outros_artistas = np.random.choice(artistas_unicos, 4, replace=False).tolist()
    
    opcoes = outros_artistas + [artista_correto]
    random.shuffle(opcoes)
    
    return wordcloud, artista_correto, opcoes


df = pd.read_csv('letras_musicas.csv')

if 'wordcloud' not in st.session_state:
    st.session_state.wordcloud, st.session_state.artista_correto, st.session_state.opcoes = gerar_nuvem_e_opcoes(df)

st.title("Adivinhe o Artista!")
st.subheader("Tente adivinhar quem é o artista desta música:")
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(st.session_state.wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

escolha = st.radio("Quem é o artista desta música?", st.session_state.opcoes)

if st.button("Verificar"):
    if escolha == st.session_state.artista_correto:
        st.success("Parabéns! Você acertou!")
    else:
        st.error(f"Que pena! A resposta correta é {st.session_state.artista_correto}.")
        
    st.session_state.wordcloud, st.session_state.artista_correto, st.session_state.opcoes = gerar_nuvem_e_opcoes(df)
