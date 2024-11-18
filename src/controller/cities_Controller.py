import os
import json
import re
from fastapi import HTTPException

# Ruta al archivo JSON
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), '../data/cities.json')

# Cargar los datos del archivo JSON
def get_cities_data():
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar los datos: {e}")

# Función para filtrar departamentos basándose en un patrón exacto de letras en orden y consecutivas
def filter_departments(query: str):
    data = get_cities_data()
    # Usar una expresión regular que asegure que las letras estén juntas y en orden
    pattern = re.compile(f"^{re.escape(query)}", re.IGNORECASE)
    filtered_departments = [
        {"id": dept["id"], "departamento": dept["departamento"]}
        for dept in data
        if pattern.search(dept["departamento"])
    ]
    return filtered_departments

# Función para filtrar ciudades dentro de un departamento específico
def filter_cities_by_department(department_id: int, query: str):
    data = get_cities_data()
    pattern = re.compile(f"^{re.escape(query)}", re.IGNORECASE)
    for department in data:
        if department["id"] == department_id:
            filtered_cities = [
                city for city in department["ciudades"] if pattern.search(city)
            ]
            return {"id": department["id"], "departamento": department["departamento"], "ciudades": filtered_cities}
    return {"error": "Departamento no encontrado"}
