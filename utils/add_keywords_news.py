from pymongo import MongoClient
import re
from utils.gemini_general_keys_words import new_general_keys_words
from datetime import datetime, timedelta, timezone

def tokenize(text):
    # Utiliza expresiones regulares para dividir el texto en palabras
    tokens = re.findall(r'\b\w+\b', text.lower())

    stopwords = set(['entre', 'tras', 'los', 'mías', 'lo', 'vuestros', 'vía', 'para', 'mío', 'nuestra', 'nuestros', 'nuestras', 'versus', 'la', 'bajo', 'en', 'tuyos', 'ante', 'sobre', 'suyo', 'desde', 'tuya', 'vuestra', 'hasta', 'nuestro', 'tu', 'esta', 'su', 'esos', 'aquella', 'vuestro', 'sus', 'durante', 'esas', 'del', 'un', 'mi', 'al', 'aquellos', 'aquel', 'mía', 'míos', 'suya', 'tuyas', 'ese', 'por', 'mediante', 'vuestras', 'unas', 'hacia', 'este', 'estos', 'unos', 'una', 'a', 'sin', 'esa', 'estas', 'suyas', 'de', 'tuyo', 'aquellas', 'las', 'con', 'suyos', 'según', 'ya', 'está', 'más', 'y', 'el', 'me', 'posibles', 'usa', 'se', 'trata', 'algunas', 'como', 'harán', 'solo', 'que', 'gracias', 'hacer', 'esto', 'si', 'puedes', 'cómo', 'hemos', 'ahora', 'le', 'será', 'es', 'ellas', 'además', 'ha', 'e', 'mismo', 'nosotros'])
    return [word for word in tokens if word not in stopwords]

def lemmatize(word):
    # Implementa tu propio método para lematizar la palabra
    # Por simplicidad, aquí simplemente devolvemos la palabra sin cambios
    return word

def extract_keywords(text):
    # Tokenización
    keywords = tokenize(text.lower())
    #lemmatized_tokens = [lemmatize(token) for token in tokens]
    # Lematización y eliminación de stopwords
    return keywords

def get_db():
    try:
        client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
        db = client['news_aixteam']
        print("Conexión a la base de datos establecida.")
        return db
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        raise

def added_keywords_news_item(collection_name):
    try:
        db = get_db()
        collection = db[collection_name]

        now = datetime.now()
        last_week = now - timedelta(days=7)
        last_week_day = last_week.strftime('%Y-%m-%d') 

        print(f"Buscando elementos sin palabras claves en '{collection_name}'...")
        news_items = collection.find({
            'date_normalized': {'$gte': last_week_day},
            'filtrada': 'si',
            'added_keywords': 'no',
        })

        num_news_items = collection.count_documents({
            'date_normalized': {'$gte': last_week_day},
            'filtrada': 'si',
            'added_keywords': 'no',
        })
        print(f"Se encontraron {num_news_items} elementos sin palabras claves.")

        for item in news_items:
            print(f"Obteniendo palabras claves para: {item['_id']}")
            try:
                all_content = ''
                if item['type'] == 'tweet':
                    all_content = item['spanish']
                else:
                    if item['fuente'] == 'Therundown':
                        all_content = item['spanish']
                    else:
                        all_content = item['title'] + ' ' + item['content']

                # Extraer palabras claves
                keywords = extract_keywords(all_content)

                # convertir las palabras claves en una cadena separada por comas
                keywords_str = ', '.join(keywords)
                # enviar las palabras claves a ser analizadas por un llm para que escoga maximo las 10 palabras claves mas relevantes
                keywords_llm = new_general_keys_words(keywords_str)

                # Convertir las primeras 15 primeras palabras clave en una lista separada por comas y también solo espacios sin comas
                keywords_list = keywords_llm.split(', ')[0:15]
                
                # Actualizar el elemento con las palabras claves
                collection.update_one({'_id': item['_id']}, {'$set': {'keywords': keywords_list, 'added_keywords': 'si'}})

                # Imprimir contenido con palabras claves
                print(f"Contenido original: {all_content}")
                print(f"Resultado keywords del llm: {keywords_list}")


                print(f"Palabras claves obtenidas con exito para: {item['_id']}")
            except Exception as e:
                print(f"Error al extraer o agregar las palabras claves del elemento {item['_id']}: {e}")

        print(f"Proceso de extrección de palabras claves para '{collection_name}' completado.")
    except Exception as e:
        print(f"Error en added_keywords_news_item para '{collection_name}': {e}")
        raise

def add_keywords_news_and_tweets():
    try:
        added_keywords_news_item('news')
        added_keywords_news_item('tweets')
        print("Extración de palabras clave de noticias y tweets completada.")
    except Exception as e:
        print("Error al extraer o agregar las palabras claves de noticias y tweets:", e)
