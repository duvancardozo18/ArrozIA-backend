from sqlalchemy import Column, Integer, String, Date, ForeignKey, LargeBinary, DECIMAL
from sqlalchemy.orm import relationship
from src.database.database import Base

class SoilAnalysisModel(Base):
    __tablename__ = 'analisis_edafologico'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lote_id = Column(Integer, ForeignKey('lote.id'), nullable=False)
    tipo_suelo_id = Column(Integer, ForeignKey("tipo_suelo.id"), nullable=False)
    fecha_analisis = Column(Date, nullable=False)
    archivo_reporte = Column(LargeBinary, nullable=True)

    biological_params = relationship("BiologicalParamModel", uselist=False, back_populates="soil_analysis")
    chemical_params = relationship("ChemicalParamModel", uselist=False, back_populates="soil_analysis")
    physical_params = relationship("PhysicalParamModel", uselist=False, back_populates="soil_analysis")



    soil_type = relationship("SoilTypeModel", back_populates="soil_analyses")
    lote = relationship("Land", back_populates="soil_analysis") 

# Model for the `tipo_suelo` table
class SoilTypeModel(Base):
    __tablename__ = 'tipo_suelo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)

    # Relationship
    soil_analyses = relationship("SoilAnalysisModel", back_populates="soil_type")


# Model for the `parametro_biologico` table
class BiologicalParamModel(Base):
    __tablename__ = 'parametro_biologico'

    id = Column(Integer, primary_key=True, autoincrement=True)
    analisis_edafologico_id = Column(Integer, ForeignKey("analisis_edafologico.id"), nullable=False)
    biomasa_microbiana = Column(DECIMAL(10, 2), nullable=True)
    actividad_enzimatica = Column(DECIMAL(10, 2), nullable=True)

    # Relationship
    soil_analysis = relationship("SoilAnalysisModel", back_populates="biological_params")

# Model for the `parametro_quimico` table
class ChemicalParamModel(Base):
    __tablename__ = 'parametro_quimico'

    id = Column(Integer, primary_key=True, autoincrement=True)
    analisis_edafologico_id = Column(Integer, ForeignKey("analisis_edafologico.id"), nullable=False)
    ph = Column(DECIMAL(4, 2), nullable=True)
    conductividad_electrica = Column(DECIMAL(10, 2), nullable=True)
    materia_organica = Column(DECIMAL(10, 2), nullable=True)
    capacidad_intercambio_cationico = Column(DECIMAL(10, 2), nullable=True)

    # Relationships
    macronutrients = relationship("MacronutrientModel", back_populates="chemical_param")
    micronutrients = relationship("MicronutrientModel", back_populates="chemical_param")
    soil_analysis = relationship("SoilAnalysisModel", back_populates="chemical_params")


# Model for the `parametro_fisico` table
class PhysicalParamModel(Base):
    __tablename__ = 'parametro_fisico'

    id = Column(Integer, primary_key=True, autoincrement=True)
    analisis_edafologico_id = Column(Integer, ForeignKey("analisis_edafologico.id"), nullable=False)
    textura_id = Column(Integer, ForeignKey("textura.id"), nullable=False)
    color_id = Column(Integer, ForeignKey("color.id"), nullable=False)
    densidad_aparente = Column(DECIMAL(10, 2), nullable=True)
    profundidad_efectiva = Column(DECIMAL(10, 2), nullable=True)

    # Relationships
    soil_analysis = relationship("SoilAnalysisModel", back_populates="physical_params")
    texture = relationship("TextureModel", back_populates="physical_params")
    color = relationship("ColorModel", back_populates="physical_params")


# Model for the `macronutriente` table
class MacronutrientModel(Base):
    __tablename__ = 'macronutriente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parametro_quimico_id = Column(Integer, ForeignKey("parametro_quimico.id"), nullable=False)
    n = Column(DECIMAL(10, 2), nullable=True)
    p = Column(DECIMAL(10, 2), nullable=True)
    k = Column(DECIMAL(10, 2), nullable=True)
    ca = Column(DECIMAL(10, 2), nullable=True)
    mg = Column(DECIMAL(10, 2), nullable=True)
    s = Column(DECIMAL(10, 2), nullable=True)

    # Relationship
    chemical_param = relationship("ChemicalParamModel", back_populates="macronutrients")


# Model for the `micronutriente` table
class MicronutrientModel(Base):
    __tablename__ = 'micronutriente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parametro_quimico_id = Column(Integer, ForeignKey("parametro_quimico.id"), nullable=False)
    fe = Column(DECIMAL(10, 2), nullable=True)
    cu = Column(DECIMAL(10, 2), nullable=True)
    mn = Column(DECIMAL(10, 2), nullable=True)
    zn = Column(DECIMAL(10, 2), nullable=True)
    b = Column(DECIMAL(10, 2), nullable=True)

    # Relationship
    chemical_param = relationship("ChemicalParamModel", back_populates="micronutrients")


# Model for the `textura` table
class TextureModel(Base):
    __tablename__ = 'textura'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)

    # Relationship
    physical_params = relationship("PhysicalParamModel", back_populates="texture")


# Model for the `color` table
class ColorModel(Base):
    __tablename__ = 'color'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)

    # Relationship
    physical_params = relationship("PhysicalParamModel", back_populates="color")
