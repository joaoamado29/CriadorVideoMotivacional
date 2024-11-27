import os
import random
from moviepy import *
import tkinter as tk
from tkinter import ttk
import subprocess

# Executa o arquivo ferramenta.py
subprocess.run(['python', 'pegar_frases.py'])

# Acessar pasta de videos
caminho = os.getcwd()
pasta_vds = caminho + '\\Videos'  # Corrigido para usar \\ em vez de \
pasta_audio = caminho + '\\Musicas'  # Corrigido para usar \\ em vez de \
pasta_resultado = caminho + '\\resultado_videos\\'

lista_vds = os.listdir(pasta_vds)
lista_audio = os.listdir(pasta_audio)
qtde_vds = len(lista_vds)
qtde_audio = len(lista_audio)

def sortar_txt():
    vds_selecionados = []
    for i in range(2):
        numero_sorteado = random.randint(0, qtde_vds - 1)  # Corrigido para incluir o índice 0
        vds_selecionados.append(pasta_vds + '\\' + lista_vds[numero_sorteado])
    return vds_selecionados

# Função para sortear videos
def sortear_vds():
    vds_selecionados = []
    for i in range(2):
        numero_sorteado = random.randint(0, qtde_vds - 1)  # Corrigido para incluir o índice 0
        vds_selecionados.append(pasta_vds + '\\' + lista_vds[numero_sorteado])
    return vds_selecionados

def sortear_audio():
    for i in range(1):
        numero_sorteado = random.randint(0, qtde_audio - 1)  # Corrigido para incluir o índice 0
        audio_selecionado = pasta_audio + '\\' + lista_audio[numero_sorteado]
    return audio_selecionado

def sortear_frase():
    for i in range(1):
        numero_sorteado = random.randint(0, qtde_audio - 1)  # Corrigido para incluir o índice 0
        frase_selecionada = todas_frases[numero_sorteado]
    return frase_selecionada

# Função para criar o vídeo
def criar_video():
    # Juntando videos
    videos_sorteados = sortear_vds()

    # Concatenação : OK
    clipe0 = VideoFileClip(videos_sorteados[0])
    clipe1 = VideoFileClip(videos_sorteados[1])

    video_concatenado = concatenate_videoclips([clipe0, clipe1])
    duracao = video_concatenado.duration

    # cria um clipe de texto
    txt_clip = TextClip(font="georgia.ttf", text=sortear_frase(), font_size=70, color='white', method='caption', size=(900, 300), bg_color='#5988FF')
    txt_clip = txt_clip.with_position('center').with_duration(duracao)

    # cria um clipe de audio
    audio_fundo = AudioFileClip(sortear_audio())
    audio_fundo_final = audio_fundo.with_subclip(0, duracao)

    # junta o video normal com o TextClip
    video_final = CompositeVideoClip([video_concatenado, txt_clip]) 
    video_final = video_final.with_audio(audio_fundo_final)

    # Obtendo o nome do vídeo da entrada
    nome = entrada_nome_arquivo.get()  # Obtém o nome do arquivo da entrada
    video_final.write_videofile(pasta_resultado + nome + '.mp4')
    # Fechando os clipes
    clipe0.close()
    clipe1.close()
    audio_fundo.close()
    audio_fundo_final.close()
    video_concatenado.close()

###############################################################################
###############################################################################
# -------------------- PEGAR FRASES ------------------------------------------
###############################################################################
###############################################################################
import requests
from bs4 import BeautifulSoup

# requisições
link = 'https://www.pensador.com/365_frases_motivacionais/'

requisicao = requests.get(link)
site = BeautifulSoup(requisicao.text, "html.parser")

# pegando as frases
lista_textos = site.find('div', class_='article-content')

textos = lista_textos.find_all('div', class_="callout") # frases sem autor
textos2 = lista_textos.find_all('blockquote') # frases autoral

# tratamento de frases sem autor especifico
def tratar_frase():
    lista_frases = []
    for item in textos:
        texto = str(item)
        texto = texto[24:]
        texto = texto[:-10]
        lista_frases.append(texto)
    return lista_frases
    
# tratamento de frases com autor
def tratar_frase_autoral():
    lista_frases = []
    for item in textos2:
        texto = str(item)
        texto = texto[15:]
        texto = texto[:-17]
        lista_frases.append(texto)
    return lista_frases

# functionar para adicionar frases autorais
def add_frases_autoral():
    for i, frase_autoral in enumerate(frases_tratadas_autoral):
        frase_autoral = frases_tratadas_autoral[i]
        frase_autoral = frase_autoral.split(sep='</p><p')
        autor = frase_autoral[1]
        autor = autor[15:]
        texto = frase_autoral[0]
        todas_frases.append(f'{texto}  -{autor}')

# lista auxiliar
todas_frases = []

# tratamento de frases
frases_tratadas_autoral = tratar_frase_autoral()
frases_tratadas = tratar_frase()

# adicionar frases

todas_frases.append(frases_tratadas) # Frases sem autor
add_frases_autoral() # Frases autorais

###################################################################################
###################################################################################
###################################################################################

# Criando a janela principal
janela = tk.Tk()
janela.title("Criar Video")
janela.geometry("600x450")  # Definindo o tamanho da janela (3:4)

# Estilo
style = ttk.Style()
style.configure("TButton", padding=10, relief="flat", background="#20bcbb", foreground="black", font=("Helvetica", 12))  # Mudando a cor do texto para preto e definindo a fonte
style.configure("TEntry", padding=5, font=("Helvetica", 12))  # Definindo a fonte para a entrada
style.configure("TLabel", font=("Helvetica", 12))  # Definindo a fonte para o rótulo

# Criando uma caixa de entrada para o nome do arquivo
ttk.Label(janela, text="Digite o nome do arquivo:").pack(pady=(112, 10), anchor='center')  # Mover para cima
entrada_nome_arquivo = ttk.Entry(janela, width=30)  # Diminuindo a largura da entrada
entrada_nome_arquivo.pack(pady=(0, 10), padx=20, anchor='center')  # Centralizando a entrada

# Apertar botão criar video com enter
entrada_nome_arquivo.bind('<Return>', lambda event: criar_video())

# Mover o botão
botao_criar_video = ttk.Button(janela, text="Criar Video", command=criar_video)
botao_criar_video.pack(pady=(25, 10), anchor='center')  # Mover o botão para cima

# Iniciando o loop da interface
janela.mainloop()