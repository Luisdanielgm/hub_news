from pymongo import MongoClient
from utils.gemini_regenerate_news import regenerate_news
from utils.gemini_regenerate_prompt_img import regenerate_prompt_img
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

def regenerate_news_item(collection_name, limit=400):
    try:
        db = get_db()
        collection = db[collection_name]

        now = datetime.now()
        last_week = now - timedelta(days=7)
        last_week_day = last_week.strftime('%Y-%m-%d') 

        print(f"Buscando {limit} elementos no regenerate en '{collection_name}'...")
        news_items = collection.find(
            {
                'date_normalized': {'$gte': last_week_day},
                'regenerate': 'no'
            }).limit(limit)

        for item in news_items:
            print(f"Regenerando: {item['_id']}")
            try:
                # Filtrar el contenido
                regenerate_content = regenerate_news(item['title'], item['content'])
                regenerate_img = regenerate_prompt_img(item['title'], item['content'])

                # Imprimir contenido original y traducido
                print(f"Contenido original: {item['title']} - {item['content']}")
                print(f"Resultado: {regenerate_content}")

                collection.update_one({'_id': item['_id']}, {'$set': {'newregenerate': regenerate_content, 'imgregenerate': regenerate_img, 'regenerate': 'si'}})

                print(f"Regeneración completada para: {item['_id']}")
            except Exception as e:
                print(f"Error al regenerar o actualizar el elemento {item['_id']}: {e}")

        print(f"Proceso de regeneración para '{collection_name}' completado.")
    except Exception as e:
        print(f"Error en regenerate_news_item para '{collection_name}': {e}")
        raise

def regenerate_news_and_tweets():
    try:
        regenerate_news_item('news')
        regenerate_news_item('tweets')
        print("Regeneración de noticias y tweets completada.")
    except Exception as e:
        print("Error al regenerar noticias y tweets:", e)
