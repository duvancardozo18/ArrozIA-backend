from datetime import date, datetime, timedelta, time
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException
from src.models.weatherRecordModel import WeatherRecord
from src.schemas.weatherRecordSchema import WeatherRecordCreate
from src.models.landModel import Land
import requests
import os
import json  # Importa json para almacenar la respuesta como texto

# Función para crear un registro meteorológico desde la API de OpenWeather
def createWeatherRecordFromAPI(db: Session, lote_id: int, latitud: float = None, longitud: float = None):
    # Obtener el lote desde la base de datos
    lote = db.query(Land).filter(Land.id == lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

     # Validar las coordenadas recibidas
    if not latitud or not longitud:
        raise HTTPException(status_code=500, detail="Latitud o longitud no proporcionadas")

    # Configuración de la solicitud a OpenWeather
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitud}&lon={longitud}&appid={api_key}&units=metric"

    # Realizar la solicitud
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Error de OpenWeather: {response.json().get('message', 'Desconocido')}")

    # Obtener los datos de la respuesta
    data = response.json()

    # Agrega logs para depuración
    print(f"Datos de OpenWeather: {data}")
    print(f"Horas de sol recibidas: {data.get('clouds', {}).get('all', 'No especificado')}")

    # Extraer y procesar los datos relevantes
    horas_sol = data.get('clouds', {}).get('all', 0)  # Ajusta según los datos que devuelve OpenWeather
    if horas_sol > 99.99:  # Validación adicional
        horas_sol = 99.99  # Ajusta al rango permitido en la base de datos
        print(f"Horas de sol ajustadas a: {horas_sol}")

    # Crear el registro meteorológico
    weather_record = WeatherRecord(
        lote_id=lote_id,
        fecha=date.today(),
        hora=datetime.now().time() if datetime.now().time() else time(0, 0),  # Hora predeterminada si no está presente
        temperatura=data["main"]["temp"],
        presion_atmosferica=data["main"]["pressure"],
        humedad=data["main"]["humidity"],
        precipitacion=data.get("rain", {}).get("1h", 0.0),
        indice_ultravioleta=0.0,
        horas_sol=horas_sol,  # Usa el valor ajustado
        fuente_datos="api",
        api_respuesta=json.dumps(data)  # Guarda la respuesta completa como JSON
    )

    # Guardar en la base de datos
    db.add(weather_record)
    db.commit()
    db.refresh(weather_record)

    return weather_record



# Función para obtener el historial meteorológico de un lote con filtros opcionales
def fetchWeatherHistory(db: Session, lote_id: int, start_date: str = None, end_date: str = None, fuente_datos: str = None):
    # Si no se proporciona start_date, usar un año atrás desde la fecha actual
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).date()
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    # Si no se proporciona end_date, usar la fecha de hoy
    if not end_date:
        end_date = datetime.now().date()
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Obtener registros en el rango de fechas especificado
    query = db.query(WeatherRecord).filter(
        WeatherRecord.lote_id == lote_id,
        WeatherRecord.fecha >= start_date,
        WeatherRecord.fecha <= end_date
    )
    
    # Si se proporciona fuente_datos, filtrar por eso
    if fuente_datos:
        query = query.filter(WeatherRecord.fuente_datos == fuente_datos)

    registros = query.all()


    # Asignar una hora predeterminada (00:00:00) a los registros donde hora es None
    for record in registros:
        if record.hora is None:
            record.hora = time(0, 0)

    if not registros:
        raise HTTPException(status_code=404, detail="No se encontraron registros en el rango de fechas especificado")

    return registros

# Función para obtener el detalle de un registro meteorológico específico
def fetchWeatherRecordDetail(db: Session, id: int):
    record = db.query(WeatherRecord).filter(WeatherRecord.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record

# Función para crear un registro meteorológico manual
def createManualWeatherRecord(db: Session, record: WeatherRecordCreate, lote_id: int):
    # Buscar el lote correspondiente a partir del lote_id
    lote = db.query(Land).filter(Land.id == lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    # Crear el registro meteorológico con la referencia al lote
    dbRecord = WeatherRecord(
        lote_id=lote_id,  # Asociamos el lote_id al registro
        fecha=record.fecha,
        hora=record.hora,
        temperatura=record.temperatura,
        presion_atmosferica=record.presion_atmosferica,
        humedad=record.humedad,
        precipitacion=record.precipitacion,
        indice_ultravioleta=record.indice_ultravioleta,
        horas_sol=record.horas_sol,
        fuente_datos="manual"  # Asignamos "manual" a la fuente de datos
    )
    
    db.add(dbRecord)
    db.commit()
    db.refresh(dbRecord)
    return dbRecord

# Función para crear un registro meteorológico general
def createWeatherRecord(db: Session, record: WeatherRecordCreate):
    dbRecord = WeatherRecord(**record.dict())
    db.add(dbRecord)
    db.commit()
    db.refresh(dbRecord)
    return dbRecord

# Función para obtener un registro meteorológico específico por fecha y lote
def fetchWeatherRecord(db: Session, fecha: date, lote_id: int):
    return db.query(WeatherRecord).filter(
        WeatherRecord.fecha == fecha,
        WeatherRecord.lote_id == lote_id
    ).first()

# Función para generar recomendaciones meteorológicas basadas en registros de un lote
def getWeatherRecommendations(db: Session, lote_id: int):
    # Obtener todos los registros meteorológicos del lote especificado
    registros = db.query(WeatherRecord).filter(WeatherRecord.lote_id == lote_id).all()
    
    if not registros:
        raise HTTPException(status_code=404, detail="No se encontraron registros para el lote especificado")

    # Ejemplo de análisis simple: calcular el promedio de temperatura
    promedio_temperatura = sum(r.temperatura for r in registros) / len(registros)

    # Generar recomendaciones basadas en el análisis
    if promedio_temperatura > 30:
        recomendacion = "Riego adicional necesario debido a altas temperaturas."
    elif promedio_temperatura < 20:
        recomendacion = "Temperaturas bajas, monitorear posibles heladas."
    else:
        recomendacion = "Condiciones climáticas favorables para el cultivo."

    # Retornar la recomendación generada
    return {"recomendacion": recomendacion, "promedio_temperatura": promedio_temperatura}

# Función para actualizar un registro meteorológico específico
def updateWeatherRecord(db: Session, record_id: int, record_data: WeatherRecordCreate):
    existing_record = db.query(WeatherRecord).filter(WeatherRecord.id == record_id).first()
    if not existing_record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    # Actualizar todos los campos del registro existente
    for key, value in record_data.dict(exclude_unset=True).items():
        setattr(existing_record, key, value)
    
    db.commit()
    db.refresh(existing_record)
    return existing_record
