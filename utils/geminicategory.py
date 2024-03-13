import google.generativeai as genai
import os
import dotenv
dotenv.load_dotenv()

genai.configure(api_key= os.getenv('API_GEMINI'))

def category_news(title, content):
    try:
        # Configuración del modelo
        generation_config = {
          "temperature": 0.9,
          "top_p": 1,
          "top_k": 1,
          "max_output_tokens": 2,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-pro")

        prompt_parts = [
            'Tu tarea solo consiste en clasificar noticias, las noticias que clasificaras seran solo de listas de herramientas, tutorial, demos de herramientas o modelos de IA, o papers, más abajo te presentaré las categorias y como debes responder cada categoria, solo debes responder con una categoria, las respuestas solo deben ser dos letras que representan la categoria, estas estaran dentro de las comillas dobles. ',
            'como te dije te presentaré las categorias y debes responder exclusivamente con las dos letras que representan la categoria en minuscula y sin envolverlas en comillas u otro simbolo, solo los dos caracteres: \n',
            '- Tutoriales: cuando la noticia describa la forma de hacer alguna cosa con IA, algún titpo de instrucción o tutorial, y las letras para tutorial seran "tt" \n',
            '- Papers o investigaciones: cuando la noticia habla sobre una nueva investigación o paper de algún nuevo modelo de ia, herramienta o tecnologia, muchas de estas notiicas contienen una url web con la palabra paper y se representa con las letras "pp" \n',
            '- Herramientas: casi siempre son noticias o tweets de personas que hacen listas de herramientas de IA para realizar algun trabajo o ayuda en algún trabajo, la diferencia con una noticia normal es que estas herramietas no son nuevas, entonces si la noticia habla de la herramienta en un contexto de enseñanza o de la lista, puede que no sea una novedad, para representar esta categoria usa "hm" \n',
            '- Demo: casi siempre se pueden reconocer porque tiene la palabra demo o intenta aquí, o prueba desde, son herramientas o mejor dicho modelos de IA recién sacados que no poseen quizás una pagina o oficial o quizás no son un producto oficial de alguna empresa, a veces son solo modelos de una empresa o comunidad opensource que han subido una demo del modelo a huggingFace o replicate o alguna otra plataforma repositorio de IA para la prueba del modelo por parte del usuario, se representan por "dm" \n',
            '- News: esta deberia ser la categoria predominante, esta categoria solo recoge aquellas noticias o innovaciones, noticias que hablan de un nuevo modelo, es decir esa primicia que anuncia por primera vez algo que ha salido, una nueva funcionalidad, una herramienta pero en este caso es nueva, una actualizacion de una herramienta, una noticia importante en el mundo de la IA, en fin una primicia digna de un diario degital de noticias puedes tener en cuenta que estas noticias seran la mayoria y seran la categoria que no encaja con las categorias antes descritas y se representa la categoria con las letras "nw" \n',
            '- Sin Categoria: si no llegas a determinar una categoria para la noticia "nc" así debes evitar responder con  None \n',
            'Ahora te presentaré la noticia: \n',
            f'titulo: {title}',
            f'contenido: {content}',
            'respuesta: ',
        ]

        response = model.generate_content(prompt_parts)
        return response.text

    except Exception as e:
        # Manejar la excepción
        print(f"Error en la generación de category_new: {e}")
        # Puedes decidir devolver un valor predeterminado o propagar la excepción
        return None