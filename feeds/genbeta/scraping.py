import requests
from bs4 import BeautifulSoup
from utils.utils import convert_to_hours_ago, extract_image_urls

def scrape_genbeta():
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

        # Encuentra la primera etiqueta <img> y extrae todas las URLs de imagen
        img_tag = article.find('img')
        img_urls = extract_image_urls(img_tag)
        
        # Extrae el título del artículo del elemento <h2> con la clase 'abstract-title'
        title = article.find('h2', class_='abstract-title').find('a').get_text()

        # Extrae la URL del enlace dentro de la etiqueta <a> en el div con la clase 'abstract-excerpt'
        link_url = article.find('div', class_='abstract-excerpt').find('a')['href']

        # Extrae el contenido del artículo del elemento <div> con la clase 'abstract-excerpt'
        contenido = article.find('div', class_='abstract-excerpt').find('p').get_text()

        # Encuentra la etiqueta <time> con el atributo datetime
        time_tag = article.find('time', {'datetime': True})

        # Extrae el texto contenido en la etiqueta <time> y lo convierte en "Hace X horas"
        if time_tag:
            date = convert_to_hours_ago(time_tag['datetime'])

        # Crea un diccionario con la información y agrega a la lista
        article_info = {
            'title': title,
            'img_urls': img_urls,
            'link_url': link_url,
            'content': contenido,
            'date': date,
            'fuente': 'Genbeta'
        }
        scraped_data.append(article_info)

    # Devuelve los resultados como JSON
    return scraped_data
