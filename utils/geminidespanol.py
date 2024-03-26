import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def generate_detecta_espanol(content):
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
            """Responde "si" en caso de que la noticia esté en español\n""",
            """Te daré algunos ejemplos de como responder:\n""",
            """Texto de ejemplo de "Modificar región" de la IA https://pika.art. Respuesta: si\n""",
            """Want to create your own Image-to-3D tools? Check out Gradio. Respuesta: no\n""",
            """Sumerge en la innovadora CLI de Francesco para RAG con YouTube, creada por Qdrant y Ollama. No necesitas frameworks: ¡echa un vistazo al código y ve cómo funciona de primera mano!. Respuesta: si\n""",
            """Ten en cuenta que el resultado puede cambiar a medida que entren más votos. ¡Contribuye a la clasificación tú mismo en http://chat.lmsys.org!. Respuesta: si\n""",
            """Samsung first launched the S24 with Galaxy AI, powered by Googles Gemini.Now, Apple is in talks to allow Googles Gemini to power iPhones generative AI features. Why is no one choosing OpenAI?. Respuesta: no\n""",
            """Quiero GPT-5. Respuesta: si\n""",
            f"""Texto: {content}\n""",
            """Respuesta: """,
        ]

        response = model.generate_content(prompt_parts)
        print(f'Idioma español: {response.text}')
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error en la detecctión del idioma: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None