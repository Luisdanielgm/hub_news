import aiohttp
import asyncio
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import ObjectId
from utils.utils import convert_to_hours_ago
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


def extract_image_urls(picture_tag):
    if not picture_tag:
        print('Picture tag no encontrada')
        return []

    img_urls = []

    # Revisa primero si hay un 'img' con 'data-src' o 'data-srcset'
    img_tag = picture_tag.find('img')
    if img_tag:
        data_src = img_tag.get('data-src')
        if data_src and data_src.startswith('https://'):
            img_urls.append(data_src)

        data_srcset = img_tag.get('data-srcset')
        if data_srcset:
            # Extrae todas las posibles URLs de data-srcset
            urls = [src.split()[0] for src in data_srcset.split(',') if src.startswith('https://')]
            img_urls.extend(urls)

    # Revisa si hay elementos 'source' con 'data-srcset'
    sources = picture_tag.find_all('source')
    for source in sources:
        data_srcset = source.get('data-srcset')
        if data_srcset:
            urls = [src.split()[0] for src in data_srcset.split(',') if src.startswith('https://')]
            img_urls.extend(urls)

    return list(set(img_urls))  # Elimina duplicados


async def scrape_gizmodo():
    try:
        # Conexión a MongoDB
        client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
        db = client['news_aixteam']
        collection = db['news']

        url = "https://es.gizmodo.com/tecnologia"
        content = await fetch(url)
        soup = BeautifulSoup(content, 'html.parser')

        articles = soup.find_all('article')
        scraped_data = []

        for article in articles:
            picture_tag = article.find('picture')
            img_urls = extract_image_urls(picture_tag)
            title = article.find('h2', class_='sc-759qgu-0 cDAvZo sc-cw4lnv-6 exTKuS').get_text()
            link_url = article.find('a', class_='sc-1out364-0 dPMosf js_link')['href']
            contenido = article.find('p', class_='sc-77igqf-0 fnnahv').get_text()
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
                'fuente': 'Gizmodo',
                'read': 'no',
                'filtrada': 'nf',
                'traducido': 'no',
                'spanish': '',
                'regenerate': 'no',
                'newregenerate': '',
                'imgregenerate': '',
                "categories": "nc"
            }

            if not article_exists(collection, link_url):
                print('-- Nueva noticia en Gizmodo agregada:')
                print(article_info)
                print('-------------------------------------')
                inserted_article = collection.insert_one(article_info).inserted_id
                article_info['_id'] = ObjectIdToStr(inserted_article)
                scraped_data.append(article_info)

        return scraped_data

    except Exception as e:
        logging.error(f"Error durante el scraping de Gizmodo: {e}")
        return []

# Función para ejecutar el scraping de forma asíncrona
def run_scraping():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(scrape_gizmodo())