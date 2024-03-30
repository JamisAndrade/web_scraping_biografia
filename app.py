from flask import Flask, jsonify
from googlesearch import search
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def obter_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        return None

def extrair_conteudo(html):
    soup = BeautifulSoup(html, 'html.parser')
    biography_span = soup.find('span', {'class': 'mw-headline', 'id': 'Biography'})
    if biography_span:
        biography_content = []
        next_element = biography_span.find_next()
        while next_element and next_element.name != 'h2':
            if next_element.name == 'p':
                biography_content.append(next_element.get_text())
            next_element = next_element.find_next()
        return '\n'.join(biography_content).strip()
    else:
        return None

@app.route('/api/biografia_politico/<nome_politico>')
def obter_biografia_politico(nome_politico):
    query = "ballotpedia " + nome_politico
    try:
        search_results = next(search(query, num_results=1), None)
        if search_results:
            url = search_results
            html = obter_html(url)
            if html:
                conteudo_biografia = extrair_conteudo(html)
                if conteudo_biografia:
                    return jsonify({"biografia": conteudo_biografia})
                else:
                    return jsonify({"mensagem": "Biografia não encontrada."}), 404
            else:
                return jsonify({"mensagem": "Erro ao obter HTML da página."}), 500
        else:
            return jsonify({"mensagem": "Nenhum resultado encontrado."}), 404
    except Exception as e:
        return jsonify({"mensagem": f"Erro ao realizar a pesquisa: {e}"}), 500

# Listando as rotas após a execução do aplicativo
print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)
