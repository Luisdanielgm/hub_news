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

def change_fields():
    try:
        db = get_db()
        collection = db.news
        now = datetime.now()

        # obtenemos el numero del día de la semana actual en formato datetime
        last_week = now - timedelta(days=1)
        last_week_day = last_week.strftime('%Y-%m-%d')
        print(f"El dia de la semana hace una semana era: {last_week_day}")

        # cambiar el campo categories de tweets en el rango de fechas especificado
        collection_count = collection.count_documents({'date_normalized': {'$gte': '2024-03-17', '$lte': '2024-03-20'}})  # Count the number of documents in the collection.
        print(f"Se encontraron {collection_count} tweets en el rango de fechas especificado.")

        #collection.update_many(
        #    {'date_normalized': {'$gte': last_week_day, '$lte': '2024-03-18'}},
        #    {'$set': {'categories': 'no', 'filtrada': 'nf'}}
        #)

        #print("Cambiado el campo categories de tweets en el rango de fechas especificado.")

    except Exception as e:
        print(f"Error en cambiar el campo para tweets: {e}")
        raise


change_fields()
