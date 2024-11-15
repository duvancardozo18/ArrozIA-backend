from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.controller.agricultralInputController import (
    createInput, deleteInput, getAllInput, getInputById, updateInput, get_all_units, get_all_input_types
)
from src.database.database import get_session
from src.schemas.agriculturalInputSchema import (
    AgriculturalInput, AgriculturalInputCreate, AgriculturalInputUpdate, UnidadInsumoSchema
)

# Crear el enrutador
AGRICULTURAL_INPUT_ROUTES = APIRouter()

# Rutas para operaciones CRUD de insumos agrícolas
@AGRICULTURAL_INPUT_ROUTES.post('/register-input')
def register_input(input: AgriculturalInputCreate, session: Session = Depends(get_session)):
    return createInput(input, session)

@AGRICULTURAL_INPUT_ROUTES.get('/inputs', response_model=list[AgriculturalInput])
def list_inputs(session: Session = Depends(get_session)):
    return getAllInput(session)

@AGRICULTURAL_INPUT_ROUTES.get('/input/{input_id}', response_model=AgriculturalInput)
def get_input(input_id: int, session: Session = Depends(get_session)):
    return getInputById(input_id, session)

@AGRICULTURAL_INPUT_ROUTES.put('/update/input/{input_id}')
def update_input_route(input_id: int, input: AgriculturalInputUpdate, session: Session = Depends(get_session)):
    return updateInput(input_id, input, session)

@AGRICULTURAL_INPUT_ROUTES.delete('/delete/input/{input_id}')
def delete_input_route(input_id: int, session: Session = Depends(get_session)):
    return deleteInput(input_id, session)

# Ruta para obtener todas las unidades de insumo
@AGRICULTURAL_INPUT_ROUTES.get('/units', response_model=list[UnidadInsumoSchema])
def list_units(session: Session = Depends(get_session)):
    return get_all_units(session)

# Ruta para obtener todos los tipos de insumo
@AGRICULTURAL_INPUT_ROUTES.get('/input-types')
def list_input_types(session: Session = Depends(get_session)):
    return get_all_input_types(session)
