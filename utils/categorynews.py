from pymongo import MongoClient
from utils.geminicategory_news import category_news
from utils.geminicategory_tuto import category_tuto
from utils.geminicategory_paper import category_paper
from utils.geminicategory_hm import category_hm
from utils.geminicategory_demo import category_demo
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

def category_unfiltrated_items(collection_name, limit=400):
    try:
        db = get_db()
        collection = db[collection_name]

        now = datetime.now()
        last_week = now - timedelta(days=7)
        last_week_day = last_week.strftime('%Y-%m-%d') 

        print(f"Buscando elementos no categorizados en '{collection_name}'...")
        num_uncategorized_items = collection.count_documents(
            {'date_normalized': {'$gte': last_week_day},
            'categories': 'no'}
        )
        print(f"Se encontraron {num_uncategorized_items} elementos no categorizados.")

        print(f"Buscando {limit} elementos no categorizados en '{collection_name}'...")
        uncategorized_items = collection.find(
            {'date_normalized': {'$gte': last_week_day},
            'categories': 'no'}
        ).limit(limit)

        for item in uncategorized_items:
            try:
                # Filtrar el contenido
                uncategorized_content = category_news(item['title'], item['spanish'])

                # Imprimir contenido original y traducido
                print(f"Contenido original: @{item['title']}:\n{item['spanish']}")
                print(f"Resultado: {uncategorized_content}")

                # Actualizar el elemento con la traducción y marcarlo como traducido
                #category_responses = ['tt', 'pp', 'hm', 'dm', 'nw']

                # Convertir el contenido a minúsculas para la comparación
                if uncategorized_content.lower() == 'nw':
                    print(f"Asignando: {uncategorized_content}")
                    collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'nw', 'filtrada': 'si'}})

                    print(f"Entrando a la categorización tutorial de nivel 2...")
                    uncategorized_content = category_tuto(item['title'], item['spanish'])
                    print(f"Resultado: {uncategorized_content}")
                    if uncategorized_content.lower() == 'tt':
                        print(f"Asignando: {uncategorized_content}")
                        collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'tt', 'filtrada': 'si'}})
                    else:
                        print(f"Entrando a la categorización Papers de nivel 3...")
                        uncategorized_content = category_paper(item['title'], item['spanish'])
                        print(f"Resultado: {uncategorized_content}")
                        if uncategorized_content.lower() == 'pp':
                            print(f"Asignando: {uncategorized_content}")
                            collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'pp', 'filtrada': 'si'}})
                        else:
                            print(f"Entrando a la categorización Herramientas de nivel 4...")
                            uncategorized_content = category_hm(item['title'], item['spanish'])
                            print(f"Resultado: {uncategorized_content}")
                            if uncategorized_content.lower() == 'hm':
                                print(f"Asignando: {uncategorized_content}")
                                collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'hm', 'filtrada': 'si'}})
                            else:
                                print(f"Entrando a la categorización Demos de nivel 5...")
                                uncategorized_content = category_demo(item['title'], item['spanish'])
                                print(f"Resultado: {uncategorized_content}")
                                if uncategorized_content.lower() == 'dm':
                                    print(f"Asignando: {uncategorized_content}")
                                    collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'dm', 'filtrada': 'si'}})
                                else:
                                    if uncategorized_content == 'nn':
                                        uncategorized_content = 'nw'
                                    print(f"Asignando: {uncategorized_content}")
                                    collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'nw', 'filtrada': 'si'}})
                else:
                    if uncategorized_content == 'nn' or uncategorized_content == 'nc':
                        uncategorized_content = 'nc'
                        print(f"Asignando: {uncategorized_content}")
                        collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'nc', 'filtrada': 'no'}})
                    else:
                        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'no', 'filtrada': 'nf'}})
                        print(f"Error al Categorizar o actualizar el elemento {item['_id']}: No se encontró categorización para: {item['_id']}")
                        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"Categorizado completado para: {item['_id']}")
                print(f"-------------------------------------")
                print(f"-------------------------------------")
            except Exception as e:
                print(f"Error al Categorizar o actualizar el elemento {item['_id']}: {e}")

        print(f"Proceso de Categorizar para '{collection_name}' completado.")
    except Exception as e:
        print(f"Error en category_unfiltrated_items para '{collection_name}': {e}")
        raise

def categorized_news_and_tweets():
    try:
        category_unfiltrated_items('news')
        category_unfiltrated_items('tweets')
        print("Categoria de noticias y tweets completada.")
    except Exception as e:
        print("Error al Categorizar noticias y tweets:", e)