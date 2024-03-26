import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def new_article(extracted_text):
    try:
        # Configuración del modelo
        generation_config = {
          "temperature": 0.5,
          "top_p": 1,
          "top_k": 1,
          "max_output_tokens": 10048,
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
            """Necesito que me ayudes a diseñar un artículo en español de 2000 palabras. Por favor, estructura el contenido con etiquetas html empezando si o si por <article>, 1 <p>, 1 título H2, varios títulos H3, si tienes los datos un <blockquote class='wp-block-quote'> con un texto <p> y un pequeño titulo <cite>.  y 1 títulos H4, no usarás imagenes, para potenciar la visibilidad en los resultados de búsqueda de Google. A continuación, muéstrame el articulo con las respectivas etiquetas.
                Por favor, redacta contenido interesante y valioso para cada título del articulo que acabas de desarrollar, escribiendo párrafos de 300 palabras sin exceder las 5 líneas por párrafo. No escribas una conclucion ni reflexion, no escribas un resumen.

                Asegúrate de que el contenido mantenga el interés del lector, aporte información útil y relevante, y realmente beneficie al lector. Ten en cuenta las siguientes características al desarrollar el contenido:
                Utiliza un lenguaje claro y conciso.
                Incorpora ejemplos y casos prácticos para ilustrar los puntos clave si es necesario.
                Estructura el contenido con subtítulos y listas para facilitar la lectura.
                Optimiza el contenido para SEO de manera natural y estratégica.
                Asegúrate de que el contenido sea original y no infrinja derechos de autor, además en el formato evita iniciar con otra etiqueta html o algpun comentario o indicativos, deberas responder unica y excluviamente comenzando con <article> y terminar la respuesta con </article>.
                Teniendo en cuenta estos puntos, procede a desarrollar el contenido con este tema principal\n""",
            f"{extracted_text}\n",
            "respuesta:\n",
        ]

        response = model.generate_content(prompt_parts)
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error en la generación de new_article: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None