import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def filtrated_news(title, content):
    try:
        # Configuración del modelo
        generation_config = {
          "temperature": 0.9,
          "top_p": 1,
          "top_k": 1,
          "max_output_tokens": 2,
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
            'Tu tarea solo consiste en clasificar noticias, las noticias que clasificaras seran solo de nuevas herramientas, productos o actualizaciones de productos o herramientas de inteligencia artificial, estas noticias tambien podras reconocerlas debido a que casi siempre tendran palabras como: presentamos, nueva actualización, herramienta, ',
            'tu deber es solo ver la noticia y deberas responder unica y estrictamente estas palabras de dos letras cual sea el caso "SI" o "NO", no deberas responder ni en inglés ni "none", "nothing" ni ningun otra opción o palabras que no sea las dos opciones que te he presentado "si" o "no", ahora te presentaré algunos ejemplos: ',
            'Noticia: Nuestra primera actualización importante a V6 alfa ya está disponible. Se han mejorado todas las cualidades principales del modelo; estética, coherencia, pronta adherencia, calidad de imagen y representación de texto. Los valores más altos de --stylize también funcionan mucho mejor y la ampliación ahora es ~2 veces más rápida. ¡Disfrutar!. Resultado: si',
            'Noticia: OpenAI anuncia la llegada de la GPT Store la próxima semana. Resultado: si',
            'Noticia: Parakeet es un modelo para pasar voz a texto que supera a Whisper. Resultado: si',
            'Noticia: GitHub Copilot Chat ahora está disponible de forma general para organizaciones e individuos: si',
            'Noticia: The wait(list) is over. ✨ Pika 1.0 is officially available to everyone! ✨Create your video on command at http://pika.art.: si',
            'Noticia: Meta just announced Fairy Fast Parallelized Instruction-Guided Video-to-Video Synthesis.: si',
            'Noticia: Presente Assistive Video, la plataforma de video generativo para crear videos a partir de texto e imágenes. Simplemente escriba lo que desea ver y observe cómo sus ideas cobran vida. Está disponible a partir de hoy en la web y a través de API.: si',
            'Noticia: La lista de espera ha terminado. ✨¡Pika 1.0 está oficialmente disponible para todos!. Resultado: si',
            'Noticia: High-Resolution and Prompt-Faithful Text-Guided Image Inpainting with Diffusion Models Resultado: si',
            'Noticia: Agotado. Copias adicionales disponibles el miércoles, 24 de enero. Resultado: no',
            'Noticia: Número 1 de la REVISTA TELESCOPE. Una exploración del arte, la tecnología y la creatividad humana. Disponible ahora en store.runwayml.com. Resultado: no',
            'Noticia: ¡Importante para el FAVICON de tu WEB! Puedes cargar uno diferente para el modo oscuro. Sólo tienes que usar la Media Query en la etiqueta. Resultado: no',
            'Noticia: Este es el plan que suelo seguir para conseguir los primeros 100 usuarios en mis negocios SaaS. Resultado: no',
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