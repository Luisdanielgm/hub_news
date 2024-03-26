from pymongo import MongoClient
from gemini_group_similar import group_news
from datetime import datetime, timedelta, timezone
import json

def get_db():
    try:
        client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
        db = client['news_aixteam']
        print("Conexión a la base de datos establecida.")
        return db
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        raise

def start_group_similar_items(collection_name):
    try:
        db = get_db()
        collection = db[collection_name]

        now = datetime.now()
        last_week = now - timedelta(days=1)
        last_week_day = last_week.strftime('%Y-%m-%d')

        today_date = datetime.now().strftime("%Y_%m_%d")
        json_name = f"group_{collection_name}_{today_date}"

        print(f"Buscando elementos no agrupados en '{collection_name}'...")
        num_ungrupped_items = collection.count_documents({'date_normalized': {'$gte': last_week_day}, 'similar_group': 'no', 'filtrada': 'si'})
        print(f"Se encontraron {num_ungrupped_items} elementos no agrupados.")

        print(f"Buscando elementos no agrupados en '{collection_name}'...")
        ungrouped_items = list(collection.find({'date_normalized': {'$gte': last_week_day}, 'similar_group': 'no', 'filtrada': 'si'}))

        # Iterar sobre cada elemento
        for i, item1 in enumerate(ungrouped_items):

            if i < len(ungrouped_items) - 1:

                print(f"Elemento {i+1}:")

                # Iterar sobre los elementos posteriores al elemento actual
                for j, item2 in enumerate(ungrouped_items[i+1:], start=i+2):
                    print(f"Comparando {i+1} con elemento {j}:")
                    
                    # guardar title y content en una variable
                    title1 = item1.get('title', '')
                    text1 = item1.get('spanish', '')
                    content1 = text1

                    title2 = item2.get('title', '')
                    text2 = item2.get('spanish', '')
                    content2 = text2

                    print(f"{i+1}- {content1}")
                    print(f"{j}- {content2}")

                    # Llamar a la funciãn group_news
                    similar_news = group_news(content1, content2)

                    if similar_news != None:
                        positive_responses = ['si', 'sí', 'yes']
                        if similar_news.lower() in positive_responses:
                            print(f"Similar News: {similar_news}")
                            #collection.update_one({'_id': item1['_id']}, {'$set': {'similar_group': 'si', 'similar_news': similar_news}})
                        else:
                            print(f"Similar News: {similar_news}")
                            #collection.update_one({'_id': item1['_id']}, {'$set': {'similar_group': 'no'}})

                print(f"--------------------------------------")

        print(f"Proceso de agrupación para '{collection_name}' completado.")
    except Exception as e:
        print(f"Error en start_group_similar_items para '{collection_name}': {e}")
        raise

def group_similar_news():
    try:
        start_group_similar_items('tweets')
        print("Agrupación de noticias similares completada.")
    except Exception as e:
        print("Error al agrupar noticias similares:", e)


group_similar_news()