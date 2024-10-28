from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.weatherRecordModel import WeatherRecord
from src.schemas.weatherRecordSchema import WeatherRecordCreate

def createWeatherRecord(db: Session, record: WeatherRecordCreate):
    dbRecord = WeatherRecord(**record.dict())
    db.add(dbRecord)
    db.commit()
    db.refresh(dbRecord)
    return dbRecord

def fetchWeatherRecord(db: Session, fecha: date, lote_id: int):
    return db.query(WeatherRecord).filter(
        WeatherRecord.fecha == fecha,
        WeatherRecord.lote_id == lote_id
    ).first()

def fetchWeatherHistory(db: Session, lote_id: int, start_date: str = None, end_date: str = None):
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
    registros = db.query(WeatherRecord).filter(
        WeatherRecord.lote_id == lote_id,
        WeatherRecord.fecha >= start_date,
        WeatherRecord.fecha <= end_date
    ).all()

    if not registros:
        raise HTTPException(status_code=404, detail="No se encontraron registros en el rango de fechas especificado")

    return registros

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
