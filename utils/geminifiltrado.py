import google.generativeai as genai

genai.configure(api_key="AIzaSyBqSz1l0faFq9GwGO6er8qLYxgPpYHeRwg")

def filtrated_news(title, content):
    try:
        # Configuración del modelo
        generation_config = {
          "temperature": 0.9,
          "top_p": 1,
          "top_k": 1,
          "max_output_tokens": 2048,
        }

        safety_settings = [
          {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
          {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        model = genai.GenerativeModel(model_name="gemini-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        prompt_parts = [
            'Tu tarea solo consiste en clasificar una noticia, tu deber es clasificar si una noticia sera util o no, estamos buscando noticias relacionadas con inteligencia artificial, pero noticias que sean nuevos inventos, nuevos descubrimientos, alguna nueva herramientas, algun nuevo producto, tu deber es solo ver la noticia y deberas responder unica y estrictamente "SI" o "NO", ahora te presento la noticia: ',
            f'titulo: {title}',
            f'contenido: {content}',
            'respuesta: ',
            ""
        ]

        response = model.generate_content(prompt_parts)
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error en la generación de filtrated_new: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None