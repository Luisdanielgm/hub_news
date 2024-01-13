# Función para realizar el scraping de una URL específica
def scrape_inner_content(inner_url):
    response = requests.get(inner_url)
    inner_content = response.content
    inner_soup = BeautifulSoup(inner_content, 'html.parser')
    
    # Busca el contenido dentro de la etiqueta <div> con la clase 'article-content'
    inner_contenido = inner_soup.find('div', class_='article-content')
    
    # Extrae el texto del contenido
    if inner_contenido:
        return inner_contenido.get_text(strip=True)
    else:
        return None

# Definición de la ruta para el scraping
@app.route('/genbeta', methods=['GET'])
def scrape_website():
    # Tu código de scraping
    url = "https://www.genbeta.com/tag/inteligencia-artificial"
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    
    # Busca todos los elementos <article> con la clase 'recent-abstract abstract-article'
    articles = soup.find_all('article', class_='recent-abstract abstract-article')

    # Lista para almacenar los resultados
    scraped_data = []

    # Itera sobre los artículos
    for article in articles:
        # Extrae la URL de la imagen del primer elemento <img>
        img_url = article.find('img')['src']
        
        # Extrae el título del artículo del elemento <h2> con la clase 'abstract-title'
        title = article.find('h2', class_='abstract-title').find('a').get_text()

        # Extrae la URL del enlace dentro de la etiqueta <a> en el div con la clase 'abstract-excerpt'
        link_url = article.find('div', class_='abstract-excerpt').find('a')['href']

        # Realiza el scraping de la URL interna para obtener el contenido adicional
        inner_content = scrape_inner_content(link_url)

        # Crea un diccionario con la información y agrega a la lista
        article_info = {
            'title': title,
            'img_url': img_url,
            'link_url': link_url,
            'inner_content': inner_content
        }
        scraped_data.append(article_info)

    # Devuelve los resultados como JSON
    return jsonify({'data': scraped_data})

# Ejecuta la aplicación si se ejecuta este script
if __name__ == '__main__':
    app.run(debug=True)