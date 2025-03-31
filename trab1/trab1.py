import os
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen

site = "https://pt.wikipedia.org/wiki/Alan_Turing"
html = urlopen(site)

soup = BeautifulSoup(html, "html.parser")

infobox = soup.find("table", class_="infobox")

dados = {}

if infobox:
    titulo = infobox.find("th").get_text(strip=True)
    dados["Título da Infobox"] = titulo

    for linha in infobox.find_all("tr"):
        chave_td = linha.find("td", {"scope": "row"})  
        valores_td = linha.find_all("td")  

        if chave_td and len(valores_td) > 1:
            chave = chave_td.get_text(strip=True)
            valor = " | ".join(td.get_text(strip=True) for td in valores_td[1:])
            dados[chave] = valor

    
    with open("infobox_alan_turing.json", "w", encoding="utf-8") as json_file:
        json.dump(dados, json_file, ensure_ascii=False, indent=4)

    print("Os dados foram salvos no arquivo 'infobox_alan_turing.json'.")

else:
    print("Infobox não encontrada.")
