import time
from feeds.genbeta.scraping import run_scraping as scrape_genbeta
from feeds.gizmodo.scraping import run_scraping as scrape_gizmodo
from feeds.xataka.scraping import run_scraping as scrape_xataka
from feeds.hipertextual.scraping import run_scraping as scrape_hipertextual
from feeds.tweets.scraping import obtener_tweets_usuarios
from utils.traductfeeds import translate_news_and_tweets
from utils.filtradonews import filtro_news_and_tweets

# Intervalos de tiempo en segundos
INTERVALO_SCRAPING = 15 * 60  # 15 minutos para el scraping
INTERVALO_ESPERA_TRADUCCION = 5 * 60  # 5 minutos de espera para la traducción después del scraping

ultimo_scraping = time.time() - INTERVALO_SCRAPING  # Inicia inmediatamente
ultima_traduccion = time.time()

while True:
    tiempo_actual = time.time()

    # Verificar si ha pasado el intervalo de scraping
    if tiempo_actual - ultimo_scraping >= INTERVALO_SCRAPING:
        try:
            scrape_genbeta()
            scrape_gizmodo()
            scrape_xataka()
            scrape_hipertextual()
            obtener_tweets_usuarios()
            # Código para guardar los resultados en la base de datos
            ultimo_scraping = tiempo_actual
            ultima_traduccion = tiempo_actual + INTERVALO_ESPERA_TRADUCCION  # Establece el momento para la próxima traducción
        except Exception as e:
            print(f"Error durante el scraping: {e}")

    # Verificar si ha pasado el tiempo de espera para la traducción
    if tiempo_actual >= ultima_traduccion:
        try:
            translate_news_and_tweets()
            filtro_news_and_tweets()
        except Exception as e:
            print(f"Error durante la traducción y filtrado: {e}")
        ultima_traduccion = tiempo_actual + INTERVALO_SCRAPING + INTERVALO_ESPERA_TRADUCCION  # Establece el próximo intervalo para la traducción

    # Esperar un poco antes de la siguiente iteración
    time.sleep(60)