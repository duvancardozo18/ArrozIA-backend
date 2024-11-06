from fastapi import APIRouter, File, Form, UploadFile

from src.controller.predictionController import predict_image

PREDICTION_ROUTES = APIRouter()

@PREDICTION_ROUTES.post("/predict")
async def predict(file: UploadFile = File(...), cultivo_id: int = Form(...)):
    # Leer la imagen del archivo cargado
    image_data = await file.read()
    
    # Llamar a la función de predicción en el controlador
    predicted_class = predict_image(image_data, cultivo_id)
    return {"prediction": predicted_class}
