import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def group_news(content1, content2):
    try:
        # Configuración del modelo
        generation_config = {
          "temperature": 0,
          "top_p": 1,
          "top_k": 1,
          "max_output_tokens": 2,
        }

        safety_settings = [
          {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings)

        prompt_parts = [
            'Te presento dos noticias, tu objetivo es determinar si son la misma noticia, debido a que hay noticias redactadas por diferentes fuentes pero son la misma, entonces debes determinar sin son misma noticia o no, responde "si" o "no".\n',
            f"""Noticia 1: {content1}\n""",
            f"""Noticia 2: {content2}\n""",
            'respuesta: ',
        ]

        response = model.generate_content(prompt_parts)
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error en la generación de category_new: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None