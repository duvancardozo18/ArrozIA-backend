from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controller.opMechController import create_op_mech, get_op_mech_by_id, get_all_op_mechs, update_op_mech, delete_op_mech
from src.schemas.opMechSchema import OpMechCreate, OpMechUpdate, OpMechResponse
from src.database.database import get_db

OP_MECH_ROUTES = APIRouter()


# Crear una nueva operación mecanización
@OP_MECH_ROUTES.post("/operation-mechanization/", response_model=OpMechCreate)
def create_operation_mechanization(operation: OpMechCreate, db: Session = Depends(get_db)):
    return create_op_mech(operation, db)


# Obtener una operación mecanización por ID
@OP_MECH_ROUTES.get("/operation-mechanization/{op_mech_id}", response_model=OpMechResponse)
def read_operation_mechanization(op_mech_id: int, db: Session = Depends(get_db)):
    db_op_mech = get_op_mech_by_id(op_mech_id, db)
    if db_op_mech is None:
        raise HTTPException(status_code=404, detail="Operación mecanización no encontrada")
    return db_op_mech


# Obtener todas las operaciones mecanización
@OP_MECH_ROUTES.get("/operation-mechanizations/", response_model=list[OpMechResponse])
def read_all_operation_mechanizations(db: Session = Depends(get_db)):
    return get_all_op_mechs(db)



# Actualizar una operación mecanización
@OP_MECH_ROUTES.put("/operation-mechanization/{op_mech_id}", response_model=OpMechCreate)
def update_operation_mechanization(op_mech_id: int, operation: OpMechUpdate, db: Session = Depends(get_db)):
    return update_op_mech(op_mech_id, operation, db)


# Eliminar una operación mecanización
@OP_MECH_ROUTES.delete("/operation-mechanization/{op_mech_id}", response_model=dict)
def delete_operation_mechanization(op_mech_id: int, db: Session = Depends(get_db)):
    return delete_op_mech(op_mech_id, db)