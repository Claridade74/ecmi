import pandas as pd
import numpy as np
import streamlit as st
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import string

#Os dataframes com cada artista - nacional ou internacional
df_nac = pd.read_csv('letras_musicas_nac.csv')
df_int = pd.read_csv('letras_musicas_int.csv')

# Troca o ícone da aba do site, apenas para melhorar no design
st.set_page_config(page_icon='🎵')

# Caminho relativo para a imagem de fundo
background_image_path = "notasmusicais.png" 

try:
    with open(background_image_path, 'rb') as f:
        st.image(f, use_column_width=True)
except FileNotFoundError:
    st.error(f"Imagem de fundo não encontrada no caminho: {background_image_path}")

# Adiciona a imagem de fundo usando CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url({background_image_path});
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Para colocar o texto explicativo na parte lateral do site 
with st.sidebar:
    st.subheader('Adivinhe: Um Jogo para Testar seus Conhecimentos Musicais')
    st.write('Esse projeto tem como objetivo oferecer um momento de diversão para qualquer pessoa com interesse em testar seus conhecimentos musicais!')
    st.write('Ao todo, são 80 músicas de 19 artistas (entre nacionais e internacionais)!')
    st.caption('Projeto desenvolvido por Clarissa Treptow, sob supervisão do Prof. Josir C. Gomes')
    st.caption('FGV ECMI')

# Define as stopwords a serem retiradas das nuvens de palavras geradas, que não agregam na identificação da música ou facilitam demais (como o nome do artista)
def stopwords():
    return set([
        'a', 'e', 'o', 'que', 'de', 'da', 'do', 'em', 'um', 'uma', 'é', 'na', 'no', 'pra', 'com', 'taylor swift', 'ariana grande', 'anitta',
        'luisa sonza', 'u2', 'lana del rey', 'panic at the disco', 'imagine dragons', 'justin timberlake', 'bon jovi', 'justin bieber',
        'seu jorge', 'sabrina carpenter', 'djavan', 'shawn mendes', 'jorge ben jor', 'iza', 'caetano veloso', 'ivete sangalo', 'my', 'the',
        'to', 'te', 'os', 'of', 'luísa'
    ])

def cores_diferentes():
    color_palettes = [
        'viridis', 'winter', 'summer', 'prism', 'Accent', 'Blues', 'Oranges',
        'GnBu', 'Purples', 'coolwarm', 'cool', 'gist_ncar_r', 'hsv', 'rainbow',
        'spring', 'magma'
    ]
    return random.choice(color_palettes)

def gerar_nuvem_e_opcoes(df):
    musica = df.sample(1).iloc[0]
    letra = musica['letra']
    artista_correto = musica['artista']
    
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap=cores_diferentes(), stopwords=stopwords()).generate(letra)

    artistas_unicos = df[df['artista'] != artista_correto]['artista'].unique()    
    outros_artistas = np.random.choice(artistas_unicos, 4, replace=False).tolist()
    
    opcoes = outros_artistas + [artista_correto]
    random.shuffle(opcoes)
    
    return wordcloud, artista_correto, opcoes

# Inicializa a escolha do usuário e as variáveis de estado
if 'escolha' not in st.session_state:
    st.session_state.escolha = None

if 'wordcloud' not in st.session_state:
    st.session_state.wordcloud = None

if 'rodada' not in st.session_state:
    st.session_state.rodada = 1

if 'pontuacao' not in st.session_state:
    st.session_state.pontuacao = 0

# Adiciona botões para o usuário escolher entre músicas nacionais e internacionais
if st.session_state.escolha is None:
    st.title("Escolha o tipo de artista que você gostaria de adivinhar as músicas:")
    if st.button("Artistas Nacionais"):
        st.session_state.escolha = "Nacionais"
        st.session_state.df = df_nac
    elif st.button("Artistas Internacionais"):
        st.session_state.escolha = "Internacionais"
        st.session_state.df = df_int

# Inicia o jogo após a escolha
if st.session_state.escolha is not None:
    if st.session_state.wordcloud is None:
        st.session_state.wordcloud, st.session_state.artista_correto, st.session_state.opcoes = gerar_nuvem_e_opcoes(st.session_state.df)
    
    if st.session_state.rodada <= 10:
        st.title(f"Rodada {st.session_state.rodada} de 10: Adivinhe o Artista!")
        st.subheader("Por meio desta nuvem de palavras, tente adivinhar quem é o artista desta música:")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(st.session_state.wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        escolha = st.radio("Quem é o artista desta música?", st.session_state.opcoes)

        if st.button("Verificar"):
            if escolha == st.session_state.artista_correto:
                st.success("Parabéns! Você acertou! Ganhou 5 pontos.")
                st.session_state.pontuacao += 5
            else:
                st.error(f"Que pena! A resposta correta é {st.session_state.artista_correto}. Perdeu 5 pontos.")
                st.session_state.pontuacao -= 5

            st.session_state.rodada += 1

            if st.session_state.rodada <= 10:
                st.session_state.wordcloud, st.session_state.artista_correto, st.session_state.opcoes = gerar_nuvem_e_opcoes(st.session_state.df)
                st.experimental_rerun()
            else:
                st.balloons()
                st.write(f"Jogo terminado! Sua pontuação final é: {st.session_state.pontuacao} pontos!")
                if st.session_state.pontuacao <= 10:
                    st.write("Seus conhecimentos musicais podem melhorar!")
                else:
                    st.write("Seus conhecimentos musicais são bem amplos!")

    else:
        st.write(f"Jogo terminado! Sua pontuação final é: {st.session_state.pontuacao} pontos!")
        if st.session_state.pontuacao <= 10:
            st.write("Seus conhecimentos musicais podem melhorar!")
        else:
            st.write("Seus conhecimentos musicais são bem amplos!")
        if st.button("Reiniciar"):
            st.session_state.update({'escolha': None, 'rodada': 1, 'pontuacao': 0, 'wordcloud': None})
