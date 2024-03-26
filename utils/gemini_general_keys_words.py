import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def new_general_keys_words(keywords):
    try:
        # Configuración del modelo
        generation_config = {
          "temperature": 0.9,
          "top_p": 1,
          "top_k": 1,
          "max_output_tokens": 2048,
        }

        safety_settings = [
          {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings)

        prompt_parts = [
            'Te daré una lista de palabras claves debes seleccionar máximo las 10 palabras claves más relevantes y devolverlas en una lista separada por comas, esta lista debe inicia por las más relevantes primero.\n',
            f"""{keywords}\n""",
            'respuesta:\n',
        ]

        response = model.generate_content(prompt_parts)
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error en la generación de new_relfection: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None