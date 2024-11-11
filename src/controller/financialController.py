from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.additionalCostsModel import AdditionalCosts
from src.models.financialExpensesModel import FinancialExpenses
from src.models.laborCulturalModel import LaborCultural
from src.models.taskModel import Task
from src.models.machineryModel import Machinery
from src.models.agriculturalInputModel import AgriculturalInput

# Funciones de costos reales
def calculate_total_additional_costs(db: Session):
    total_training_cost = db.query(func.sum(AdditionalCosts.costo_capacitacion_real)).scalar() or 0
    total_rodent_control_cost = db.query(func.sum(AdditionalCosts.costo_control_roedores_real)).scalar() or 0
    return total_training_cost + total_rodent_control_cost

def calculate_total_financial_expenses(db: Session):
    total_tax_cost = db.query(func.sum(FinancialExpenses.costo_impuestos_real)).scalar() or 0
    total_insurance_cost = db.query(func.sum(FinancialExpenses.costo_seguros_real)).scalar() or 0
    return total_tax_cost + total_insurance_cost

def get_real_labor_costs(db: Session):
    return db.query(
        LaborCultural.nombre.label("nombre"),
        func.sum(Task.tiempo_hora * LaborCultural.precio_hora_real).label("costo_total"),
        func.sum(Task.tiempo_hora).label("total_horas")
    ).join(Task, Task.labor_cultural_id == LaborCultural.id)\
    .filter(LaborCultural.precio_hora_real.isnot(None))\
    .group_by(LaborCultural.nombre)\
    .all()

def get_real_machinery_costs(db: Session):
    return db.query(
        Machinery.name.label("nombre"),
        func.sum(Task.tiempo_hora * Machinery.costPerHour).label("costo_total"),
        func.sum(Task.tiempo_hora).label("total_horas")
    ).join(Task, Task.maquinaria_agricola_id == Machinery.id)\
    .group_by(Machinery.name)\
    .all()

def get_real_agricultural_input_costs(db: Session):
    return db.query(
        AgriculturalInput.nombre.label("nombre"),
        func.sum(AgriculturalInput.cantidad * AgriculturalInput.costo_unitario).label("costo_total"),
        func.sum(AgriculturalInput.cantidad).label("total_cantidad")
    ).group_by(AgriculturalInput.nombre).all()

# Funciones de costos estimados
def calculate_total_estimated_additional_costs(db: Session):
    total_training_cost = db.query(func.sum(AdditionalCosts.costo_capacitacion_estimado)).scalar() or 0
    total_rodent_control_cost = db.query(func.sum(AdditionalCosts.costo_control_roedores_estimado)).scalar() or 0
    return total_training_cost + total_rodent_control_cost

def calculate_total_estimated_financial_expenses(db: Session):
    total_tax_cost = db.query(func.sum(FinancialExpenses.costo_impuestos_estimado)).scalar() or 0
    total_insurance_cost = db.query(func.sum(FinancialExpenses.costo_seguros_estimado)).scalar() or 0
    return total_tax_cost + total_insurance_cost

def get_estimated_labor_costs(db: Session):
    return db.query(
        LaborCultural.nombre.label("nombre"),
        func.sum(func.coalesce(LaborCultural.precio_hora_estimado, 0)).label("costo_total"),
        func.sum(func.coalesce(Task.tiempo_hora, 0)).label("total_horas")  # Asegurar que total_horas no sea None
    ).join(Task, Task.labor_cultural_id == LaborCultural.id)\
    .group_by(LaborCultural.nombre).all()


def get_estimated_machinery_costs_from_controller(db: Session):
    return db.query(
        Machinery.name.label("nombre"),
        func.coalesce(func.sum(Machinery.estimatedCostPerHour), 0).label("costo_total"),  # Usamos COALESCE para evitar None
        func.coalesce(func.sum(Machinery.estimatedCostPerHour), 0).label("total_horas")  # Aseguramos que total_horas no sea None
    ).group_by(Machinery.name).all()



def get_estimated_agricultural_input_costs(db: Session):
    return db.query(
        AgriculturalInput.nombre.label("nombre"),
        func.coalesce(func.sum(AgriculturalInput.cantidad * AgriculturalInput.precio_unitario_estimado), 0).label("costo_total"),
        func.coalesce(func.sum(AgriculturalInput.cantidad), 0).label("total_cantidad")
    ).group_by(AgriculturalInput.nombre).all()

