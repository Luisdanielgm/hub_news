from ntscraper import Nitter


def obtener_tweets_usuarios():
    usuarios = ["GM_LuisDaniel", "DotCSV", "huggingface", "TheRundownAI", "krea_ai", 'dhernandezlarez']
    scraper = Nitter()
    tweets_por_usuario = {}

    for usuario in usuarios:
        tweets_raw = scraper.get_tweets(usuario, mode='user', number=5)
        tweets_info = []
        if 'tweets' in tweets_raw:
            for tweet in tweets_raw['tweets']:
                tweet_data = {
                    'usuario': tweet['user']['username'],
                    'texto': tweet['text'],
                    'fecha': tweet['date']
                }
                # Añadir imagen si está disponible
                if 'pictures' in tweet and tweet['pictures']:
                    tweet_data['imagen'] = tweet['pictures'][0]  # La primera imagen

                # Añadir GIFs si están disponibles
                if 'gifs' in tweet and tweet['gifs']:
                    tweet_data['gifs'] = tweet['gifs']  # Lista de GIFs

                # Añadir videos si están disponibles
                if 'videos' in tweet and tweet['videos']:
                    tweet_data['videos'] = tweet['videos']  # Lista de URLs de videos

                tweets_info.append(tweet_data)
        tweets_por_usuario[usuario] = tweets_info

    return tweets_por_usuario
