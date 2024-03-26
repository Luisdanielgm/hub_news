import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def category_news(title, content):
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
            'Tu tarea solo consiste en determinar si esta noticia es relevante para mi diario digital de inteilencia artificial como titular, es decir solo deberas clasificar como noticias aquellas que sean el lanzamiento de una novedad en inteligencia artificial o algo que es relevante para mi diario digital.\n',
            'si es una noticia relevante responderas solo con las dos letras "nw" si no responderas con "nn", te mostraré algunos ejemplos de correcta clasificación:\n',
            'Los ejecutivos de OpenAI, Jason Kwon y Sam Altman, han rechazado las afirmaciones de Elon Musk y están abordando internamente la nueva demanda presentada por Musk., respuestas: nw\n',
            'Servicio de correo electrónico gratuito que permite recibir correo en una dirección temporal que se autodestruye después de que transcurra un cierto tiempo., respuestas: nw\n',
            '1 mes de Dropshipping 1 mes de SMMA 1 mes de SaaS 1 mes de Criptomonedas = 0 € VS 4 meses de Afiliación Hotmart + TikTok = 3300 € al mes, respuestas: nn\n',
            'GROK-1 YA ES OPEN SOURCE! Acabo de aterrizar en San Francisco y por suerte OpenAI no ha liberado nada durante el vuelo, pero Elon Musk sí ha cumplido con su palabra de liberar a Grok-1 durante esta semana. Un modelo tipo MoE de 314B !! Habrá qué ver cómo rinde :), respuestas: nw\n',
            'Tendríamos nada menos de Lykon., respuestas: nn\n',
            'Andooril, respuestas: nn\n',
            'JUNTO CON HYDRA, respuestas: nn\n',
            'JUNTO A DENTORO, respuestas: nn\n',
            'Inflection ha lanzado Inflection-2.5, una actualización significativa de su modelo que impulsa su asistente personal de IA Pi, alcanzando un rendimiento del 94 de GPT-4 en diversas tareas, utilizando solo el 40 del cómputo de entrenamiento., respuestas: nw\n',
            'Tal vez no quiera un LLM "seguro/justo/imparcial", respuestas: nn\n',
            '10 sitios web locos que podrías no saber que existen (todos GRATIS)., respuestas: nw\n',
            'Esta semana, después de once años con este proyecto, llegamos a los ¡300 Recreos Naukas! Por este motivo, veremos la charla que impartí en #NaukasBilbao23 relatando en qué consiste este nuevo espacio de divulgación científica., respuestas: nn\n',
            'La Comisión de Servicios Públicos de California (CPUC) ha otorgado a Waymo el permiso para ampliar sus operaciones de robotaxi a áreas de Los Ángeles y la Península de San Francisco, lo que permite a los vehículos circular a velocidades de hasta 65 mph., respuestas: nw\n',
            'Cuando hice esta foto del Matterhorn buscaba que evocara a esas ilustraciones japonesas tradicionales del monte Fuji., respuestas: nn\n',
            'La próxima vez que veas a Ilya, probablemente se verá así., respuestas: nn\n',
            'Alibaba, el gigante del comercio electrónico, encabezó una ronda de financiación de 600 millones de dólares para respaldar a MiniMax, una startup china especializada en inteligencia artificial., respuestas: nw\n',
            'Y comparativa con el modo realista., respuestas: nn\n',
            'Groq, la prominente startup de chips de IA, ha dado un paso audaz para fortalecer su presencia en el ámbito del hardware al anunciar la creación de Groq Systems y la adquisición estratégica de Definitive Intelligence., respuestas: nw\n',
            'Un tutor de matemáticas con IA mejora el rendimiento en Ghana: Un nuevo estudio en Ghana encontró que los estudiantes que utilizaron Rori, un tutor de matemáticas con chatbot impulsado por inteligencia artificial, obtuvieron puntajes de matemáticas significativamente más altos., respuestas: nw\n',
            '¿Y los tuyos? ¿Cuáles te vienen a la mente? Comparte si te gustan este tipo de recomendaciones más alejadas de mis temas tradicionales de IA o startups., respuestas: nn\n',
            'Los chatbots de IA desarrollados por TurboTax y H&R Block fueron sometidos a pruebas por parte del Washington Post, revelando que casi el 50 de las respuestas proporcionadas eran engañosas o incorrectas., respuestas: nw\n',
            'Tres visionado que me impactaron enormemente en mi vida y a los que vuelvo una y otra vez como fuente de inspiración/reflexión., respuestas: nn\n',
            'Midjourney también ha anunciado el lanzamiento de v6 turbo, una actualización que permite a los usuarios generar imágenes a una velocidad 3.5 veces mayor que la habitual., respuestas: nw\n',
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