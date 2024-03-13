from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import time
import pandas as pd
import os
import json
from utils.utils import convert_to_hours_ago

client = MongoClient('mongodb+srv://luisdanielgm19:gksq4WQwlQJh5nus@cluster0.pgqscfq.mongodb.net/?retryWrites=true&w=majority')
db = client['news_aixteam']
collection = db['tweets']

# Función para verificar si el tweet ya existe
def tweet_exists(tweet_link):
    return collection.count_documents({'link_url': tweet_link}) > 0

def obtener_tweets(users):
    driver = None
    tweets_data = []

    def iniciar_sesion():
        nonlocal driver
        print(f"Iniciando sesión de @AIPedia_tools")
        username_field = driver.find_element("xpath", "//input[@name='text']")
        username_field.send_keys("@AIPedia_tools")
        #username_field.send_keys("@aiteamdigital")

        next_button = driver.find_element("xpath", '//div[@role="button"]//span[text()="Siguiente"]')
        next_button.click()
        time.sleep(3)

        password_field = driver.find_element("xpath", "//input[@name='password']")
        password_field.send_keys("taipedia2023.")
        #password_field.send_keys("Aiteam321.")

        login_button = driver.find_element("xpath", '//div[@role="button"]//span[text()="Iniciar sesión"]')
        login_button.click()
        print(f"Sesión iniciada @AIPedia_tools")
        guardar_cookies()
        time.sleep(3)


    def cargar_cookies_y_abrir_sesion():
        nonlocal driver
        try:
            # Cargar cookies desde el archivo
            with open("cookies.json", "r") as f:
                cookies = json.load(f)
            # Abrir el navegador y cargar las cookies
            #options = webdriver.ChromeOptions()
            #options.add_argument("--headless")
            driver = webdriver.Chrome()
            driver.get("https://twitter.com") 
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.get("https://twitter.com") 
            driver.refresh()
            guardar_cookies()
        except Exception as e:
            print("Error al cargar cookies:", e)
            driver.get("https://twitter.com/i/flow/login")
            time.sleep(7)
            print('Cargando Pagina Login...')
            iniciar_sesion()
            

    def guardar_cookies():
        nonlocal driver
        try:
            cookies = driver.get_cookies()
            #with open("cookies.json", "w") as f:
                #json.dump(cookies, f)
            pass
        except Exception as e:
            print("Error al guardar cookies:", e)

    def esperar_elementos_presentes(selector, tiempo_espera=30):
        nonlocal driver
        return WebDriverWait(driver, tiempo_espera).until(EC.presence_of_all_elements_located((By.XPATH, selector)))

    def obtener_tweets_usuario(user):
        nonlocal driver
        user_tweets = []
        tweet_ids = set()
        tweet_count = 0
        repeated_tweet_count = 0
        max_repeated_tweets = 15

        web = f"https://twitter.com/{user}"
        print(f"Obteniendo tweets de {user}")
        driver.get(web)
        time.sleep(5)

        # Altura de la ventana
        window_height = driver.execute_script("return window.innerHeight;")
        print(f"Altura de la ventana: {window_height}")
        # Desplazamiento parcial (3/4 del tamaño de la ventana)
        scroll_height = window_height * 0.65
        print(f"Desplazamiento parcial: {scroll_height}")

        # Desplazamiento lento y guardado de tweets
        while True:
            try:
                # Espera para cargar los elementos
                time.sleep(0.1)
                tweets = esperar_elementos_presentes("//article")

                # Procesar los tweets
                for tweet in tweets:

                    link_element_tweet = tweet.find_element(By.XPATH, ".//a[contains(@class, 'css-1rynq56')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-37j5jr')][contains(@class, 'r-a023e6')][contains(@class, 'r-rjixqe')][contains(@class, 'r-16dba41')][contains(@class, 'r-xoduu5')][contains(@class, 'r-1q142lx')][contains(@class, 'r-1w6e6rj')][contains(@class, 'r-9aw3ui')][contains(@class, 'r-3s2u2q')][contains(@class, 'r-1loqt21')]")
                    url_tweet = link_element_tweet.get_attribute('href')

                    if not tweet_exists(url_tweet):
                        tweet_data = get_tweet(tweet, user)
                        collection.insert_one(tweet_data)
                        print('-- Nueva tweet agregado:', tweet_count)
                        print(tweet_data)
                        print('--------------------------')
                        tweet_count += 1
                    
                    else:
                        repeated_tweet_count += 1

                    # Detener si ya se han guardado 15 tweets únicos o si se repiten 5 tweets
                    if tweet_count >= 15 or repeated_tweet_count >= max_repeated_tweets:
                        if tweet_count >= 15:
                            print(f"Se han guardado {tweet_count} tweets. Se detiene la ejecución.")
                        else:
                            print(f"Se han detectado {repeated_tweet_count} tweets repetidos. Se detiene la ejecución.")
                        break

                # Desplazamiento suave
                driver.execute_script(f"window.scrollBy(0, {scroll_height});")
                time.sleep(0.1)  # Espera corta para un desplazamiento suave

            except Exception as e:
                print(f"Error al obtener tweets: {e}")
                break

        return user_tweets


    def get_tweet(element, user):
        try:
            typeTweet = "post"
            traducido = 'no'
            spanish = ''
            # Obtener el usuario y el texto del tweet original
            user_element = element.find_element(By.XPATH, ".//*[contains(text(), '@')]")
            tweet_user = user_element.text.lstrip('@')
            if tweet_user.lower() != user.lower():
                typeTweet = "retweet"
            text_element = element.find_element(By.XPATH, ".//div[@lang]")
            text = text_element.text
            lang = text_element.get_attribute("lang")
            if lang == 'es':
                traducido = 'na'
                spanish = text

            avatar_elements = element.find_elements(By.XPATH, ".//*[contains(@data-testid, 'Tweet-User-Avatar')]")
            avatar_url = None  # Inicializa avatar_url como None por defecto

            for avatar_element in avatar_elements:
                try:
                    a_element = avatar_element.find_element(By.XPATH, ".//a")
                    img_element = a_element.find_element(By.XPATH, ".//img[@class='css-9pa8cd']")
                    avatar_url = img_element.get_attribute("src")
                    break
                except NoSuchElementException as e:
                    print("No se encontró la etiqueta 'a' dentro del elemento del avatar.")
                    print("Excepción:", e)
                    continue

             # Buscar todos los elementos con el atributo data-testid="tweetPhoto" para obtener las fotos
            all_photo_divs = element.find_elements(By.XPATH, ".//div[@data-testid='tweetPhoto']")
            photo_urls = [photo_div.find_element(By.TAG_NAME, "img").get_attribute("src") for photo_div in all_photo_divs]

            quote_content = {}
            

            # Buscar el contenido de la cita si está presente
            quote_content_div = None
            try:
                quote_content_div = element.find_element(By.XPATH, ".//div[contains(@class, 'css-175oi2r')][contains(@class, 'r-adacv')][contains(@class, 'r-1udh08x')][contains(@class, 'r-1kqtdi0')][contains(@class, 'r-1867qdf')][contains(@class, 'r-rs99b7')][contains(@class, 'r-o7ynqc')][contains(@class, 'r-6416eg')][contains(@class, 'r-1ny4l3l')][contains(@class, 'r-1loqt21')]")
            except NoSuchElementException:
                pass

            if quote_content_div:
                if tweet_user.lower() != user.lower():
                    typeTweet = "retweet_quote"
                else:
                    typeTweet = "quote"

                quote_text = ""
                quote_lang = ""

                quote_user_element = quote_content_div.find_element(By.XPATH, ".//*[contains(text(), '@')]")
                quote_user = quote_user_element.text.lstrip('@')
                
                try:
                    quote_text_element = quote_content_div.find_element(By.XPATH, ".//div[@lang]")
                    quote_text = quote_text_element.text
                    quote_lang = quote_text_element.get_attribute("lang")
                except NoSuchElementException:
                    print("No se encontró ningún elemento de texto para la cita.")

                # Buscar las fotos dentro del elemento de cita (quote)
                quote_photo_divs = quote_content_div.find_elements(By.XPATH, ".//div[@data-testid='tweetPhoto']")
                quote_photo_urls = [photo_div.find_element(By.TAG_NAME, "img").get_attribute("src") for photo_div in quote_photo_divs]

                for quote_photo_url in quote_photo_urls:
                    if quote_photo_url in photo_urls:
                        photo_urls.remove(quote_photo_url)

                quote_content = {
                    'quote_user': quote_user,
                    'quote_text': quote_text,
                    'quote_lang': quote_lang,
                    'quote_img_urls': quote_photo_urls
                }

            # Buscar la etiqueta <a> que contiene el enlace y el tiempo
            link_element = element.find_element(By.XPATH, ".//a[contains(@class, 'css-1rynq56')][contains(@class, 'r-bcqeeo')][contains(@class, 'r-qvutc0')][contains(@class, 'r-37j5jr')][contains(@class, 'r-a023e6')][contains(@class, 'r-rjixqe')][contains(@class, 'r-16dba41')][contains(@class, 'r-xoduu5')][contains(@class, 'r-1q142lx')][contains(@class, 'r-1w6e6rj')][contains(@class, 'r-9aw3ui')][contains(@class, 'r-3s2u2q')][contains(@class, 'r-1loqt21')]")
            url = link_element.get_attribute('href')
            date_element = link_element.find_element(By.TAG_NAME, 'time')
            date = date_element.get_attribute('datetime')

            if date:
                date_result, date_normalized = convert_to_hours_ago(date)

            tweet_data = {
                'type': 'tweet',
                'typeTweet': typeTweet,
                'title': user,
                'content': text,
                'date': date_result,
                'date_normalized': date_normalized,
                'date_origen': date,
                'fuente': tweet_user,
                'read': 'no',
                'filtrada': 'nf',
                "lang": lang,
                'traducido': traducido,
                'spanish': spanish,
                'regenerate': 'no',
                'newregenerate': '',
                'imgregenerate': '',
                'avatar': avatar_url,
                "categories": "nc",
                "thread": "no",
                'link_url': url,
                'img_urls': photo_urls,
                'quote_content': quote_content
            }

            return tweet_data
        except NoSuchElementException as e:
            print(f"Error al obtener tweet: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al obtener tweet: {e}")
            return None

    # Configuración del WebDriver
    web = 'https://twitter.com'
    path = '/Users/LENOVO/Desktop/chrome-win64'
    driver = webdriver.Chrome()
    driver.get(web)
    print('Cargando Pagina Principal...')
    driver.maximize_window()
    time.sleep(6)

    # Comprueba si hay cookies guardadas y abre la sesión, o inicia sesión si no hay cookies guardadas
    cargar_cookies_y_abrir_sesion()

    # Iterar sobre la lista de usuarios
    for user in users:
        user_tweets = obtener_tweets_usuario(user)
        tweets_data.extend(user_tweets)

    driver.quit()