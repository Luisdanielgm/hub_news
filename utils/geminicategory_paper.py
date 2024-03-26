import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def category_paper(title, content):
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
            'Tu tarea solo consiste en determinar si esta noticia es una paper o investigación de inteligencia artificial, incluso si no es una investigacióndirecta si no un articulo o noticia que hablé o mencione algún estudio o paper de IA, podrás incluso también identificarlas debido a que algunas tienen una url con la palabra paper otras no tiene una url pero si hablan de la investigación, recuerda que estas noticias deben estar respaldadas por una investigación de una institución o algún articulo cientifico sobre IA, si es una noticia de tipo paper responderas con las dos letras "pp" y si no responderas con las dos letras "nn".\n',
            'entonces si es una noticia de tipo paper de IA solo responderas con las dos letras "pp" y si no responderas con "nn", te mostraré algunos ejemplos de correcta clasificación:\n',
            'google presenta genie, un modelo que aprende a generar mundos interactivos para video juegos, respuestas: pp\n',
            '¿Te imaginas que la administración pública pudiera detectar el fraude de una baja médica gracias a la #IA? Sí es posible, en países como #Singapur ya tienen este modelo en producción. Algunas de sus ventajas son: Identificar cuánto tiempo de baja necesita el paciente.…, respuestas: pp\n',
            'GROK-1 YA ES OPEN SOURCE! Acabo de aterrizar en San Francisco y por suerte OpenAI no ha liberado nada durante el vuelo, pero Elon Musk sí ha cumplido con su palabra de liberar a Grok-1 durante esta semana. Un modelo tipo MoE de 314B !! Habrá qué ver cómo rinde :), respuestas: nn\n',
            'En primer lugar, la predicción más obvia para GPT-5 es que será multimodal, compatible con texto, imagen, audio y vídeo desde cero., respuestas: nn\n',
            'Investigadores muestran como un chatbot basado en IA y que es tutor de matematicas han mejorado el aprendizaje de niños en africa, respuestas: pp\n',
            'Servicio de correo electrónico gratuito que permite recibir correo en una dirección temporal que se autodestruye después de que transcurra un cierto tiempo., respuestas: nn\n',
            'Se cumple un año desde el lanzamiento de GPT-4. Espero que todos hayan disfrutado de algo de tiempo para relajarse; habrán sido los 12 meses más lentos de progreso de IA durante bastante tiempo., respuestas: nn\n',
            'La demo de VideoMamba ya salió Modelo de estado de espacio para un entendimiento de video eficiente., respuestas: nn\n',
            '¿Cuál es el mejor método para inyectar nuevos conocimientos en los LLM? Leer más https://lnkd.in/d8TQaSBE, respuestas: pp\n',
            'El lanzamiento del último modelo de IA de Anthropic, Claude-3, que se dice que sobrepasa las capacidades de GPT-4, ha reavivado el debate sobre AGI una vez más., respuestas: nn\n',
            '¡Nos emociona compartir nuestro trabajo más reciente! Proponemos un método sin supervisión que consigue un nuevo estado del arte en edición de vídeo basada en texto. Compruébalo: https://fdd-video-edit.github.io, respuestas: nn\n',
            'Google acaba de anunciar una actualización masiva. ¡La IA está ahora dentro de Google Maps! Aquí hay 5 nuevas características AI Powered de Google Maps, que no querrá perderse., respuestas: nn\n',
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