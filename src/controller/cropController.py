import re
import traceback
from src.models.farmModel import Farm
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from src.models.cropModel import Crop
from src.schemas.cropSchema import CropCreate, CropUpdate
from src.models.landModel import Land
from src.models.varietyArrozModel import VarietyArrozModel

# Función para generar el slug
def generate_slug(name: str) -> str:
    return name.lower().replace(" ", "-")

def createCrop(crop: CropCreate, db: Session):
    try:
        slug = generate_slug(crop.cropName)

        db_crop = Crop(
            cropName=crop.cropName,
            varietyId=crop.varietyId,
            plotId=crop.plotId,
            plantingDate=crop.plantingDate,
            estimatedHarvestDate=crop.estimatedHarvestDate,
            slug=slug  # Asigna el slug generado desde el backend
        )
        print(f"Datos que se van a insertar: {db_crop.__dict__}")
        db.add(db_crop)
        db.commit()
        db.refresh(db_crop)

        # Obtener la variedad y el lote para la respuesta
        variety = db.query(VarietyArrozModel).filter_by(id=db_crop.varietyId).first()
        lote = db.query(Land).filter_by(id=db_crop.plotId).first()
        
        # Verificar si se obtuvo un lote y variedad válidos
        if not variety or not lote:
            raise HTTPException(status_code=404, detail="Variety or Plot not found")
        
        # Obtener la finca asociada al lote
        finca = db.query(Farm).filter_by(id=lote.finca_id).first()
        if not finca:
            raise HTTPException(status_code=404, detail="Finca not found")

        # Retornar los datos junto con los slugs y otros campos
        return {
            "id": db_crop.id,
            "cropName": db_crop.cropName,
            "varietyId": db_crop.varietyId,
            "varietyName": variety.nombre,
            "plotId": db_crop.plotId,
            "plotName": lote.nombre,
            "plantingDate": db_crop.plantingDate,
            "estimatedHarvestDate": db_crop.estimatedHarvestDate,
            "cropslug": db_crop.slug,
            "slug": db_crop.slug,  # Devuelve el slug del cultivo
            "plotSlug": lote.slug,  # Devuelve el slug del lote
            "fincaSlug": finca.slug  # Devuelve el slug de la finca
        }

    except Exception as e:
        print(f"Error al crear el cultivo: {e}")
        traceback.print_exc()  # Imprime el traceback del error
        raise HTTPException(status_code=500, detail="Error inesperado al crear el cultivo")

def getCrop(cropId: int, db: Session):
    try:
        # Cargar el cultivo con su variedad asociada
        crop = (
            db.query(Crop)
            .options(joinedload(Crop.variety))
            .filter(Crop.id == cropId)
            .first()
        )
        if not crop:
            raise HTTPException(status_code=404, detail="Crop not found")

        # Validar si la variedad está presente
        if not crop.variety:
            raise HTTPException(status_code=404, detail="Variety not found")

        return {
            "id": crop.id,
            "cropName": crop.cropName,
            "varietyId": crop.variety.id,
            "varietyName": crop.variety.nombre,
            "plotId": crop.plotId,
            "plantingDate": crop.plantingDate,
            "estimatedHarvestDate": crop.estimatedHarvestDate,
            "slug": crop.slug
        }
    except Exception as e:
        print(f"Error al obtener el cultivo: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener el cultivo")

def getAllCrops(db: Session):
    try:
        # Cargar todos los cultivos con su variedad asociada
        crops = db.query(Crop).options(joinedload(Crop.variety)).all()
        return [
            {
                "id": crop.id,
                "cropName": crop.cropName,
                "varietyId": crop.variety.id if crop.variety else None,
                "varietyName": crop.variety.nombre if crop.variety else None,
                "plotId": crop.plotId,
                "plantingDate": crop.plantingDate,
                "estimatedHarvestDate": crop.estimatedHarvestDate,
                "slug": crop.slug
            }
            for crop in crops
        ]
    except Exception as e:
        print(f"Error al obtener todos los cultivos: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener la lista de cultivos")

def getCropsByLand(land_id: int, db: Session):
    try:
        # Obtener los cultivos asociados al lote (land_id) con sus relaciones
        crops = (
            db.query(Crop)
            .options(joinedload(Crop.variety))
            .filter(Crop.plotId == land_id)
            .all()
        )

        return [
            {
                "id": crop.id,
                "cropName": crop.cropName,
                "varietyId": crop.variety.id if crop.variety else None,
                "varietyName": crop.variety.nombre if crop.variety else None,
                "plotId": crop.plotId,
                "plantingDate": crop.plantingDate,
                "estimatedHarvestDate": crop.estimatedHarvestDate,
                "slug": crop.slug
            }
            for crop in crops
        ]
    except Exception as e:
        print(f"Error al obtener los cultivos por land_id: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener los cultivos")

def updateCrop(cropId: int, cropUpdate: CropUpdate, db: Session):
    try:
        crop = db.query(Crop).filter(Crop.id == cropId).first()
        if not crop:
            raise HTTPException(status_code=404, detail="Crop not found")
        
        for key, value in cropUpdate.dict(exclude_unset=True).items():
            setattr(crop, key, value)
        
        db.commit()
        db.refresh(crop)
        return crop
    except Exception as e:
        print(f"Error al actualizar el cultivo: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar el cultivo")

def deleteCrop(cropId: int, db: Session):
    try:
        crop = db.query(Crop).filter(Crop.id == cropId).first()
        if not crop:
            raise HTTPException(status_code=404, detail="Crop not found")
        
        db.delete(crop)
        db.commit()
        return {"message": "Crop deleted successfully"}
    except Exception as e:
        print(f"Error al eliminar el cultivo: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar el cultivo")

def getCropInfo(finca_slug: str, lote_slug: str, cultivo_slug: str, db: Session):
    try:
        # Buscar la finca por slug
        finca = db.query(Farm).filter(Farm.slug == finca_slug).first()
        if not finca:
            raise HTTPException(status_code=404, detail="Finca not found")

        # Buscar el lote por slug y finca
        lote = db.query(Land).filter(Land.slug == lote_slug, Land.finca_id == finca.id).first()
        if not lote:
            raise HTTPException(status_code=404, detail="Lote not found")

        # Buscar el cultivo por slug y lote
        cultivo = db.query(Crop).filter(Crop.plotId == lote.id, Crop.slug == cultivo_slug).first()
        if not cultivo:
            raise HTTPException(status_code=404, detail="Cultivo not found")

        # Buscar la variedad de arroz asociada
        variedad = db.query(VarietyArrozModel).filter(VarietyArrozModel.id == cultivo.varietyId).first()
        if not variedad:
            raise HTTPException(status_code=404, detail="Variedad de arroz not found")

        # Retornar los datos
        return {
            "id": cultivo.id,
            "cropName": cultivo.cropName,
            "cropSlug": cultivo.slug,
            "varietyId": variedad.id,
            "varietyName": variedad.nombre,
            "plotId": lote.id,
            "plotName": lote.nombre,
            "plotSlug": lote.slug,
            "fincaSlug": finca.slug,
            "plantingDate": cultivo.plantingDate,
            "estimatedHarvestDate": cultivo.estimatedHarvestDate
        }
    except Exception as e:
        print(f"Error al obtener la información del cultivo: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener la información del cultivo")
