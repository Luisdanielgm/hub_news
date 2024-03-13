from datetime import datetime, timedelta, timezone

# Función para convertir una fecha en "Hace X horas"
def convert_to_hours_ago(date_str):
    # Fecha actual en UTC con información de zona horaria
    fecha_actual = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Formatos a probar
    formats = ['%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%SZ', '%b %d, %Y · %I:%M %p UTC', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%fZ']

    # Intentar parsear la fecha con los formatos dados
    for fmt in formats:
        try:
            fecha_proporcionada = datetime.strptime(date_str, fmt)
            # Si el formato no tiene información de zona horaria, asumir UTC
            if fecha_proporcionada.tzinfo is None:
                fecha_proporcionada = fecha_proporcionada.replace(tzinfo=timezone.utc)
            break
        except ValueError:
            continue
    else:
        raise ValueError("Formato de fecha no reconocido")

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

    # Formato normalizado para la fecha proporcionada
    # Este formato es comúnmente utilizado para búsquedas y ordenamiento
    date_normalized = fecha_proporcionada.strftime('%Y-%m-%d %H:%M:%S')

    return resultado, date_normalized


    

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
