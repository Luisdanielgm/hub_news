import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def category_tuto(title, content):
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
            'Tu tarea solo consiste en determinar si esta noticia es un tutorial de como utilizar una herramienta de IA o de como crear una aplicación o de como hacer alguna actividad usando IA, estas noticias casi siempre tendrán frases como: "como crear", "como hacer", "tutorial", "aprende a", si la noticia de tipo tutorial responderas con las dos letras "tt" y si no responderas con las dos letras "nn".\n',
            'entonces si es una noticia de tipo tutorial solo responderas con las dos letras "tt" y si no responderas con "nn", te mostraré algunos ejemplos de correcta clasificación:\n',
            'Aprende a crear imagenes con el nuevo modelo de IA de alibaba: tt\n',
            'Aprende como crear una app RAG de IA con nosotros, respuestas: tt\n',
            'Servicio de correo electrónico gratuito que permite recibir correo en una dirección temporal que se autodestruye después de que transcurra un cierto tiempo., respuestas: nn\n',
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