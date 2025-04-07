import os
import json
import re
from bs4 import BeautifulSoup


html_pasta = "wikipedia_crawler/paginas"
infoboxes_pasta = "infoboxes"

# Criar pasta de infoboxes se não existir
if not os.path.exists(infoboxes_pasta):
    os.makedirs(infoboxes_pasta)


if not os.path.exists(html_pasta):
    print(f"Erro: A pasta '{html_pasta}' não foi encontrada.")
else:
    for arquivo in os.listdir(html_pasta):
        if arquivo.endswith(".html"):
            caminho_arquivo = os.path.join(html_pasta, arquivo)

            print("\n" + "=" * 40)
            print(f"Lendo: {arquivo}")
            print("=" * 40)

            with open(caminho_arquivo, "r", encoding="utf-8") as file:
                site = file.read()

            soup = BeautifulSoup(site, "html.parser")
            infobox = soup.find("table", class_="infobox")
            dados = {}

            if infobox:
                # Extrair o título da infobox
                titulo_element = (
                    infobox.find("th", class_="infobox-title")
                    or infobox.find("caption")
                    or infobox.find("th")
                )
                if titulo_element:
                    titulo = titulo_element.get_text(strip=True)
                    dados["Título da Infobox"] = titulo
                    print(f"Título da Infobox: {titulo}")
                else:
                    titulo = arquivo.replace(".html", "")
                    dados["Título da Infobox"] = titulo
                    print("Título da infobox não encontrado, usando nome do arquivo.")

                # Extrair pares chave-valor e chave-lista
                for linha in infobox.find_all("tr"):
                    # Buscar células que podem conter chaves
                    chave_element = linha.find("th") or linha.find(
                        "td", {"scope": "row"}
                    )

                    if chave_element and chave_element != titulo_element:
                        chave = chave_element.get_text(strip=True)

                        # Ignorar linhas vazias ou que parecem ser cabeçalhos de seção
                        if (
                            chave
                            and not chave_element.get("colspan")
                            and not chave == titulo
                        ):
                            # Encontrar a célula de valor
                            valor_tds = [
                                td for td in linha.find_all("td") if td != chave_element
                            ]

                            if valor_tds:
                                # Se tem apenas um TD, provavelmente é um par chave-valor simples
                                if len(valor_tds) == 1:
                                    # Substituir <br> por espaço
                                    for br in valor_tds[0].find_all("br"):
                                        br.replace_with(" ")

                                    valor_text = valor_tds[0].get_text(strip=False)

                                    # Substituir &nbsp; por espaço
                                    valor_text = valor_text.replace("\xa0", " ")

                                    # Verificar se o valor parece ser uma lista (contém bullets, quebras, etc)
                                    lista_items = valor_tds[0].find_all(["li", "br"])
                                    if lista_items:
                                        # É um par chave-lista
                                        valores = [
                                            item.get_text(strip=False).replace("\xa0", " ")
                                            for item in lista_items
                                            if item.get_text(strip=False)
                                        ]
                                        if (
                                            not valores
                                        ):  # Se não encontrou itens específicos, tente separar por vírgulas
                                            valores = [
                                                v.strip()
                                                for v in re.split(r"[,•]", valor_text)
                                                if v.strip()
                                            ]
                                        dados[chave] = valores
                                    else:
                                        # É um par chave-valor
                                        dados[chave] = valor_text
                                else:
                                    # Múltiplos TDs, pode ser estrutura complexa, unimos com separador
                                    dados[chave] = " | ".join(
                                        td.get_text(strip=True) for td in valor_tds
                                    )

                # Criar nome de arquivo baseado no título da infobox
                safe_titulo = re.sub(
                    r'[\\/*?:"<>|]', "_", titulo
                )  # Remover caracteres inválidos para nome de arquivo
                json_nome_arquivo = f"{safe_titulo}.json"

                # Salvar na pasta de infoboxes
                caminho_completo = os.path.join(infoboxes_pasta, json_nome_arquivo)
                with open(caminho_completo, "w", encoding="utf-8") as json_file:
                    json.dump(dados, json_file, ensure_ascii=False, indent=4)

                print(f"Os dados foram salvos no arquivo '{caminho_completo}'.")

            else:
                print("Infobox não encontrada.")
