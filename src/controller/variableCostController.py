from sqlalchemy.orm import Session
from src.models.variableCostModel import VariableCost
from src.schemas.variableCostSchema import VariableCostsCreate, VariableCostsResponse
from src.database.database import get_db
from sqlalchemy.orm import joinedload

# Crear un nuevo gasto variable
def create_variable_cost(db: Session, variable_cost: VariableCostsCreate):
    db_variable_cost = VariableCost(
        id_costos_adicionales=variable_cost.id_costos_adicionales,
        id_agua=variable_cost.id_agua,
        id_gastos_administrativos_financieros=variable_cost.id_gastos_administrativos_financieros,
        descripcion=variable_cost.descripcion
    )
    db.add(db_variable_cost)
    db.commit()
    db.refresh(db_variable_cost)
    return db_variable_cost

# Obtener todos los gastos variables con los campos de las relaciones
def get_variable_costs(db):
    variable_costs = db.query(VariableCost).options(
        joinedload(VariableCost.costos_adicionales),
        joinedload(VariableCost.agua),
        joinedload(VariableCost.gastos_administrativos_financieros)
    ).all()

    response = []
    for variable_cost in variable_costs:
        # Verificamos si las relaciones están presentes antes de acceder a ellas
        costos_adicionales_nombre = variable_cost.costos_adicionales.costo_capacitacion_real if variable_cost.costos_adicionales else None
        agua_consumo = variable_cost.agua.costo_consumo_agua_real if variable_cost.agua else None
        gastos_administrativos_impuesto = variable_cost.gastos_administrativos_financieros.costo_impuestos_real if variable_cost.gastos_administrativos_financieros else None
        agua_consumo_energia = variable_cost.agua.consumo_energia_estimada if variable_cost.agua and variable_cost.agua.consumo_energia_estimada is not None else 0.0

        response.append({
            "id": variable_cost.id,
            "descripcion": variable_cost.descripcion,
            "costos_adicionales_nombre": costos_adicionales_nombre,
            "agua_consumo": agua_consumo,
            "gastos_administrativos_impuesto": gastos_administrativos_impuesto,
            "agua_consumo_energia": agua_consumo_energia
        })

    return response


# Función para obtener los detalles de los gastos variables
def get_variable_costs_details(db: Session):
    return db.query(VariableCost).all()

# Obtener un solo gasto variable por ID
def get_variable_cost_by_id(db: Session, variable_cost_id: int):
    return db.query(VariableCost).filter(VariableCost.id == variable_cost_id).first()

# Actualizar un gasto variable
def update_variable_cost(db: Session, variable_cost_id: int, variable_cost: VariableCostsCreate):
    db_variable_cost = db.query(VariableCost).filter(VariableCost.id == variable_cost_id).first()
    if db_variable_cost:
        db_variable_cost.id_costos_adicionales = variable_cost.id_costos_adicionales
        db_variable_cost.id_agua = variable_cost.id_agua
        db_variable_cost.id_gastos_administrativos_financieros = variable_cost.id_gastos_administrativos_financieros
        db_variable_cost.descripcion = variable_cost.descripcion
        db.commit()
        db.refresh(db_variable_cost)
    return db_variable_cost

# Eliminar un gasto variable
def delete_variable_cost(db: Session, variable_cost_id: int):
    db_variable_cost = db.query(VariableCost).filter(VariableCost.id == variable_cost_id).first()
    if db_variable_cost:
        db.delete(db_variable_cost)
        db.commit()
    return db_variable_cost
