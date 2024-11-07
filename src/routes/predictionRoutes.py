from fastapi import APIRouter, File, Form, UploadFile, Depends

from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.controller.predictionController import predict_image,get_diagnostics_by_cultivo, get_diagnostic_detail
from src.schemas.phytosanitaryDiagnosisSchema import DiagnosticoFitosanitarioOut
from datetime import date

PREDICTION_ROUTES = APIRouter()

@PREDICTION_ROUTES.post("/predict")
async def predict(file: UploadFile = File(...), cultivo_id: int = Form(...)):
    # Validación adicional para `cultivo_id`
    if not isinstance(cultivo_id, int) or cultivo_id <= 0:
        raise HTTPException(status_code=400, detail="El `cultivo_id` debe ser un número entero positivo válido.")
    
    # Leer la imagen del archivo cargado
    image_data = await file.read()
    
    # Llamar a la función de predicción en el controlador
    predicted_class = predict_image(image_data, cultivo_id)
    return {"prediction": predicted_class}


@PREDICTION_ROUTES.get("/diagnostics/history/{cultivo_id}", response_model=List[DiagnosticoFitosanitarioOut])
def read_diagnostics_history(cultivo_id: int, start_date: date = None, end_date: date = None, db: Session = Depends(get_db)):
    return get_diagnostics_by_cultivo(db, cultivo_id, start_date, end_date)

@PREDICTION_ROUTES.get("/diagnostics/detail/{id}", response_model=DiagnosticoFitosanitarioOut)
def read_diagnostic_detail(id: int, db: Session = Depends(get_db)):
    return get_diagnostic_detail(db, id)