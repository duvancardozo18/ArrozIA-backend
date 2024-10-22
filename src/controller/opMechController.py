from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.models.opMechModel import OpMech
from src.schemas.opMechSchema import OpMechCreate, OpMechUpdate


# Crear una nueva operación mecanización
def create_op_mech(operation: OpMechCreate, db: Session):
    # Verificar si ya existe una operación con el mismo taskId
    existing_operation = db.query(OpMech).filter(OpMech.taskId == operation.taskId).first()
    
    if existing_operation:
        # Lanzar una excepción si ya existe una operación con el mismo taskId
        raise HTTPException(status_code=400, detail="Ya existe una operación mecanización con el mismo taskId")
    
    # Si no existe, crear la nueva operación
    db_operation = OpMech(
        taskId=operation.taskId,
        mechanizationName=operation.mechanizationName,
        machineryId=operation.machineryId,
        hoursUsed=operation.hoursUsed
    )
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation


# Obtener una operación mecanización por ID
def get_op_mech_by_id(op_mech_id: int, db: Session):
    return db.query(OpMech).filter(OpMech.id == op_mech_id).first()


# Obtener todas las operaciones mecanización
def get_all_op_mechs(db: Session):
    return db.query(OpMech).all()


# Actualizar una operación mecanización por ID
def update_op_mech(op_mech_id: int, operation: OpMechUpdate, db: Session):
    db_operation = db.query(OpMech).filter(OpMech.id == op_mech_id).first()
    if db_operation:
        db_operation.taskId = operation.taskId
        db_operation.mechanizationName = operation.mechanizationName
        db_operation.machineryId = operation.machineryId
        db_operation.hoursUsed = operation.hoursUsed
        db.commit()
        db.refresh(db_operation)
        return db_operation
    else:
        raise HTTPException(status_code=404, detail="Operación mecanización no encontrada")

# Eliminar una operación mecanización por ID
def delete_op_mech(op_mech_id: int, db: Session):
    db_operation = db.query(OpMech).filter(OpMech.id == op_mech_id).first()
    if not db_operation:
        raise HTTPException(status_code=404, detail="Operación mecanización no encontrada")
    db.delete(db_operation)
    db.commit()
    return {"message": "Operación mecanización eliminada correctamente"}