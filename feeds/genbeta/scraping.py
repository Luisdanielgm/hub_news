import aiohttp
import asyncio
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import ObjectId
from utils.utils import convert_to_hours_ago, extract_image_urls
import logging
import resend
import os
import dotenv
import re
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

async def scrape_genbeta():
    try:
        # Conexión a MongoDB
        client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
        db = client['news_aixteam']
        collection = db['news']

        url = "https://www.genbeta.com/categoria/inteligencia-artificial"
        content = await fetch(url)
        soup = BeautifulSoup(content, 'html.parser')

        articles = soup.find_all('article', class_='recent-abstract abstract-article')
        scraped_data = []

        for article in articles:
            img_tag = article.find('img')
            img_urls = extract_image_urls(img_tag)
            title = article.find('h2', class_='abstract-title').find('a').get_text()
            link_url = article.find('h2', class_='abstract-title').find('a')['href']
            time_tag = article.find('time', {'datetime': True})

            if time_tag:
                date_result, date_normalized = convert_to_hours_ago(time_tag['datetime'])
                date_origen = time_tag['datetime']

            article_info = {
                'type': 'feed',
                'title': title,
                'img_urls': img_urls,
                'link_url': link_url,
                'content': '',
                'date': date_result,
                'date_normalized': date_normalized,
                'date_origen': date_origen,
                'fuente': 'Genbeta',
                'read': 'no',
                'filtrada': 'nf',
                'traducido': 'na',
                'spanish': '',
                'regenerate': 'no',
                'newregenerate': '',
                'imgregenerate': '',
                "categories": "no",
                "similar_group": "no",
                "added_keywords": "no"
            }


            if not article_exists(collection, link_url):
                print('-- Nueva noticia en Genbeta agregada:')
                print(article_info)
                print('-------------------------------------')
                inserted_article = collection.insert_one(article_info).inserted_id
                article_info['_id'] = ObjectIdToStr(inserted_article)
                scraped_data.append(article_info)

                full_link_url = article_info['link_url']
                full_content_article = await fetch(full_link_url)
                full_content_soup = BeautifulSoup(full_content_article, 'html.parser')

                title_full = full_content_soup.find('h1', class_='post-title').get_text()
                texts_full_divi = full_content_soup.find('div', class_='article-content')
                texts_full = texts_full_divi.find('div', class_='blob js-post-images-container')

                full_img = full_content_soup.find('main').find('header').find('picture').find('img')['src']

                extracted_text = ''

                for element in texts_full.children:
                    if element.name == 'div':
                        continue
                    
                    else:
                        text = element.get_text(strip=True)
                        text_lower = text.lower()
                        exclusion_strings = ['imágenes', 'imágenes |', 'imágenes: ', 'imagen', 'imagen: ', 'imagen |', 'más información: ', 'más información', 'más información |', 'en genbeta:', 'en genbeta |']

                        if any(text_lower.startswith(s) for s in exclusion_strings):
                            continue
                        else:
                            extracted_text += text + '\n\n'

                extracted_text = re.sub(r'https?://\S+|www\.\S+|[^A-Za-z0-9]+', ' ', extracted_text)
                extracted_text = extracted_text.lower()

                print('Generando nuevo título...')
                title_text = new_title_article(title_full)
                if title_text == None:
                    continue

                # limpiar el titulo de los caracteres *
                title_text = title_text.replace('*', '')


                print('Generando nuevo articulo...')
                extracted_text = new_article(extracted_text)
                if extracted_text == None:
                    continue

                # extraer de extracted_text solo el contenido dentro de las etiquetas <article> y </article>
                extracted_text = re.findall(r'<article>(.*?)</article>', extracted_text, re.DOTALL)[0]
                if re.search(r'<h1>.*?</h1>', extracted_text) is None:
                    print("No se encontraron etiquetas h1 en extracted_text.")
                else:

                    extracted_text = re.sub(r'<h1>(.*?)</h1>', r'<h3>\1</h3>', extracted_text)

                first_p = re.findall(r'<p>(.*?)</p>', extracted_text, re.DOTALL)[0]

                print('Generando palabras claves...')
                keyWords_text = new_keys_words(title_full, extracted_text)
                if keyWords_text == None:
                    continue


                html_content = f'<!DOCTYPE html><html><body><center><article>'

                html_content += f'{extracted_text}'
                    
                html_content += f'</article><img src="{full_img}" alt="{title_text}" />'

                html_content += '</center>'

                html_content += f'<p>Fuente: <a href="{full_link_url}">{full_link_url}</a></p>'

                html_content += f'<p>[status pending][tags {keyWords_text}][category Inteligencia Artificial][excerpt]{first_p}[/excerpt]</p>'

                html_content += '</body></html>'

                print('Enviando correos...')
                send_email(title_text, html_content, 'luisdanielgm19@gmail.com')
                send_email(title_text, html_content, 'hilo214cecu@post.wordpress.com')


        print(f"Se han extraido {len(scraped_data)} noticias de Genbeta.")
        return scraped_data

    except Exception as e:
        logging.error(f"Error durante el scraping de Genbeta: {e}")
        return []

# Función para ejecutar el scraping de forma asíncrona
def run_scraping():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(scrape_genbeta())