import aiohttp
import asyncio
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import ObjectId
from utils.utils import convert_to_hours_ago
import logging
import resend
import os
import re
import dotenv
from utils.gemini_new_title_article import new_title_article
from utils.gemini_new_article import new_article
from utils.gemini_new_keys_words import new_keys_words

dotenv.load_dotenv()
resend.api_key = os.getenv('RESEND_API_KEY')

def send_email(subject, html_content, email):
    try:

        params = {
            "from": "AITeam <redactor@webflowsolution.lat>",
            "to": [email],
            "subject": f"""{subject}""",
            "html": f"""{html_content}""",
        }

        email = resend.Emails.send(params)
        print('Email enviado:', email)

    except Exception as e:
        logging.error(f"Error sending email: {e}")

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


async def scrape_therundown():
    try:
        # Conexión a MongoDB
        client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
        db = client['news_aixteam']
        collection = db['news']

        url = "https://www.therundown.ai/"
        content = await fetch(url)
        soup = BeautifulSoup(content, 'html.parser')

        print('iniciando scraping a therundown.ai')

        articles_content = soup.find('div', class_='grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3')
        articles = articles_content.find_all('div', class_='group h-full overflow-hidden transition-all shadow-none hover:shadow-xl rounded-md')

        scraped_data = []

        for article in articles:

            article_link = article.find('a')

            if not article_link:
                continue

            link_url = 'https://www.therundown.ai' + article_link['href']
            time_tag = article.find('time', {'datetime': True})

            if time_tag:
                date_result, date_normalized = convert_to_hours_ago(time_tag['datetime'])
                date_origen = time_tag['datetime']
            
            # Comprobamos si la noticia ya existe
            if article_exists(collection, link_url):
                continue

            # Extraemos el contenido de la noticia
            article_content = await fetch(link_url)
            article_soup = BeautifulSoup(article_content, 'html.parser')

            content_blocks = article_soup.find(id='content-blocks')

            # iterar por los hijos de content_blocks
            for child in content_blocks.children:
                article_texto_all = ''
                if child.name == 'style':
                    continue
                elif child.name == 'div' and child.get('style') == 'background-color:#FFFFFF;border-color:#000000;border-radius:10px;border-style:solid;border-width:2px;margin:0px 0px 0px 0px;padding:0px 0px 0px 0px;':
                    child_div = child
                    for child_in_child_div in child_div.children:
                        if child_in_child_div.name == 'p':
                            continue
                        elif child_in_child_div.name == 'style':
                            continue
                        else:
                            article_texto_all += child_in_child_div.text + '\n\n'

                    article_info = {
                        'type': 'feed',
                        'title': '',
                        'img_urls': '',
                        'link_url': link_url,
                        'content': article_texto_all,
                        'date': date_result,
                        'date_normalized': date_normalized,
                        'date_origen': date_origen,
                        'fuente': 'Therundown',
                        'read': 'no',
                        'filtrada': 'nf',
                        'traducido': 'no',
                        'spanish': '',
                        'regenerate': 'no',
                        'newregenerate': '',
                        'imgregenerate': '',
                        "categories": "no",
                        "similar_group": "no",
                        "added_keywords": "no"
                    }

                    inserted_article = collection.insert_one(article_info).inserted_id
                    article_info['_id'] = ObjectIdToStr(inserted_article)
                    scraped_data.append(article_info)

                    print('Articulo: ', article_info)

                    print('Articulo de Newsletter Therundown: ----------------------------------------------')
                else:
                    continue
                    


            
            if not article_exists(collection, link_url):
                print('-- Nueva noticia en TheRundown agregada:')
                print(article_info)
                print('-------------------------------------')
                inserted_article = collection.insert_one(article_info).inserted_id
                article_info['_id'] = ObjectIdToStr(inserted_article)
                scraped_data.append(article_info)

                
        print(f"Se han extraido {len(scraped_data)} noticias de Therundown.")
        return scraped_data

    except Exception as e:
        logging.error(f"Error durante el scraping de Therundown: {e}")
        return []

# Función para ejecutar el scraping de forma asíncrona
def run_scraping():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(scrape_therundown())