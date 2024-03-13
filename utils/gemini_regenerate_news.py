import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def regenerate_news(titulo, content):
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

        model = genai.GenerativeModel(model_name="gemini-pro")

        prompt_parts = [
            'Te proporcionaré una o varias noticias e informaciones, y tu misión será reformar o reestructurar estas noticias. Para lograrlo de manera efectiva y precisa, sigue las siguientes instrucciones paso a paso:',
            'Leer y Comprender las Noticias Originales: Inicia leyendo atentamente cada noticia seleccionada. Asegúrate de entender completamente el contenido, contexto y detalles clave.',
            'Identificar Elementos Clave: Subraya o anota todas las palabras clave, frases importantes y datos cruciales que son esenciales para entender el mensaje principal de las noticias.',
            'Parafrasear Creativamente: Transforma las palabras y frases clave identificadas usando sinónimos y reestructurando las oraciones. Mantén el significado original, pero exprésalo de manera diferente.',
            'Reestructurar y Sintetizar: Reorganiza las ideas parafraseadas en un nuevo orden lógico y coherente para formar la nueva noticia. Redacta un título impactante y pertinente. Asegúrate de que la noticia tenga entre 40 y 60 palabras.',
            'Revisar y Corregir: Verifica que la nueva noticia refleje fielmente el contenido y mensaje de las noticias originales. Comprueba la exactitud de los hechos y corrige cualquier error gramatical o de coherencia.',
            f'Noticia original: {titulo} - {content}',
            'Nueva noticia: ',
            ""
        ]

        response = model.generate_content(prompt_parts)
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error en la generación de la nueva noticia: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None