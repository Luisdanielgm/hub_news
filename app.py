from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
from feeds.genbeta.scraping import scrape_genbeta
from feeds.gizmodo.scraping import scrape_gizmodo
from feeds.tweets.scraping import obtener_tweets_usuarios

app = Flask(__name__)
CORS(app)

def parse_date(date_str, formats):
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"No se pudo parsear la fecha: {date_str}")

@app.route('/', methods=['GET'])
def get_all_news():

    genbeta_data = scrape_genbeta()
    gizmodo_data = scrape_gizmodo()
    combined_data = genbeta_data + gizmodo_data

    date_formats = ['%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%SZ']
    combined_data.sort(key=lambda x: parse_date(x['date_origen'], date_formats), reverse=True)

    return jsonify(combined_data)

@app.route('/genbeta', methods=['GET'])
def get_genbeta_news():
    scraped_data = scrape_genbeta()
    return jsonify({'data': scraped_data})

@app.route('/gizmodo', methods=['GET'])
def get_gizmodo_news():
    scraped_data = scrape_gizmodo()
    return jsonify({'data': scraped_data})

@app.route('/tweets', methods=['GET'])
def obtener_tweets():
    tweets_por_usuario = obtener_tweets_usuarios()
    return jsonify(tweets_por_usuario)

# Ejecuta la aplicación si se ejecuta este script
if __name__ == '__main__':
    app.run(debug=True)