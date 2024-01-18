import requests
from bs4 import BeautifulSoup
from utils.utils import convert_to_hours_ago, extract_image_urls

def scrape_gizmodo():
    # Tu código de scraping
    url = "https://es.gizmodo.com/tecnologia"
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    
    # Busca todos los elementos <article> con la clase 'recent-abstract abstract-article'
    articles = soup.find_all('article', class_='sc-cw4lnv-0 ksZQxB js_post_item')

    # Lista para almacenar los resultados
    scraped_data = []

    # Itera sobre los artículos
    for article in articles:

        # Encuentra la primera etiqueta <img> y extrae todas las URLs de imagen
        img_tag = article.find('img')
        img_urls = extract_image_urls(img_tag)
        
        # Extrae el título del artículo del elemento <h2> con la clase 'abstract-title'
        title = article.find('h2', class_='sc-759qgu-0 cDAvZo sc-cw4lnv-6 exTKuS').get_text()

        # Extrae la URL del enlace dentro de la etiqueta <a> en el div con la clase 'abstract-excerpt'
        link_url = article.find('a', class_='sc-1out364-0 dPMosf js_link')['href']

        # Extrae el contenido del artículo del elemento <div> con la clase 'abstract-excerpt'
        contenido = article.find('p', class_='sc-77igqf-0 fnnahv').get_text()

        # Encuentra la etiqueta <time> con el atributo datetime
        time_tag = article.find('time', {'datetime': True})

        # Extrae el texto contenido en la etiqueta <time> y lo convierte en "Hace X horas"
        if time_tag:
            date = convert_to_hours_ago(time_tag['datetime'])
            date_origen = time_tag['datetime']

        # Crea un diccionario con la información y agrega a la lista
        article_info = {
            'title': title,
            'img_urls': img_urls,
            'link_url': link_url,
            'content': contenido,
            'date': date,
            'date_origen': date_origen,
            'fuente': 'Gizmodo'
        }
        scraped_data.append(article_info)

    # Devuelve los resultados como JSON
    return scraped_data
