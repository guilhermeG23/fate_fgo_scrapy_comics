#Libs necessarias
from bs4 import BeautifulSoup
import wget
import requests
import os
import img2pdf
from PIL import Image
import sys

"""
Opcao de escala de cinza
"""
gray_scale = False
try:
    if sys.argv[1] == "gray":
        gray_scale = True
except:
    pass

"""
Links para o site
"""
url_raiz = "https://fate-go.us/manga_fgo3/"
#url_raiz = "https://fate-go.us/manga_fgo2/"
#url_raiz = "https://fate-go.us/manga_fgo/"
url = url_raiz
logo = "{}images/common/logo.png".format(url)

"""
Extrair as imagens
"""
saida = requests.get(url, headers={'User-Agent': 'Custom'})
html = BeautifulSoup(saida.text, 'html.parser')
titulos = html.findAll('img')

"""
Array dos comics existentes
"""
comics = []

"""
Pegar todos os comics
"""
for i in titulos:
    if str(str(i).find("Episdoe")) != "-1":
        a = str(i).split("/")
        comics.append(a[3])

"""
Criar pastas necessarias
"""
if os.path.exists("comics") == False:
    os.mkdir("comics")

if os.path.exists("comics_convertidos") == False:
    os.mkdir("comics_convertidos")

"""
Buscar todos os valores do comics
"""
ja_existem = os.listdir("comics")

"""
Confirmar se ja existe o logo
"""
try:
    ja_existem.index("comic00.png")
except:
    wget.download(logo, bar=None)
    os.rename("logo.png", "comics/comic00.png")

"""
Download dos comics
"""
for comic in comics:
    """
    Se der errado o try, ele busca o download
    """
    try:
        ja_existem.index("{}.png".format(comic))
    except:
        """
        Try é para buscar a primeira img que e diferente de todas
        Except busca todos os demais que ficam só nomeados de comic
        """
        try:
            urlDownload = "{}images/{}/comic.png".format(url, comic)
            wget.download(urlDownload, bar=None)
            os.rename("comic.png", "comics/{}.png".format(comic))
        except:
            urlDownload = "{}images/{}/{}.png".format(url, comic, comic)
            wget.download(urlDownload, bar=None)
            os.rename("{}.png".format(comic), "comics/{}.png".format(comic))

"""
Convertendo as imagens
"""
for img in ja_existem:
    im = Image.open("comics\\{}".format(img))
    rgb_im = im.convert('RGB')
    if gray_scale:
        rgb_im = rgb_im.convert('L')
    rgb_im.save('comics_convertidos\\{}.jpg'.format(img.split(".")[0]))

"""
Buscando o caminho das imagens
"""
ja_existem = os.listdir("comics_convertidos")
lista_imagens = []
for img in ja_existem:
    lista_imagens.append("comics_convertidos\{}".format(img))

"""
Convertendo em pdf
"""
nome_manga = url_raiz.split("/")[3]
nome_arquivo = "comics_fate_{}".format(nome_manga)
if gray_scale:
    nome_arquivo = "{}_cinza.pdf".format(nome_arquivo)
else:
    nome_arquivo = "{}_colorido.pdf".format(nome_arquivo)

with open(nome_arquivo,"wb") as f:
	f.write(img2pdf.convert(lista_imagens))     
