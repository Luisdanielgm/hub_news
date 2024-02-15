from ntscraper import Nitter
import threading
import logging
from pymongo import MongoClient
from utils.utils import convert_to_hours_ago

# Configura la conexión a MongoDB
client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
db = client['news_aixteam']
collection = db['tweets']

# Función para verificar si el tweet ya existe
def tweet_exists(tweet_link):
    return collection.count_documents({'link_url': tweet_link}) > 0

def scrape_tweets_usuario(usuario, scraper, tweets_por_usuario):
    try:
        tweets_raw = scraper.get_tweets(usuario, mode='user', number=15)
        tweets_info = []
        if 'tweets' in tweets_raw:
            for tweet in tweets_raw['tweets']:

                try:
                    tweet_link = tweet.get('link')

                    if not tweet_exists(tweet_link):

                        if tweet['date']:
                            date_result, date_normalized = convert_to_hours_ago(tweet['date'])
                            date_origen = tweet['date']


                        tweet_data = {
                            'type': 'tweet',
                            'title': usuario,
                            'content': tweet['text'],
                            'date': date_result,
                            'date_normalized': date_normalized,
                            'date_origen': date_origen,
                            'fuente': tweet['user']['username'],
                            'read': 'no',
                            'filtrada': 'nf',
                            'traducido': 'no',
                            'spanish': '',
                            'regenerate': 'no',
                            'newregenerate': '',
                            'imgregenerate': '',

                            'avatar': tweet['user']['avatar'],
                            'is-retweet': tweet['is-retweet'],
                            "categories": "nc",
                            "thread": "no"
                            # Añade campos adicionales como imágenes, GIFs, videos
                        }

                        if tweet.get('link'):
                            tweet_data['link_url'] = tweet['link']

                        if tweet.get('pictures'):
                            tweet_data['img_urls'] = tweet['pictures']
                        
                        if tweet.get('videos'):
                            tweet_data['videos'] = tweet['videos']
                        
                        if tweet.get('gifs'):
                            tweet_data['gifs'] = tweet['gifs']

                        tweets_info.append(tweet_data)
                        # Considera insertar el tweet en la base de datos aquí

                        # Insertar el tweet en la base de datos
                        collection.insert_one(tweet_data)

                        print('-- Nueva tweet agregado:')
                        print(tweet_data)
                        print('--------------------------')

                except IndexError as e:
                    print(f"Error de índice en tweet: {tweet}. Error: {e}")
                except Exception as e:
                    print(f"Error procesando tweet: {tweet}")
                    logging.error(f"Error al raspar tweets de {usuario}: {e}")

        tweets_por_usuario[usuario] = tweets_info
    except Exception as e:
        logging.error(f"Error al raspar tweets de {usuario}: {e}")

def obtener_tweets_usuarios():
    # 78 usuarios = 390 tweets
    usuarios = ["DotCSV",
                "TheRundownAI",
                "krea_ai",
                "AiBreakfast",
                "rowancheung",
                "iia_es",
                "theDeepView", 
                "javilop",
                "DeepLearningAI",
                "Analyticsindiam",
                "midudev",
                "luffy_ia",
                "Xiaomi",
                "runwayml",
                "emulenews",
                "joshua_xu_",
                "HeyGen_Official",
                "togethercompute",
                "Neuro_Flash",
                "kaggle",
                "BigTechAlert",
                "DavidSHolz",
                "WriteSonic",
                "NVIDIALA",
                "Grammarly",
                "jackclarkSF",
                "Junia_ai",
                "ChatGPTapp",
                "heyaiwordsmith",
                "LangChainAI",
                "xDaily",
                "Muennighoff",
                "WonderDynamics",
                "seostratega",
                "vercel",
                "pika_labs",
                "HyperWriteAI",
                "El_Lobo_WS",
                "patriciofernanf",
                "HelloCivitai",
                "TUPROFESORIA",
                "Windows",
                "PalmerLuckey",
                "ai_for_success",
                "Donebylaura",
                "OpenAIDevs",
                "playground_ai",
                "lemonfoxai",
                "Tesla_Optimus",
                "sanchitgandhi99",
                "lmsysorg",
                "llama_index",
                "LeiferMendez",
                "isaacconemail",
                "xai",
                "OfficialLoganK",
                "IRLab_UDC",
                "Spain_AI_",
                "getremixai",
                "github",
                "_philschmid",
                "StabilityAI",
                "synthesiaIO",
                "ecomlukaskral",
                "StanfordAILab",
                "GoogleDeepMind",
                "AIatMeta",
                "GoogleAI",
                "googlechrome",
                "Google",
                "LumaLabsAI",
                "barbbowman",
                "nutlope",
                "xavier_mitjana",
                "copyelpadrino",
                "serchaicom",
                "IAViajero",
                "CohesiveAI",
                "SoyTioDaniel",
                "NVIDIAAI",
                "OpenAI",
                "sama",
                "qdrant_engine",
                "midjourney",
                "TheRundownTech",
                "The_CourseAI",
                "neuralink",
                "AndrewYNg",
                "huggingface",
                "_akhaliq",
                "Medivis_AR",
                "LeonardoAi_",
                "mangelroman"]
    scraper = Nitter()
    tweets_por_usuario = {}
    threads = []

    for usuario in usuarios:
        thread = threading.Thread(target=scrape_tweets_usuario, args=(usuario, scraper, tweets_por_usuario))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return tweets_por_usuario