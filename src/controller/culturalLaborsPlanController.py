from fastapi import HTTPException
from datetime import timedelta

# Diccionario básico de labores culturales
CULTURAL_LABORS = {
    "soil_preparation": {"duration": 5, "description": "Preparación del suelo", "equipment": "Tractor", "input": "Fertilizante A"},
    "planting": {"duration": 3, "description": "Siembra del cultivo", "equipment": "Sembradora", "input": "Semilla B"},
    "irrigation": {"duration": 10, "description": "Riego programado", "equipment": "Sistema de riego", "input": "Agua"},
    "fertilization": {"duration": 7, "description": "Aplicación de fertilizantes", "equipment": "Aspersor", "input": "Fertilizante C"},
    "pest_control": {"duration": 5, "description": "Control de plagas", "equipment": "Pulverizador", "input": "Insecticida"},
    "harvest": {"duration": 10, "description": "Cosecha del cultivo", "equipment": "Cosechadora", "input": "N/A"}
}

def plan_cultural_labors(sowing_date, existing_plan=None):
    try:
        labors_plan = []
        current_date = sowing_date
        
        if existing_plan:
            # Si se recibe un plan existente, recalculamos las fechas
            for labor in existing_plan:
                labor_end = current_date + timedelta(days=labor['duration'])
                labors_plan.append({
                    "labor": labor['labor'],
                    "description": labor['description'],
                    "start_date": current_date,
                    "end_date": labor_end,
                    "equipment": labor['equipment'],
                    "input": labor['input']
                })
                current_date = labor_end
        else:
            # Si no hay plan existente, generamos uno nuevo
            for labor, details in CULTURAL_LABORS.items():
                labor_end = current_date + timedelta(days=details['duration'])
                labors_plan.append({
                    "labor": labor,
                    "description": details["description"],
                    "start_date": current_date,
                    "end_date": labor_end,
                    "equipment": details["equipment"],
                    "input": details["input"]
                })
                current_date = labor_end
        
        return labors_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating cultural labors plan: {str(e)}")

# Función para agregar una labor manualmente
def add_cultural_labor(labor, duration, description, equipment, input, sowing_date):
    try:
        new_labor_end = sowing_date + timedelta(days=duration)
        return {
            "labor": labor,
            "description": description,
            "start_date": sowing_date,
            "end_date": new_labor_end,
            "equipment": equipment,
            "input": input
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding cultural labor: {str(e)}")

# Función para modificar una labor en el plan existente
def modify_cultural_labor(labor_name, new_duration, new_description, new_equipment, new_input, plan):
    try:
        for labor in plan:
            if labor['labor'] == labor_name:
                labor['duration'] = new_duration
                labor['description'] = new_description
                labor['equipment'] = new_equipment
                labor['input'] = new_input
                return labor  # Retornamos la labor modificada
        raise HTTPException(status_code=404, detail="Labor not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error modifying cultural labor: {str(e)}")

# Función para eliminar una labor en el plan
def delete_cultural_labor(labor_name, plan):
    try:
        for labor in plan:
            if labor['labor'] == labor_name:
                plan.remove(labor)  # Eliminamos la labor del plan
                return {"message": f"Labor '{labor_name}' deleted successfully"}
        raise HTTPException(status_code=404, detail="Labor not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting cultural labor: {str(e)}")
