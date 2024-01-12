from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/genbeta', methods=['GET'])
def scrape_website():
    # Tu código de scraping
    url = "https://www.genbeta.com/tag/inteligencia-artificial"
    respuesta = requests.get(url)
    contenido = respuesta.content
    soup = BeautifulSoup(contenido, 'html.parser')
    resultados = soup.find_all('h2', 'abstract-title')

    # Lista para almacenar los resultados
    scraped_data = []

    for resultado in resultados:
        enlace = resultado.find('a')
        texto = enlace.get_text()
        scraped_data.append(texto)

    # Devolvemos los resultados como JSON
    return jsonify({'data': scraped_data})

if __name__ == '__main__':
    # Puedes cambiar el puerto aquí
    # puerto = 8080
    app.run(debug=True)