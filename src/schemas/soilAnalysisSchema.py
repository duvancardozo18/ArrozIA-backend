from typing import Optional, List
from pydantic import BaseModel, root_validator
from datetime import date

# Biological Parameter Output
class BiologicalParamOut(BaseModel):
    biomasa_microbiana: Optional[float] = None
    actividad_enzimatica: Optional[float] = None

    model_config = {
        "from_attributes": True
    }

# Soil Type Output with id
class SoilTypeOut(BaseModel):
    id: int
    descripcion: str

    model_config = {
        "from_attributes": True
    }

# Land Output with id
class LandOut(BaseModel):
    id: int
    nombre: str

    model_config = {
        "from_attributes": True
    }

# Macronutrient Output
class MacronutrientOut(BaseModel):
    n: Optional[float] = None
    p: Optional[float] = None
    k: Optional[float] = None
    ca: Optional[float] = None
    mg: Optional[float] = None
    s: Optional[float] = None

    model_config = {
        "from_attributes": True
    }

# Micronutrient Output
class MicronutrientOut(BaseModel):
    fe: Optional[float] = None
    cu: Optional[float] = None
    mn: Optional[float] = None
    zn: Optional[float] = None
    b: Optional[float] = None

    model_config = {
        "from_attributes": True
    }

# Chemical Parameter Output
class ChemicalParamOut(BaseModel):
    ph: Optional[float] = None
    conductividad_electrica: Optional[float] = None
    materia_organica: Optional[float] = None
    capacidad_intercambio_cationico: Optional[float] = None
    macronutriente: Optional[List[MacronutrientOut]] = None
    micronutriente: Optional[List[MicronutrientOut]] = None

    model_config = {
        "from_attributes": True
    }

# Physical Parameter Output with additional fields for texture and color descriptions
class PhysicalParamOut(BaseModel):
    textura_id: Optional[int] = None
    textura_descripcion: Optional[str] = None
    densidad_aparente: Optional[float] = None
    profundidad_efectiva: Optional[float] = None
    color_id: Optional[int] = None
    color_descripcion: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class SoilAnalysisCreate(BaseModel):
    lote_id: int
    fecha_analisis: str
    tipo_suelo_id: int
    archivo_reporte: Optional[str] = None
    parametro_biologico: Optional[BiologicalParamOut] = None
    parametro_quimico: Optional[ChemicalParamOut] = None
    parametro_fisico: Optional[PhysicalParamOut] = None

    model_config = {
        "from_attributes": True
    }

# Soil Analysis Output with id and detailed fields
class SoilAnalysisOut(BaseModel):
    id: int
    fecha_analisis: str
    soil_type: Optional[SoilTypeOut] = None
    lote: Optional[LandOut] = None
    archivo_reporte: Optional[str] = None
    parametro_biologico: Optional[BiologicalParamOut] = None
    parametro_quimico: Optional[ChemicalParamOut] = None
    parametro_fisico: Optional[PhysicalParamOut] = None

    model_config = {
        "from_attributes": True
    }

    @root_validator(pre=True)
    def format_fecha_analisis(cls, values):
        # Intentar obtener `fecha_analisis` del objeto directamente
        fecha_analisis = getattr(values, "fecha_analisis", None)
        
        # Si `fecha_analisis` es de tipo `date`, formatearlo
        if isinstance(fecha_analisis, date):
            values.fecha_analisis = fecha_analisis.strftime("%Y-%m-%d")
        return values

class SoilAnalysisSimpleOut(BaseModel):
    id: int
    message: str

    model_config = {
        "from_attributes": True
    }
