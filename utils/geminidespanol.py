import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def generate_detecta_espanol(content, title):
    try:
        # Configuración del modelo
        generation_config = {
          "temperature": 0.9,
          "top_p": 1,
          "top_k": 1,
          "max_output_tokens": 50,
        }

        safety_settings = [
          {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
          {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(model_name="gemini-pro")

        prompt_parts = [
            'Que idioma es este, solo responde "español" o "ingles": '
            f'{title}',
            f'{content}',
            ""
        ]

        response = model.generate_content(prompt_parts)
        print('Idioma español: ')
        print(response.text)
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error en la detecctión del idioma: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None