import aiohttp
import asyncio
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import ObjectId
from utils.utils import convert_to_hours_ago, extract_image_urls
import logging

# Función auxiliar para convertir ObjectId a str
def ObjectIdToStr(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError

# Función auxiliar para verificar si un artículo ya existe en la base de datos
def article_exists(collection, link_url):
    return collection.count_documents({'link_url': link_url}) > 0

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def scrape_genbeta():
    try:
        # Conexión a MongoDB
        client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
        db = client['news_aixteam']
        collection = db['news']

        url = "https://www.genbeta.com/tag/inteligencia-artificial"
        content = await fetch(url)
        soup = BeautifulSoup(content, 'html.parser')

        articles = soup.find_all('article', class_='recent-abstract abstract-article')
        scraped_data = []

        for article in articles:
            img_tag = article.find('img')
            img_urls = extract_image_urls(img_tag)
            title = article.find('h2', class_='abstract-title').find('a').get_text()
            link_url = article.find('div', class_='abstract-excerpt').find('a')['href']
            contenido = article.find('div', class_='abstract-excerpt').find('p').get_text()
            time_tag = article.find('time', {'datetime': True})

            if time_tag:
                date_result, date_normalized = convert_to_hours_ago(time_tag['datetime'])
                date_origen = time_tag['datetime']

            article_info = {
                'type': 'feed',
                'title': title,
                'img_urls': img_urls,
                'link_url': link_url,
                'content': contenido,
                'date': date_result,
                'date_normalized': date_normalized,
                'date_origen': date_origen,
                'fuente': 'Genbeta',
                'read': 'no',
                'filtrada': 'nf',
                'traducido': 'no',
                'spanish': '',
                'regenerate': 'no',
                'newregenerate': '',
                'imgregenerate': ''
            }


            if not article_exists(collection, link_url):
                print('-- Nueva noticia en Genbeta agregada:')
                print(article_info)
                print('-------------------------------------')
                inserted_article = collection.insert_one(article_info).inserted_id
                article_info['_id'] = ObjectIdToStr(inserted_article)
                scraped_data.append(article_info)

        return scraped_data

    except Exception as e:
        logging.error(f"Error durante el scraping de Genbeta: {e}")
        return []

# Función para ejecutar el scraping de forma asíncrona
def run_scraping():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(scrape_genbeta())