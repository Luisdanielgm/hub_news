from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Definición de la ruta para el scraping
@app.route('/genbeta', methods=['GET'])
def scrape_website():
    # Tu código de scraping
    url = "https://www.genbeta.com/tag/inteligencia-artificial"
    respuesta = requests.get(url)
    contenido = respuesta.content
    soup = BeautifulSoup(contenido, 'html.parser')
    
    # Busca todos los elementos <article> con la clase 'recent-abstract abstract-article'
    articulos = soup.find_all('article', class_='recent-abstract abstract-article')

    # Lista para almacenar los resultados
    scraped_data = []

    # Itera sobre los artículos
    for articulo in articulos:
        # Extrae la URL de la imagen del primer elemento <img>
        img_url = articulo.find('img')['src']
        
        # Extrae el título del artículo del elemento <h2> con la clase 'abstract-title'
        titulo = articulo.find('h2', class_='abstract-title').find('a').get_text()

        # Extrae el contenido del artículo del elemento <div> con la clase 'abstract-excerpt'
        contenido = articulo.find('div', class_='abstract-excerpt').find('p').get_text()

        # Crea un diccionario con la información y agrega a la lista
        articulo_info = {
            'titulo': titulo,
            'img_url': img_url,
            'contenido': contenido
        }
        scraped_data.append(articulo_info)

    # Devuelve los resultados como JSON
    return jsonify({'data': scraped_data})

if __name__ == '__main__':
    # Puedes cambiar el puerto aquí
    # puerto = 8080
    app.run(debug=True)