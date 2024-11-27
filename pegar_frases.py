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
