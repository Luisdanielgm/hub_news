import time
from testSelenium import obtener_tweets
import json

def obtener_tweets_usuarios():
    
    start_time = time.time()

    #users = ['DotCSV', 'IAViajero', 'Copyelpadrino']
    users = ["DotCSV",
                "TheRundownAI",
                "krea_ai",
                "AiBreakfast",
                "rowancheung",
                "seostratega",
                "vercel",
                "pika_labs",
                "HyperWriteAI",
                "El_Lobo_WS",
                "patriciofernanf",
                "HelloCivitai",
                "TUPROFESORIA",
                "Windows",
                "PalmerLuckey",
                "ai_for_success",
                "Donebylaura",
                "OpenAIDevs",
                "playground_ai",
                "sanchitgandhi99",
                "lmsysorg",
                "llama_index",
                "LeiferMendez",
                "isaacconemail",
                "xai",
                "OfficialLoganK",
                "IRLab_UDC",
                "Spain_AI_",
                "getremixai",
                "github",
                "_philschmid",
                "StabilityAI",
                "synthesiaIO",
                "ecomlukaskral",
                "StanfordAILab",
                "GoogleDeepMind",
                "AIatMeta",
                "GoogleAI",
                "googlechrome",
                "Google",
                "LumaLabsAI",
                "barbbowman",
                "nutlope",
                "xavier_mitjana",
                "copyelpadrino",
                "serchaicom",
                "IAViajero",
                "CohesiveAI",
                "SoyTioDaniel",
                "NVIDIAAI",
                "OpenAI",
                "sama",
                "qdrant_engine",
                "midjourney",
                "TheRundownTech",
                "The_CourseAI",
                "neuralink",
                "AndrewYNg",
                "huggingface",
                "_akhaliq",
                "Medivis_AR",
                "LeonardoAi_",
                "sourab_m",
                "RekaAILabs",
                "Auto_GPT",
                "bebeAGI_",
                "PhotoGarrido",
                "mangelroman"]


    obtener_tweets(users)

    end_time = time.time()
    total_time_seconds = end_time - start_time
    total_time_minutes = total_time_seconds // 60
    remaining_seconds = total_time_seconds % 60

    print(f"Tiempo total de ejecución: {int(total_time_minutes)} minutos y {int(remaining_seconds)} segundos")