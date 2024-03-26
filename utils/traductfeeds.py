from pymongo import MongoClient
from utils.geminidespanol import generate_detecta_espanol
from utils.gemini import generate_translation
from datetime import datetime, timedelta, timezone

def get_db():
    try:
        client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
        db = client['news_aixteam']
        print("Conexión a la base de datos establecida.")
        return db
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        raise

def translate_untranslated_items(collection_name):
    try:
        db = get_db()
        collection = db[collection_name]

        now = datetime.now()
        last_week = now - timedelta(days=7)
        last_week_day = last_week.strftime('%Y-%m-%d')

        print(f"Buscando elementos no traducidos en '{collection_name}'...")
        num_untranslated_items = collection.count_documents(
            {   'date_normalized': {'$gte': last_week_day},
                'traducido': 'no'
            })
        print(f"Se encontraron {num_untranslated_items} elementos no traducidos.")

        untranslated_items = collection.find(
            {
                'date_normalized': {'$gte': last_week_day},
                'traducido': 'no'
                })

        num_translated_items = 0

        for item in untranslated_items:
            try:
                if item['type'] == 'tweet' or item['type'] == 'feed':

                    content = item.get('content', '')
                    if not content:
                        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        print(f"El contenido para {item['_id']} está vacío o no existe. No se realiza traducción.")
                        collection.update_one({'_id': item['_id']}, {'$set': {'content': '', 'spanish': '', 'traducido': 'na'}})
                        continue


                    translated_content = generate_translation(item['content'])

                    if translated_content is not None:
                        
                        verification_laguage = generate_detecta_espanol(translated_content)

                        if verification_laguage is not None:

                            positive_responses = ['si', 'sí', 'yes']

                            if verification_laguage.lower() in positive_responses:
                                es_traducido = 'si'
                                collection.update_one({'_id': item['_id']}, {'$set': {'spanish': translated_content, 'traducido': es_traducido}})
                                num_translated_items += 1
                                print(f"-------------------------------")
                                print(f"Traducción completada para: {item['_id']}")
                                print(f"Contenido original: {item['content']}")
                                print(f"Contenido traducido: {translated_content}")
                            else:
                                print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                print(f"La traducción para {item['_id']} no es español. No se guarda la traducción.")
                                print(f"contenido original: {item['content']}")
                                print(f"Contenido traducido: {translated_content}")
                        else:
                            print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print(f"La traducción para {item['_id']} es None. No se guarda la traducción.")
                            print(f"contenido no traducido: {item['content']}")
                    else:
                        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        print(f"La traducción para {item['_id']} es None. No se guarda la traducción.")
                        print(f"contenido no traducido: {item['content']}")

            except Exception as e:
                print(f"Error al traducir o actualizar el elemento {item['_id']}: {e}")

        print(f"Proceso de traducción para '{collection_name}' completado.")
        print(f"Total de elementos traducidos: {num_translated_items}")
        print(f"Total de elementos no traducidos restantes: {num_untranslated_items - num_translated_items}")
    except Exception as e:
        print(f"Error en translate_untranslated_items para '{collection_name}': {e}")
        raise

def translate_news_and_tweets():
    try:
        #translate_untranslated_items('news') obviado debido a que no tengo fuentes feeds en ingles
        translate_untranslated_items('tweets')
        translate_untranslated_items('news')
        print("Traducción de noticias y tweets completada.")
    except Exception as e:
        print("Error al traducir noticias y tweets:", e)
