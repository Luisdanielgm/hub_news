import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def category_hm(title, content):
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
            'Tu tarea solo consiste en determinar si esta noticia es una lista de herramientas o la promoción de alguna herramienta, no una herramienta nueva que acaba de salir si no alguna herramienta la cual alguien está recomendando o la lista o top de algunas herramientas, si es una noticia de tipo herramientas responderas con las dos letras "hm" y si no responderas con las dos letras "nn".\n',
            'entonces si es una noticia de tipo herramientas solo responderas con las dos letras "hm" y si no responderas con "nn", te mostraré algunos ejemplos de correcta clasificación:\n',
            'Descubre estas nueve herramientas de IA que te convertiran en un profesional del marketing, respuestas: hm\n',
            'Tal vez no quiera un LLM "seguro/justo/imparcial", respuestas: nn\n',
            'Andooril, respuestas: nn\n',
            'Ya conoces leonardo AI, podrás crear imagenes impresionantes, respuestas: hm\n',
            'Servicio de correo electrónico gratuito que permite recibir correo en una dirección temporal que se autodestruye después de que transcurra un cierto tiempo., respuestas: nn\n',
            'La próxima vez que veas a Ilya, probablemente se verá así., respuestas: nn\n',
            'Si te dijeran que @Magnific_AI es un startup americana en la que trabajan 20 ingenieros de Standford o MIT y que ha levantado $29M con inversores como Jeff Bezos, te cuadraría completamente.., respuestas: nn\n',
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