from pymongo import MongoClient
from utils.geminifiltrado import filtrated_news

def get_db():
    try:
        client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
        db = client['news_aixteam']
        print("Conexión a la base de datos establecida.")
        return db
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        raise

def filtrar_unfiltrated_items(collection_name, limit=400):
    try:
        db = get_db()
        collection = db[collection_name]

        print(f"Buscando {limit} elementos no filtrados en '{collection_name}'...")
        unfiltrated_items = collection.find({'filtrada': 'no'}).limit(limit)

        for item in unfiltrated_items:
            print(f"Filtrando: {item['_id']}")
            try:
                # Filtrar el contenido
                unfiltrated_content = filtrated_news(item['title'], item['content'])

                # Imprimir contenido original y traducido
                print(f"Contenido original: {item['title']} - {item['content']}")
                print(f"Resultado: {unfiltrated_content}")

                # Actualizar el elemento con la traducción y marcarlo como traducido
                positive_responses = ['si', 'sí', 'yes']

                # Convertir el contenido a minúsculas para la comparación
                if unfiltrated_content.lower() in positive_responses:
                    collection.update_one({'_id': item['_id']}, {'$set': {'filtrada': 'si'}})
                else:
                    collection.update_one({'_id': item['_id']}, {'$set': {'filtrada': 'no'}})

                print(f"Filtro completado para: {item['_id']}")
            except Exception as e:
                print(f"Error al Filtrar o actualizar el elemento {item['_id']}: {e}")

        print(f"Proceso de filtro para '{collection_name}' completado.")
    except Exception as e:
        print(f"Error en filtrar_unfiltrated_items para '{collection_name}': {e}")
        raise

def filtro_news_and_tweets():
    try:
        filtrar_unfiltrated_items('news')
        filtrar_unfiltrated_items('tweets')
        print("Filtro de noticias y tweets completada.")
    except Exception as e:
        print("Error al filtrar noticias y tweets:", e)
