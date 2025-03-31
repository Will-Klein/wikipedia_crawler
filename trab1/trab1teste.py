import os
import json
from bs4 import BeautifulSoup


html_pasta = "paginas-teste/testes-infoboxes"


if not os.path.exists(html_pasta):
    print(f"Erro: A pasta '{html_pasta}' não foi encontrada.")
else:
    for arquivo in os.listdir(html_pasta):
        if arquivo.endswith(".html"):
            caminho_arquivo = os.path.join(html_pasta, arquivo)

            print("\n" + "="*40)
            print(f"Lendo: {arquivo}")
            print("="*40)

            
            with open(caminho_arquivo, "r", encoding="utf-8") as file:
                site = file.read()

            
            soup = BeautifulSoup(site, "html.parser")
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

                
                json_nome_arquivo = f"infobox_{arquivo.replace('.html', '')}.json"
                with open(json_nome_arquivo, "w", encoding="utf-8") as json_file:
                    json.dump(dados, json_file, ensure_ascii=False, indent=4)

                print(f"Os dados foram salvos no arquivo '{json_nome_arquivo}'.")

            else:
                print("Infobox não encontrada.")
