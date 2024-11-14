from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from src.controller.cities_Controller import filter_departments, filter_cities_by_department

router = APIRouter()

# Endpoint para filtrar departamentos
@router.get("/departments/filter")
async def get_filtered_departments(query: str = Query(..., min_length=1, description="Parte del nombre del departamento")):
    filtered_departments = filter_departments(query)
    return JSONResponse(content=filtered_departments)

# Endpoint para filtrar ciudades por departamento
@router.get("/departments/{department_id}/cities/filter")
async def get_filtered_cities(department_id: int, query: str = Query(..., min_length=1, description="Parte del nombre de la ciudad")):
    filtered_cities = filter_cities_by_department(department_id, query)
    return JSONResponse(content=filtered_cities)
