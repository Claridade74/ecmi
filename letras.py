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

background_image_url = "https://github.com/Claridade74/ecmi/blob/main/notasmusicais.png"

# Adiciona a imagem de fundo usando CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{background_image_url}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: white; 
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
    
# Definindo uma função para gerar várias colorações para a nuvem de palavras
def cores_diferentes():
    color_palettes = [
        'viridis', 'winter', 'summer', 'prism', 'Accent', 'Blues', 'Oranges',
        'GnBu', 'Purples', 'coolwarm', 'cool', 'gist_ncar_r', 'hsv', 'rainbow',
        'spring', 'magma'
    ]
    return random.choice(color_palettes)

# Gera nuvens de palavras com uma letra aleatória, pega a opção correta do artista e também gera as outras opções "incorretas" 
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

# Pega uma letra aleatória, separa a letra para retirar uma palavra aleatória para ser substituída por uma "____" e também pega outras 4 palavras incorretas para as outras opções
def gerar_sentenca_e_opcoes(df):
    musica = df.sample(1).iloc[0]
    letra = musica['letra']
    palavras = letra.split()

    if len(palavras) < 5:
        return gerar_sentenca_e_opcoes(df)

    indice = random.randint(0, len(palavras) - 1)
    palavra_correta = palavras[indice]
    palavras[indice] = '_____'
    sentenca = ' '.join(palavras)

    palavras_unicas = df['letra'].str.split(expand=True).stack().unique()
    outras_palavras = np.random.choice(palavras_unicas, 4, replace=False).tolist()

    opcoes = outras_palavras + [palavra_correta]
    random.shuffle(opcoes)

    return sentenca, palavra_correta, opcoes

# Inicializando estados para o jogo de adivinhar o artista
if 'escolha_artista' not in st.session_state:
    st.session_state.escolha_artista = None

if 'wordcloud' not in st.session_state:
    st.session_state.wordcloud = None

if 'rodada_artista' not in st.session_state:
    st.session_state.rodada_artista = 1

if 'pontuacao_artista' not in st.session_state:
    st.session_state.pontuacao_artista = 0

# Inicializando estados para o jogo de adivinhar a palavra
if 'escolha_palavra' not in st.session_state:
    st.session_state.escolha_palavra = None

if 'sentenca' not in st.session_state:
    st.session_state.sentenca = None

if 'palavra_correta' not in st.session_state:
    st.session_state.palavra_correta = None

if 'opcoes_palavra' not in st.session_state:
    st.session_state.opcoes_palavra = None

if 'rodada_palavra' not in st.session_state:
    st.session_state.rodada_palavra = 1

if 'pontuacao_palavra' not in st.session_state:
    st.session_state.pontuacao_palavra = 0

# Separando o site em duas abas, uma para cada um dos jogos de adivinhação
tab1, tab2 = st.tabs(["Adivinhe o Artista", "Adivinhe a Palavra"])

# Primeiro jogo, para adivinhar o artista a partir da música contida na nuvem de palavras
with tab1:
    # Oferece duas opções para o usuário escolher entre artistas internacionais ou nacionais
    if st.session_state.escolha_artista is None:
        st.title("Escolha o tipo de artista que você gostaria de adivinhar as músicas:")
        if st.button("Artistas Nacionais"):
            st.session_state.escolha_artista = "Nacionais"
            st.session_state.df_artista = df_nac
        elif st.button("Artistas Internacionais"):
            st.session_state.escolha_artista = "Internacionais"
            st.session_state.df_artista = df_int
    
    if st.session_state.escolha_artista is not None:
        if st.session_state.wordcloud is None:
            st.session_state.wordcloud, st.session_state.artista_correto, st.session_state.opcoes_artista = gerar_nuvem_e_opcoes(st.session_state.df_artista)
        
        if st.session_state.rodada_artista <= 10:
            st.title(f"Rodada {st.session_state.rodada_artista} de 10: Adivinhe o Artista!")
            st.subheader("Por meio desta nuvem de palavras, tente adivinhar quem é o artista desta música:")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(st.session_state.wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
    
            escolha_artista = st.radio("Quem é o artista desta música?", st.session_state.opcoes_artista)
    
            if st.button("Verificar", key="verificar_artista"):
                if escolha_artista == st.session_state.artista_correto:
                    st.success("Parabéns! Você acertou! Ganhou 5 pontos.")
                    st.session_state.pontuacao_artista += 5
                else:
                    st.error(f"Que pena! A resposta correta é {st.session_state.artista_correto}. Perdeu 5 pontos.")
                    st.session_state.pontuacao_artista -= 5
    
                st.session_state.rodada_artista += 1
    
                if st.session_state.rodada_artista <= 10:
                    st.session_state.wordcloud, st.session_state.artista_correto, st.session_state.opcoes_artista = gerar_nuvem_e_opcoes(st.session_state.df_artista)
                    st.experimental_rerun()
                else:
                    st.balloons()
                    st.write(f"Jogo terminado! Sua pontuação final é: {st.session_state.pontuacao_artista} pontos!")
                    if st.session_state.pontuacao_artista <= 10:
                        st.write("Seus conhecimentos musicais podem melhorar!")
                    else:
                        st.write("Seus conhecimentos musicais são bem amplos!")
        else:
            st.write(f"Jogo terminado! Sua pontuação final é: {st.session_state.pontuacao_artista} pontos!")
            if st.session_state.pontuacao_artista <= 10:
                st.write("Seus conhecimentos musicais podem melhorar!")
            else:
                st.write("Seus conhecimentos musicais são bem amplos!")
            if st.button("Reiniciar"):
                st.session_state.update({
                    'escolha_artista': None, 'rodada_artista': 1, 'pontuacao_artista': 0, 'wordcloud': None,
                    'escolha_palavra': st.session_state.escolha_palavra, 'rodada_palavra': st.session_state.rodada_palavra,
                    'pontuacao_palavra': st.session_state.pontuacao_palavra, 'sentenca': st.session_state.sentenca
                })

# Segundo jogo, para adivinhar qual é a palavra que completa a letra da música
with tab2:
    # Oferece duas opções para o usuário escolher entre músicas internacionais ou nacionais
    if st.session_state.escolha_palavra is None:
        st.title("Escolha o tipo de música que você gostaria de adivinhar a palavra:")
        if st.button("Músicas Nacionais", key="nacionais_palavra"):
            st.session_state.escolha_palavra = "Nacionais"
            st.session_state.df_palavra = df_nac
        elif st.button("Músicas Internacionais", key="internacionais_palavra"):
            st.session_state.escolha_palavra = "Internacionais"
            st.session_state.df_palavra = df_int
    
    if st.session_state.escolha_palavra is not None:
        if st.session_state.sentenca is None:
            st.session_state.sentenca, st.session_state.palavra_correta, st.session_state.opcoes_palavra = gerar_sentenca_e_opcoes(st.session_state.df_palavra)
        
        if st.session_state.rodada_palavra <= 10:
            st.title(f"Rodada {st.session_state.rodada_palavra} de 10: Adivinhe a Palavra!")
            st.subheader("Tente adivinhar qual é a palavra original na letra abaixo, substituída por '_____':")
            st.write(st.session_state.sentenca)
    
            escolha_palavra = st.radio("Qual é a palavra original?", st.session_state.opcoes_palavra)
    
            if st.button("Verificar", key="verificar_palavra"):
                if escolha_palavra == st.session_state.palavra_correta:
                    st.success("Parabéns! Você acertou! Ganhou 5 pontos.")
                    st.session_state.pontuacao_palavra += 5
                else:
                    st.error(f"Que pena! A resposta correta é {st.session_state.palavra_correta}. Perdeu 5 pontos.")
                    st.session_state.pontuacao_palavra -= 5
    
                st.session_state.rodada_palavra += 1
    
                if st.session_state.rodada_palavra <= 10:
                    st.session_state.sentenca, st.session_state.palavra_correta, st.session_state.opcoes_palavra = gerar_sentenca_e_opcoes(st.session_state.df_palavra)
                    st.experimental_rerun()
                else:
                    st.balloons()
                    st.write(f"Jogo terminado! Sua pontuação final é: {st.session_state.pontuacao_palavra} pontos!")
                    if st.session_state.pontuacao_palavra <= 10:
                        st.write("Seus conhecimentos podem melhorar!")
                    else:
                        st.write("Seus conhecimentos estão bem amplos!")
        else:
            st.write(f"Jogo terminado! Sua pontuação final é: {st.session_state.pontuacao_palavra} pontos!")
            if st.session_state.pontuacao_palavra <= 10:
                st.write("Seus conhecimentos podem melhorar!")
            else:
                st.write("Seus conhecimentos estão bem amplos!")
            if st.button("Reiniciar", key="reiniciar_palavra"):
                st.session_state.update({
                    'escolha_palavra': None, 'rodada_palavra': 1, 'pontuacao_palavra': 0, 'sentenca': None,
                    'escolha_artista': st.session_state.escolha_artista, 'rodada_artista': st.session_state.rodada_artista,
                    'pontuacao_artista': st.session_state.pontuacao_artista, 'wordcloud': st.session_state.wordcloud
                })
