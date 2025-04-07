import os
import time
import requests
from bs4 import BeautifulSoup

# Função para coletar links presentes na página passada por parâmetro
def coletar_links(pag):
    todos_links = pag.find(id="bodyContent").find_all("a")
    coletados = set(
        filtrar_links(todos_links)
    )  # Uso de set para não ter links repetidos
    return coletados


# OBS: todos_links é uma coleção de links não filtrados


# Função para filtrar os links para salvar apenas verbetes
def filtrar_links(conj_links):
    links = []
    for link in conj_links:
        if "href" in link.attrs.keys() and link["href"].startswith("/wiki/"):
            if ":" not in link["href"]:  # verbetes não tem :
                links.append(link["href"])
                # append inserção no fim
    return links


# Função que salva uma página
def salvar_pagina(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica erros HTTP
        soup = BeautifulSoup(response.content, "html.parser")
        if soup.select(".mw-page-title-main"):
            titulo = soup.select(".mw-page-title-main")[0].text

            # Evitar que tenha caracteres invalidos no nome do arquivo
            titulo_formatado = (
                titulo.replace(" ", "_")
                .replace("/", "_")
                .replace("?", "")
                .replace(":", "")
            )
            # Criando pasta para organizar todas as paginas
            os.makedirs("paginas", exist_ok=True)

            caminho_arquivo = f"paginas/{titulo_formatado}.html"
            if "Página_principal" in titulo_formatado:
                return soup
            else:
                with open(caminho_arquivo, "w", encoding="utf-8") as f:
                    f.write(response.text)

                print(f"Pagina salva: {caminho_arquivo}")

                return soup
        else:
            return

    except requests.RequestException as e:
        print(f"Erro ao baixar {url}: {e}")


# Função para formatar a URL completa da Wikipedia
def formatar_url(link):
    return f"https://pt.wikipedia.org{link}"


# Função que verifica se a URL já foi visitada
def foi_visitado(url, visitados):
    return url in visitados


def main():
    pag_inicial = "https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal"
    visitados = set()
    para_visitar = [pag_inicial]

    while len(visitados) < 5001 and para_visitar:  # Continua se tiver URL para visitar
        url = para_visitar.pop(0)

        if foi_visitado(url, visitados):
            continue

        soup = salvar_pagina(url)
        if soup is None:
            continue  # Deu erro ao salvar? Pula!

        visitados.add(url)
        print(visitados)

        novos_links = coletar_links(soup)
        for link in novos_links:
            url_formatada = formatar_url(link)
            if (
                not foi_visitado(url_formatada, visitados)
                and url_formatada not in para_visitar
            ):
                para_visitar.append(url_formatada)

        time.sleep(1)

    print(f"Coleta concluída. {len(visitados)-1} verbetes salvos.")


# Executar a função principal quando o script é executado diretamente
if __name__ == "__main__":
    main()
