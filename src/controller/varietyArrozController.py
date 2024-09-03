from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models.varietyArrozModel import VariedadArroz
from src.schemas.varietyArrozSchema import VariedadArrozCreate

#Crear variedad de arroz
def createVariety(varietyData: VariedadArrozCreate, db: Session):
    try:
        newVariety = VariedadArroz(**varietyData.dict())
        db.add(newVariety)
        db.commit()
        db.refresh(newVariety)
        return newVariety
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error creating variety: " + str(e))


#Modificar variedad de arroz 
def getVariety(varietyId: int, db: Session):
    try:
        variety = db.query(VariedadArroz).filter(VariedadArroz.id == varietyId).first()
        if not variety:
            raise HTTPException(status_code=404, detail="Variety not found")
        return variety
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error retrieving variety: " + str(e))


#lista de variedad arroz
def listVarieties(db: Session):
    try:
        varieties = db.query(VariedadArroz).all()
        return varieties
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error listing varieties: " + str(e))

def updateVariety(varietyId: int, updatedData: VariedadArrozCreate, db: Session):
    try:
        variety = db.query(VariedadArroz).filter(VariedadArroz.id == varietyId).first()
        if not variety:
            raise HTTPException(status_code=404, detail="Variety not found")
        
        for key, value in updatedData.dict().items():
            setattr(variety, key, value)
        
        db.commit()
        db.refresh(variety)
        return variety
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error updating variety: " + str(e))


#Eliminar variedad de arroz 
def deleteVariety(varietyId: int, db: Session):
    try:
        variety = db.query(VariedadArroz).filter(VariedadArroz.id == varietyId).first()
        if not variety:
            raise HTTPException(status_code=404, detail="Variety not found")
        
        db.delete(variety)
        db.commit()
        return {"message": "Variety deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error deleting variety: " + str(e))
