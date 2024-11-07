from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from src.models.landModel import Land
from src.models.soilAnalysisModel import (
    SoilAnalysisModel, BiologicalParamModel, ChemicalParamModel,
    PhysicalParamModel, MacronutrientModel, MicronutrientModel, SoilTypeModel,
    TextureModel, ColorModel
)
from src.schemas.soilAnalysisSchema import SoilAnalysisCreate, SoilAnalysisOut, BiologicalParamOut, ChemicalParamOut, PhysicalParamOut, SoilAnalysisSimpleOut

def create_soil_analysis(
    soil_data: SoilAnalysisCreate,
    db: Session,
    archivo_reporte: UploadFile = None
) -> SoilAnalysisSimpleOut:
    # Validar que los campos obligatorios estén presentes
    if soil_data.parametro_quimico and soil_data.parametro_quimico.ph is None:
        raise HTTPException(status_code=400, detail="El campo 'ph' en 'parametro_quimico' es obligatorio.")
    
    # Validar que el lote especificado en la solicitud existe
    lote_existente = db.query(Land).filter(Land.id == soil_data.lote_id).first()
    if not lote_existente:
        raise HTTPException(status_code=400, detail="El lote especificado no existe.")

    # Validar que el tipo de suelo especificado en soil_data existe
    soil_type_existente = db.query(SoilTypeModel).filter(SoilTypeModel.id == soil_data.tipo_suelo_id).first()
    if not soil_type_existente:
        raise HTTPException(status_code=400, detail="El tipo de suelo especificado no existe.")

# def create_soil_analysis(
#     soil_data: SoilAnalysisCreate,
#     db: Session,
#     archivo_reporte: UploadFile = None
# ) -> SoilAnalysisSimpleOut:
#     # Buscar lote por nombre
#     lote_existente = db.query(Land).filter(Land.nombre == soil_data.lote_nombre).first()
#     if not lote_existente:
#         raise HTTPException(status_code=400, detail="El lote especificado no existe.")
    
#     # Asigna el lote_id encontrado
#     soil_data.lote_id = lote_existente.id
    
#     # Validar que el tipo de suelo especificado en soil_data existe
#     soil_type_existente = db.query(SoilTypeModel).filter(SoilTypeModel.id == soil_data.tipo_suelo_id).first()
#     if not soil_type_existente:
#         raise HTTPException(status_code=400, detail="El tipo de suelo especificado no existe.")

    # Validar que textura_id especificado en soil_data existe si se proporciona
    if soil_data.parametro_fisico and soil_data.parametro_fisico.textura_id is not None:
        textura_existente = db.query(TextureModel).filter(TextureModel.id == soil_data.parametro_fisico.textura_id).first()
        if not textura_existente:
            raise HTTPException(status_code=400, detail="La textura especificada no existe.")

    # Validar que color_id especificado en soil_data existe si se proporciona
    if soil_data.parametro_fisico and soil_data.parametro_fisico.color_id is not None:
        color_existente = db.query(ColorModel).filter(ColorModel.id == soil_data.parametro_fisico.color_id).first()
        if not color_existente:
            raise HTTPException(status_code=400, detail="El color especificado no existe.")

    # Crear el análisis principal de suelo
    soil_data_excluded = soil_data.dict(exclude={
        "parametro_biologico", "parametro_quimico", "parametro_fisico"
    })
    soil_analysis = SoilAnalysisModel(**soil_data_excluded)
    db.add(soil_analysis)
    db.commit()
    db.refresh(soil_analysis)

    # Insertar parámetros biológicos, químicos y físicos
    if soil_data.parametro_biologico:
        bio_params = BiologicalParamModel(
            analisis_edafologico_id=soil_analysis.id,
            **soil_data.parametro_biologico.dict(exclude_unset=True)
        )
        db.add(bio_params)
    if soil_data.parametro_quimico:
        chem_params = ChemicalParamModel(
            analisis_edafologico_id=soil_analysis.id,
            **soil_data.parametro_quimico.dict(exclude={"macronutriente", "micronutriente"}, exclude_unset=True)
        )
        db.add(chem_params)
        db.flush()

        # Agregar macronutrientes y micronutrientes
        if soil_data.parametro_quimico.macronutriente:
            for macro in soil_data.parametro_quimico.macronutriente:
                new_macronutrient = MacronutrientModel(
                    parametro_quimico_id=chem_params.id,
                    **macro.dict(exclude_unset=True)
                )
                db.add(new_macronutrient)

        if soil_data.parametro_quimico.micronutriente:
            for micro in soil_data.parametro_quimico.micronutriente:
                new_micronutrient = MicronutrientModel(
                    parametro_quimico_id=chem_params.id,
                    **micro.dict(exclude_unset=True)
                )
                db.add(new_micronutrient)

    if soil_data.parametro_fisico:
        phys_params = PhysicalParamModel(
            analisis_edafologico_id=soil_analysis.id,
            **soil_data.parametro_fisico.dict(exclude_unset=True)
        )
        db.add(phys_params)

    db.commit()

    # Crear y devolver la respuesta simplificada
    response_data = SoilAnalysisSimpleOut(
        id=soil_analysis.id,
        message=f"Análisis de suelo creado exitosamente con el id: {soil_analysis.id}"
    )

    return response_data

def get_analyses_by_lote(lote_id: int, db: Session):
    # Obtener el lote completo (id y nombre)
    lote = db.query(Land).filter(Land.id == lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="El lote especificado no existe.")
    
    # Obtener todos los análisis del lote junto con el tipo de suelo y parámetros anidados
    analyses = db.query(SoilAnalysisModel).options(
        joinedload(SoilAnalysisModel.soil_type),
        joinedload(SoilAnalysisModel.chemical_params)
    ).filter(SoilAnalysisModel.lote_id == lote_id).all()
    
    # Formatear la respuesta para incluir los campos adicionales o devolver lista vacía si no hay análisis
    formatted_analyses = [
        {
            "id": analysis.id,
            "tipo_suelo_id": analysis.tipo_suelo_id,
            "tipo_suelo_descripcion": analysis.soil_type.descripcion if analysis.soil_type else None,
            "fecha_analisis": analysis.fecha_analisis.strftime("%Y-%m-%d") if analysis.fecha_analisis else None,
            "ph": analysis.chemical_params.ph if analysis.chemical_params else None,
            "materia_organica": analysis.chemical_params.materia_organica if analysis.chemical_params else None
        }
        for analysis in analyses
    ]
    
    return {"lote_id": lote.id, "lote_name": lote.nombre, "analyses": formatted_analyses}

# def get_analyses_by_lote(lote_nombre: str, db: Session):
#     # Obtener el lote completo (id y nombre) usando el nombre
#     lote_nombre = str(lote_nombre)
#     lote = db.query(Land).filter(Land.nombre == lote_nombre).first()
#     if not lote:
#         raise HTTPException(status_code=404, detail="El lote especificado no existe.")
    
#     # Obtener todos los análisis del lote
#     analyses = db.query(SoilAnalysisModel).options(
#         joinedload(SoilAnalysisModel.soil_type),
#         joinedload(SoilAnalysisModel.chemical_params)
#     ).filter(SoilAnalysisModel.lote_id == lote.id).all()
    
#     formatted_analyses = [
#         {
#             "id": analysis.id,
#             "tipo_suelo_id": analysis.tipo_suelo_id,
#             "tipo_suelo_descripcion": analysis.soil_type.descripcion if analysis.soil_type else None,
#             "fecha_analisis": analysis.fecha_analisis.strftime("%Y-%m-%d") if analysis.fecha_analisis else None,
#             "ph": analysis.chemical_params.ph if analysis.chemical_params else None,
#             "materia_organica": analysis.chemical_params.materia_organica if analysis.chemical_params else None
#         }
#         for analysis in analyses
#     ]
    
#     return {"lote_name": lote.nombre, "analyses": formatted_analyses}

def get_analysis_detail(lote_id: int, analysis_id: int, db: Session): 
    analysis = db.query(SoilAnalysisModel).options(
        joinedload(SoilAnalysisModel.soil_type),
        joinedload(SoilAnalysisModel.lote),
        joinedload(SoilAnalysisModel.biological_params),
        joinedload(SoilAnalysisModel.chemical_params).joinedload(ChemicalParamModel.macronutrients),
        joinedload(SoilAnalysisModel.chemical_params).joinedload(ChemicalParamModel.micronutrients),
        joinedload(SoilAnalysisModel.physical_params).joinedload(PhysicalParamModel.texture),
        joinedload(SoilAnalysisModel.physical_params).joinedload(PhysicalParamModel.color)
    ).filter_by(id=analysis_id, lote_id=lote_id).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Análisis no encontrado para el lote especificado.")

# def get_analysis_detail(lote_nombre: str, analysis_id: int, db: Session): 
#     lote = db.query(Land).filter(Land.nombre == lote_nombre).first()
#     if not lote:
#         raise HTTPException(status_code=404, detail="El lote especificado no existe.")
    
#     analysis = db.query(SoilAnalysisModel).options(
#         joinedload(SoilAnalysisModel.soil_type),
#         joinedload(SoilAnalysisModel.lote),
#         joinedload(SoilAnalysisModel.biological_params),
#         joinedload(SoilAnalysisModel.chemical_params).joinedload(ChemicalParamModel.macronutrients),
#         joinedload(SoilAnalysisModel.chemical_params).joinedload(ChemicalParamModel.micronutrients),
#         joinedload(SoilAnalysisModel.physical_params).joinedload(PhysicalParamModel.texture),
#         joinedload(SoilAnalysisModel.physical_params).joinedload(PhysicalParamModel.color)
#     ).filter_by(id=analysis_id, lote_id=lote.id).first()
    
#     if not analysis:
#         raise HTTPException(status_code=404, detail="Análisis no encontrado para el lote especificado.")

    result = {
        "id": analysis.id,
        "fecha_analisis": analysis.fecha_analisis.strftime("%Y-%m-%d") if analysis.fecha_analisis else None,
        "soil_type": {
            "id": analysis.soil_type.id,
            "descripcion": analysis.soil_type.descripcion
        } if analysis.soil_type else None,
        "lote": {
            "id": analysis.lote.id,
            "nombre": analysis.lote.nombre
        } if analysis.lote else None,
        "archivo_reporte": analysis.archivo_reporte,
        "parametro_biologico": {
            "biomasa_microbiana": analysis.biological_params.biomasa_microbiana,
            "actividad_enzimatica": analysis.biological_params.actividad_enzimatica
        } if analysis.biological_params else None,
        "parametro_quimico": {
            "ph": analysis.chemical_params.ph,
            "conductividad_electrica": analysis.chemical_params.conductividad_electrica,
            "materia_organica": analysis.chemical_params.materia_organica,
            "capacidad_intercambio_cationico": analysis.chemical_params.capacidad_intercambio_cationico,
            "macronutriente": [
                {
                    "n": macronutrient.n,
                    "p": macronutrient.p,
                    "k": macronutrient.k,
                    "ca": macronutrient.ca,
                    "mg": macronutrient.mg,
                    "s": macronutrient.s
                } for macronutrient in analysis.chemical_params.macronutrients
            ] if analysis.chemical_params.macronutrients else None,
            "micronutriente": [
                {
                    "fe": micronutrient.fe,
                    "cu": micronutrient.cu,
                    "mn": micronutrient.mn,
                    "zn": micronutrient.zn,
                    "b": micronutrient.b
                } for micronutrient in analysis.chemical_params.micronutrients
            ] if analysis.chemical_params.micronutrients else None,
        } if analysis.chemical_params else None,
        "parametro_fisico": {
            "textura_id": analysis.physical_params.textura_id,
            "textura_descripcion": analysis.physical_params.texture.descripcion if analysis.physical_params and analysis.physical_params.texture else None,
            "densidad_aparente": analysis.physical_params.densidad_aparente,
            "profundidad_efectiva": analysis.physical_params.profundidad_efectiva,
            "color_id": analysis.physical_params.color_id,
            "color_descripcion": analysis.physical_params.color.descripcion if analysis.physical_params and analysis.physical_params.color else None
        } if analysis.physical_params else None,
    }

    return result

def update_soil_analysis(lote_id: int, analysis_id: int, soil_data: SoilAnalysisCreate, db: Session):
    # Validar que el lote actual especificado en la solicitud existe
    lote_existente = db.query(Land).filter(Land.id == lote_id).first()
    if not lote_existente:
        raise HTTPException(status_code=400, detail="El lote especificado para la actualización no existe.")
    
    # Validar que el nuevo lote especificado en soil_data existe si se proporciona un cambio de lote
    if soil_data.lote_id is not None and soil_data.lote_id != lote_id:
        nuevo_lote_existente = db.query(Land).filter(Land.id == soil_data.lote_id).first()
        if not nuevo_lote_existente:
            raise HTTPException(status_code=400, detail="El nuevo lote especificado no existe.")

    # Validar que el tipo de suelo especificado en soil_data existe si se proporciona
    if soil_data.tipo_suelo_id is not None:
        soil_type_existente = db.query(SoilTypeModel).filter(SoilTypeModel.id == soil_data.tipo_suelo_id).first()
        if not soil_type_existente:
            raise HTTPException(status_code=400, detail="El tipo de suelo especificado no existe.")

    # Validar que textura_id especificado en soil_data existe si se proporciona
    if soil_data.parametro_fisico and soil_data.parametro_fisico.textura_id is not None:
        textura_existente = db.query(TextureModel).filter(TextureModel.id == soil_data.parametro_fisico.textura_id).first()
        if not textura_existente:
            raise HTTPException(status_code=400, detail="La textura especificado no existe en la base de datos.")

    # Validar que color_id especificado en soil_data existe si se proporciona
    if soil_data.parametro_fisico and soil_data.parametro_fisico.color_id is not None:
        color_existente = db.query(ColorModel).filter(ColorModel.id == soil_data.parametro_fisico.color_id).first()
        if not color_existente:
            raise HTTPException(status_code=400, detail="El color especificado no existe en la base de datos.")

    # Buscar el análisis y verificar que esté vinculado al lote
    analysis = db.query(SoilAnalysisModel).filter_by(id=analysis_id, lote_id=lote_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="El análisis no fue encontrado para el lote especificado.")

    # Realizar la actualización de campos
    for key, value in soil_data.dict(exclude_unset=True).items():
        setattr(analysis, key, value)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar el análisis debido a restricciones de integridad.")
    
    return {"message": "Análisis actualizado exitosamente"}

def delete_soil_analysis(lote_id: int, analysis_id: int, db: Session):
    # Buscar el análisis de suelo junto con sus relaciones dependientes
    analysis = db.query(SoilAnalysisModel).options(
        joinedload(SoilAnalysisModel.biological_params),
        joinedload(SoilAnalysisModel.chemical_params),
        joinedload(SoilAnalysisModel.physical_params)
    ).filter_by(id=analysis_id, lote_id=lote_id).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")

    # Eliminar registros dependientes
    if analysis.biological_params:
        db.delete(analysis.biological_params)
    if analysis.chemical_params:
        # Eliminar macronutrientes y micronutrientes relacionados con parametros químicos
        for macro in analysis.chemical_params.macronutrients:
            db.delete(macro)
        for micro in analysis.chemical_params.micronutrients:
            db.delete(micro)
        db.delete(analysis.chemical_params)
    if analysis.physical_params:
        db.delete(analysis.physical_params)

    # Eliminar el análisis de suelo principal
    db.delete(analysis)
    db.commit()
    
    return {"message": "Análisis y parámetros relacionados eliminados correctamente"}

# Example function to get soil types
def get_soil_types(db: Session):
    soil_types = db.query(SoilTypeModel).all()
    print("Fetched soil types from database:", soil_types)  # Log data
    return soil_types

def get_textures(db: Session):
    # Directly query the TextureModel table
    textures = db.query(TextureModel).all()
    print("Fetched textures:", textures)
    return textures

def get_colors(db: Session):
    # Directly query the ColorModel table
    colors = db.query(ColorModel).all()
    print("Fetched colors:", colors)
    return colors
