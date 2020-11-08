#Libs necessarias
from bs4 import BeautifulSoup
import wget
import requests
import os

#Links para o site
url = "https://fate-go.us/manga_fgo2/"
logo = "https://fate-go.us/manga_fgo2/images/common/logo.png"

#Extrair as imagens
saida = requests.get(url, headers={'User-Agent': 'Custom'})
html = BeautifulSoup(saida.text, 'html.parser')
titulos = html.findAll('img')

#Array dos comics existentes
comics = []

#Pegar todos os comics
for i in titulos:
    if str(str(i).find("Episdoe")) != "-1":
        a = str(i).split("/")
        comics.append(a[3])

#Criar pasta
if os.path.exists("comics") == False:
    os.mkdir("comics")

#Buscar todos os valores do comics
ja_existem = os.listdir("comics")

#Confirmar se ja existe o logo
try:
    ja_existem.index("logo.png")
except:
    wget.download(logo, bar=None)
    os.rename("logo.png", "comics/logo.png")

#Download dos comics
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
            url = "https://fate-go.us/manga_fgo2/images/{}/comic.png".format(comic)
            wget.download(url, bar=None)
            os.rename("comic.png".format(comic), "comics/{}.png".format(comic))
        except:
            url = "https://fate-go.us/manga_fgo2/images/{}/{}.png".format(comic, comic)
            wget.download(url, bar=None)
            os.rename("{}.png".format(comic), "comics/{}.png".format(comic))
