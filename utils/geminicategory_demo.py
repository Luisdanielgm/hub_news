import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def category_demo(title, content):
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
            'Tu tarea solo consiste en determinar si esta noticia es una Demo de algún modelo de inteligencia artificial o una demo de alguna herramienta, casí siempre este tipo de noticias tendrán una invitación de probar la herramienta pudiendo incluso tener un enlace o link url, además deben ser solo demos de alguna innovación, no deben ser demos de herramientas ya vistas, si no demos de herramientas nuevas o modelos nuevos los cuales casi siempre no son herramientas ya comerciales si no acabadas de salir o incluso tecnologicas nuevas, también casi siempre estas demos estan alojadas en sitios como huggingFace que es un repositorio de IA o replicate es otro sitio, o incluso más sitios de repositorios de IA, si es una noticia de demo responderas con las dos letras "dm" y si no responderas con las dos letras "nn".\n',
            'entonces si es una demo solo con las dos letras "dm" y si no responderas con "nn", te mostraré algunos ejemplos de correcta clasificación:\n',
            'Acaba de salir un nuevo modelo el cual elimina el fondo de imagenes de manera muy eficaz, puedes comprobarlo en huggingFace., respuestas: dm\n',
            'Servicio de correo electrónico gratuito que permite recibir correo en una dirección temporal que se autodestruye después de que transcurra un cierto tiempo., respuestas: nn\n',
            'La demo de VideoMamba ya salió Modelo de estado de espacio para un entendimiento de video eficiente, respuestas: dm\n',
            'ahora te presento la noticia a clasificar:\n',
            f'titulo: {title}\n',
            f'contenido: {content}\n',
            'respuesta:\n',
        ]

        response = model.generate_content(prompt_parts)
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error en la generación de category_new: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None