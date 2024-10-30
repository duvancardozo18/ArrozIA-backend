from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from src.database.database import Base

class Task(Base):
    __tablename__ = "tarea_labor_cultural"

    id = Column(Integer, primary_key=True, index=True)
    fecha_estimada = Column(Date, nullable=False)
    fecha_realizacion = Column(Date, nullable=True)
    descripcion = Column(String, nullable=True)
    
    # Declaración de claves foráneas con carga diferida
    estado_id = Column(Integer, ForeignKey("estado.id", ondelete="CASCADE"), nullable=False)
    es_mecanizable = Column(Boolean, default=False)
    cultivo_id = Column(Integer, ForeignKey("cultivo.id", ondelete="CASCADE"), nullable=False)
    labor_cultural_id = Column(Integer, ForeignKey("labor_cultural.id", ondelete="CASCADE"), nullable=False)
    insumo_agricola_id = Column(Integer, ForeignKey("insumo_agricola.id", ondelete="SET NULL"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    tiempo_hora = Column(Integer, nullable=True)
    maquinaria_agricola_id = Column(Integer, ForeignKey("maquinaria_agricola.id", ondelete="SET NULL"), nullable=True)
