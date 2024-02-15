import requests
import json
import os

# Replace with your OpenAI API key
OPENAI_API_KEY = os.getenv('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')

# Define the API endpoint and request payload
api_url = 'https://api.openai.com/v1/images/generations'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer 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'
}
data = {
    "model": "dall-e-3",
    "prompt": "Genera un logotipo simple y elegante que represente la silueta de Un caballo de ajedrez formado por circuitos cubos texto 'AITeam' utilizando un enfoque minimalista con líneas limpias",
    "n": 1,
    "size": "1024x1024"
}

# Make the API request
response = requests.post(api_url, headers=headers, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    print("Generated image URL:", result['data'][0]['url'])
else:
    print("Error:", response.status_code, response.text)