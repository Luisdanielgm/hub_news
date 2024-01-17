from datetime import datetime, timedelta

# Función para convertir una fecha en "Hace X horas"
def convert_to_hours_ago(date):
    # Fecha actual
    fecha_actual = datetime.utcnow()

    # Convierte la fecha proporcionada en formato ISO 8601 a datetime
    fecha_proporcionada = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

    # Calcula la diferencia de tiempo
    diferencia = fecha_actual - fecha_proporcionada

    # Calcula días, horas y minutos
    dias = diferencia.days
    horas_restantes = diferencia.seconds // 3600  # Calcula las horas restantes en el último día
    minutos_restantes = (diferencia.seconds % 3600) // 60  # Calcula los minutos restantes

    # Formatea la cadena resultante
    if dias == 0:
        if horas_restantes < 1:
            if minutos_restantes == 0:
                resultado = "Hace menos de un minuto"
            elif minutos_restantes == 1:
                resultado = "Hace 1 minuto"
            else:
                resultado = f"Hace {minutos_restantes} minutos"
        elif horas_restantes == 1:
            resultado = "Hace 1 hora"
        else:
            resultado = f"Hace {horas_restantes} horas"
    elif dias == 1:
        resultado = "Hace 1 día"
    else:
        resultado = f"Hace {dias} días"
        if horas_restantes > 0:
            resultado += f" y {horas_restantes} horas"

    return resultado

    

# Función para obtener todas las URLs de imágenes
def extract_image_urls(img_tag):
    if not img_tag:
        return []
    img_urls = [img_tag['src']]
    srcset = img_tag.get('srcset')
    if srcset:
        srcset_urls = [img.split()[0] for img in srcset.split(",")]
        img_urls.extend(srcset_urls)
    return list(set(img_urls))  # Elimina duplicados, si los hay
