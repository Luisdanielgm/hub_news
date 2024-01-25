import google.generativeai as genai

genai.configure(api_key="AIzaSyBqSz1l0faFq9GwGO6er8qLYxgPpYHeRwg")

def regenerate_prompt_img(titulo, content):
    try:
        # Configuración del modelo
        generation_config = {
          "temperature": 0.9,
          "top_p": 1,
          "top_k": 1,
          "max_output_tokens": 2046,
        }

        safety_settings = [
          {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        model = genai.GenerativeModel(model_name="gemini-pro",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        prompt_parts = [
            'Genera un prompt para generar una imagen que visualice de manera vívida y atractiva la esencia de una noticia reestructurada.',
            'La imagen debe capturar los siguientes elementos clave de la noticia: como el tema central, personajes importantes, ubicación, eventos específicos o cualquier detalle distintivo.',
            'La composición debe ser equilibrada y estéticamente agradable, con colores y texturas que reflejen el tono de la noticia (por ejemplo, colores brillantes para una noticia positiva o tonos más oscuros para una temática seria).',
            'Asegúrate de que la imagen sea dinámica y capte la atención, ilustrando claramente el mensaje principal de la noticia y su impacto. El estilo debe ser realista/fantástico/artístico (según corresponda) y debe transmitir la atmósfera y la emoción de la historia contada en la noticia. ',
            'Si el texto por elgun motivo nombra a una personalidad que no deba ser nombrada o quizás infranja las politicas de gemini, entonces cambia solo esa parte por una persona ramdon. ',
            f'Noticia: {content}',
            'respuesta: ',
            ""
        ]

        response = model.generate_content(prompt_parts)
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error del prompt para la imagen de la nueva noticia: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None