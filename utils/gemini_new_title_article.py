import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def new_title_article(title_full):
    try:
        # Configuración del modelo
        generation_config = {
          "temperature": 0.5,
          "top_p": 1,
          "top_k": 1,
          "max_output_tokens": 2048,
        }

        safety_settings = [
          {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config, safety_settings=safety_settings)

        prompt_parts = [
            """Necesito que me ayudes a redactar un nuevo titulo para un articulo, te pasaré el titulo original, solo deberas parafrasearlo e incluso cambiando el orden de las ideas pero manteniendo la fidelidad de las noticias, recuerda que debe ser 100 por ciento fiel a la noticia.
                Por Favor el titulo debe ser muy llamativo, conciso y llamar al usuario a leerlo,
                Utiliza un lenguaje claro y conciso.
                Optimiza el titulo para SEO de manera natural y estratégica.
                Asegúrate de que el titulo sea original y no infrinja derechos de autor, además devuelve solo texto, nada de * o simbolos para dar formato, solo texto sin formato. 
                Teniendo en cuenta estos puntos, procede a desarrollar el titulo, ahora te mostraré el titulo original:\n""",
            f"""{title_full}\n""",
            'nuevo titulo:\n',
        ]

        response = model.generate_content(prompt_parts)
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error en la generación de new_article: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None