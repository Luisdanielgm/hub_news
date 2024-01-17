from flask import Flask, jsonify
from flask_cors import CORS
from feeds.genbeta.scraping import scrape_genbeta

app = Flask(__name__)
CORS(app)



@app.route('/', methods=['GET'])
def get_all_news():
    scraped_data = scrape_genbeta()
    return jsonify({'data': scraped_data})


@app.route('/genbeta', methods=['GET'])
def get_genbeta_news():
    scraped_data = scrape_genbeta()
    return jsonify({'data': scraped_data})


# Ejecuta la aplicación si se ejecuta este script
if __name__ == '__main__':
    app.run(debug=True)