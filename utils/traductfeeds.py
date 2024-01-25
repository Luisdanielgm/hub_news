from pymongo import MongoClient
from utils.geminidespanol import generate_detecta_espanol
from utils.gemini import generate_translation
import re

def get_db():
    try:
        client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
        db = client['news_aixteam']
        print("Conexión a la base de datos establecida.")
        return db
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        raise

def translate_untranslated_items(collection_name, limit=400):
    try:
        db = get_db()
        collection = db[collection_name]

        print(f"Buscando {limit} elementos no traducidos en '{collection_name}'...")
        untranslated_items = collection.find({'traducido': 'no'}).limit(limit)

        for item in untranslated_items:
            print(f"Traduciendo: {item['_id']}")
            try:
                # Traducir el contenido
                language_result = generate_detecta_espanol(item['content'], item['title'])

                language_responses = ['español', 'spanish']

                if language_result.lower() in language_responses:
                    translated_content = item['content']
                    translated_title = item['title']
                    es_traducido = 'na'
                else:
                    translated_content = generate_translation(item['content'])
                    translated_title = generate_translation(item['title'])
                    es_traducido = 'si'

                # Imprimir contenido original y traducido
                print(f"Contenido original: {item['content']}")
                print(f"Contenido traducido: {translated_content}")

                # Actualizar el elemento con la traducción y marcarlo como traducido
                collection.update_one({'_id': item['_id']}, {'$set': {'spanish': translated_content, 'traducido': es_traducido}})
                print(f"Traducción completada para: {item['_id']}")
            except Exception as e:
                print(f"Error al traducir o actualizar el elemento {item['_id']}: {e}")

        print(f"Proceso de traducción para '{collection_name}' completado.")
    except Exception as e:
        print(f"Error en translate_untranslated_items para '{collection_name}': {e}")
        raise

def translate_news_and_tweets():
    try:
        translate_untranslated_items('news')
        translate_untranslated_items('tweets')
        print("Traducción de noticias y tweets completada.")
    except Exception as e:
        print("Error al traducir noticias y tweets:", e)
