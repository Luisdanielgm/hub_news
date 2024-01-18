import time
from ntscraper import Nitter
from pprint import pprint

def main():
    scraper = Nitter()

    # Obtener tweets de un usuario
    tweets = scraper.get_tweets("GM_LuisDaniel", mode='user', number=5)
    print("Tweets del usuario:")
    pprint(tweets)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(600)  # Espera 10 minutos (600 segundos) antes de la próxima ejecución