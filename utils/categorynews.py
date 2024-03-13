from pymongo import MongoClient
from utils.geminicategory import category_news

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

        print(f"Buscando {limit} elementos no categorizados en '{collection_name}'...")
        uncategorized_items = collection.find({'categories': 'nc', 'filtrada': 'si'}).limit(limit)

        for item in uncategorized_items:
            print(f"Categorizando: {item['_id']}")
            try:
                # Filtrar el contenido
                uncategorized_content = category_news(item['title'], item['content'])

                # Imprimir contenido original y traducido
                print(f"Contenido original: {item['title']} - {item['content']}")
                print(f"Resultado: {uncategorized_content}")

                # Actualizar el elemento con la traducción y marcarlo como traducido
                #category_responses = ['tt', 'pp', 'hm', 'dm', 'nw']

                # Convertir el contenido a minúsculas para la comparación
                if uncategorized_content.lower() == 'nw':
                    print(f"Asignando: {uncategorized_content}")
                    collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'nw'}})
                else:
                    if uncategorized_content.lower() == 'tt':
                        print(f"Asignando: {uncategorized_content}")
                        collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'tt'}})
                    else:
                        if uncategorized_content.lower() == 'pp':
                            print(f"Asignando: {uncategorized_content}")
                            collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'pp'}})
                        else:
                            if uncategorized_content.lower() == 'hm':
                                print(f"Asignando: {uncategorized_content}")
                                collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'hm'}})
                            else:
                                if uncategorized_content.lower() == 'dm':
                                    print(f"Asignando: {uncategorized_content}")
                                    collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'dm'}})
                                else:
                                    collection.update_one({'_id': item['_id']}, {'$set': {'categories': 'nc'}})

                print(f"Categorizado completado para: {item['_id']}")
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