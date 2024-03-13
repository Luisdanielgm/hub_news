from pymongo import MongoClient
#from utils.gemini_group_similar import group_news

def get_db():
    try:
        client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
        db = client['news_aixteam']
        print("Conexión a la base de datos establecida.")
        return db
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        raise

def start_group_similar_items(collection_name, limit=10):
    try:
        db = get_db()
        collection = db[collection_name]

        print(f"Buscando {limit} elementos no agrupados en '{collection_name}'...")
        ungrouped_items = collection.find({'similar_group': 'no'}).limit(limit)

        batch = []  # Lista para almacenar lotes de noticias a procesar

        for item in ungrouped_items:
            print(f"Agregando a lote: {item['_id']}")
            batch.append(item)

        # Procesar lotes de 10 noticias
        for i in range(0, len(batch), 10):
            batch_to_process = batch[i:i+10]
            processed_group = process_and_save_group(batch_to_process)

            print(f"Agrupación de noticias procesadas: {processed_group}")

        print(f"Proceso de agrupación para '{collection_name}' completado.")
    except Exception as e:
        print(f"Error en start_group_similar_items para '{collection_name}': {e}")
        raise


def process_and_save_group(batch_to_process):
    try:
        # Aquí procesas el lote de noticias y las agrupas
        # Luego las guardas en la base de datos y obtienes el nuevo id de grupo
        # Esta parte del código es un pseudo-código que debes ajustar según tu lógica real

        # Supongamos que procesas y agrupas las noticias en la variable grouped_news
        grouped_news = {'idgrupo': ['id12345678', 'id123456438', 'id1237248', 'id45545678']}

        # Guardar las noticias agrupadas en la base de datos y obtener el nuevo id de grupo
        new_group_id = save_grouped_news(grouped_news)

        return new_group_id
    except Exception as e:
        print(f"Error al procesar y guardar grupo de noticias: {e}")
        raise

def save_grouped_news(grouped_news):
    try:
        # Aquí guardas las noticias agrupadas en la base de datos
        # y devuelves el nuevo id de grupo
        # Esta parte del código es un pseudo-código que debes ajustar según tu lógica real

        # Supongamos que guardas las noticias agrupadas en la base de datos y obtienes el nuevo id de grupo
        new_group_id = 'nuevo_id_grupo'

        return new_group_id
    except Exception as e:
        print(f"Error al guardar grupo de noticias en la base de datos: {e}")
        raise

def group_similar_news():
    try:
        start_group_similar_items('news')
        print("Agrupación de noticias similares completada.")
    except Exception as e:
        print("Error al agrupar noticias similares:", e)