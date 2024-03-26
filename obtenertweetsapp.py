import time
from testSelenium import obtener_tweets
import json

def obtener_tweets_usuarios():
    
    start_time = time.time()

    list_users_not_processed = []

    usertwitter1 = '@aiteamdigital'
    passwordtwitter1 = 'Aiteam321.'
    usertwitter2 = '@AIPedia_tools'
    passwordtwitter2 = 'taipedia2023.'

    users1 = [
                "DotCSV",
                "TheRundownAI",
                "AiBreakfast",
                "_akhaliq",
                "rowancheung",
                "iia_es",
                "theDeepView", 
                "runwayml",
                "huggingface",
                "javilop",
                "DeepLearningAI",
                "Analyticsindiam",
                "krea_ai",
                "xDaily",
                "togethercompute",
                "emulenews",
                "joshua_xu_",
                "OpenAIDevs",
                "LangChainAI",
                "HeyGen_Official",
                "DavidSHolz",
                "NVIDIALA",
                "jackclarkSF",
                "isaacconemail",
                ]

    users2 = [
                "ai_for_success",
                "lmsysorg",
                "PalmerLuckey",
                "seostratega",
                "nutlope",
                "GoogleDeepMind",
                "vercel",
                "pika_labs",
                "llama_index",
                "_philschmid",
                "PhotoGarrido",
                "Muennighoff",
                "WonderDynamics",
                "midudev",
                "playground_ai",
                "kaggle",
                "Xiaomi",
                "heyaiwordsmith",
                "patriciofernanf",
                "luffy_ia",
                "WriteSonic",
                "Neuro_Flash",
                "TUPROFESORIA",
                "sanchitgandhi99",
                ]

    users3 = [
                "NVIDIAAI",
                "xai",
                "OfficialLoganK",
                "GoogleAI",
                "sama",
                "OpenAI",
                "github",
                "StabilityAI",
                "IRLab_UDC",
                "Spain_AI_",
                "BigTechAlert",
                "Donebylaura",
                "AIatMeta",
                "getremixai",
                "Junia_ai",
                "HyperWriteAI",
                "xavier_mitjana",
                "El_Lobo_WS",
                "LeiferMendez",
                "AndrewYNg",
                "ecomlukaskral",
                "StanfordAILab",
                "Tesla_Optimus",
                "Windows"
                ]

    users4 = [
                "synthesiaIO",
                "HelloCivitai",
                "googlechrome",
                "Grammarly",
                "Google",
                "LumaLabsAI",
                "barbbowman",
                "copyelpadrino",
                "neuralink",
                "midjourney",
                "TheRundownTech",
                "serchaicom",
                "Medivis_AR",
                "IAViajero",
                "CohesiveAI",
                "SoyTioDaniel",
                "qdrant_engine",
                "The_CourseAI",
                "LeonardoAi_",
                "sourab_m",
                "RekaAILabs",
                "Auto_GPT",
                "mangelroman"
            ]


    list_users_not_processed.extend(obtener_tweets(users1, usertwitter1, passwordtwitter1))
    list_users_not_processed.extend(obtener_tweets(users2, usertwitter2, passwordtwitter2))
    list_users_not_processed.extend(obtener_tweets(users3, usertwitter1, passwordtwitter1))
    list_users_not_processed.extend(obtener_tweets(users4, usertwitter2, passwordtwitter2))

    while len(list_users_not_processed) > 0:
        print("Existen usuarios por procesar:", len(list_users_not_processed))
        new_users_not_processed = obtener_tweets(list_users_not_processed, usertwitter1, passwordtwitter1)
        list_users_not_processed.clear()  # Limpiar la lista actual
        list_users_not_processed.extend(new_users_not_processed) 

    end_time = time.time()
    total_time_seconds = end_time - start_time
    total_time_minutes = total_time_seconds // 60
    remaining_seconds = total_time_seconds % 60

    print(f"Tiempo total de ejecución: {int(total_time_minutes)} minutos y {int(remaining_seconds)} segundos")