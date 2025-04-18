import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
import datetime

from src.models.cropModel import Crop
from src.schemas.cropSchema import CropUpdate
from src.models.farmModel import Farm
from src.models.landModel import Land
from src.models.varietyArrozModel import VarietyArrozModel
from src.schemas.cropSchema import CropCreate
from src.controller.cropController import createCrop
from src.models.soilAnalysisModel import SoilAnalysisModel
from src.models.weatherRecordModel import WeatherRecord
from src.models.varietyRiceStageModel import VarietyRiceStageModel
from src.models.taskModel import Task
from src.models.monitoringModel import Monitoring
from src.models.agriculturalInputModel import AgriculturalInput
from src.models.harvestModel import Harvest
from src.models.costsModel import Costs
from src.models.phenologicalStageModel import PhenologicalStage
from src.models.laborCulturalModel import LaborCultural
from src.models.userModel import User
from src.models.machineryModel import Machinery
from src.models.estadoModel import Estado
from src.models.opMechModel import OpMech
from src.controller.cropController import updateCrop

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    session.commit = MagicMock()
    session.refresh = MagicMock()
    return session

@pytest.fixture
def mock_crop():
    MagicMock(spec=Land)
    MagicMock(spec=SoilAnalysisModel)
    MagicMock(spec=VarietyRiceStageModel)
    MagicMock(spec=Monitoring)
    MagicMock(spec=Task)
    MagicMock(spec=WeatherRecord)
    MagicMock(spec=VarietyArrozModel)
    MagicMock(spec=AgriculturalInput)
    MagicMock(spec=Harvest)
    MagicMock(spec=Costs)
    MagicMock(spec=PhenologicalStage)
    MagicMock(spec=LaborCultural)
    MagicMock(spec=User)
    MagicMock(spec=Machinery)
    MagicMock(spec=Estado)
    MagicMock(spec=OpMech)

    """Crea un mock para un cultivo existente"""
    crop = MagicMock(spec=Crop)
    crop.id = 1
    crop.cropName = "Arroz Premium"
    crop.varietyId = 1
    crop.plotId = 1
    crop.plantingDate = datetime.date.today()
    crop.estimatedHarvestDate = datetime.date.today().replace(month=datetime.date.today().month + 3)
    crop.slug = "arroz-premium"
    return crop

@pytest.fixture
def valid_update_data():
    """Crea datos válidos para actualizar un cultivo"""
    return CropUpdate(
        cropName="Arroz Premium Actualizado",
        varietyId=2,
        plotId=1,
        slug="nuevo-slug",
        estimatedHarvestDate=datetime.date.today() + datetime.timedelta(days=90)
    )

def test_update_crop_success(mock_session, mock_crop, valid_update_data):
    """Prueba la actualización exitosa de un cultivo"""
    # Configurar el mock de la sesión para devolver el cultivo cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = mock_crop
    
    # Ejecutar la función
    result = updateCrop(1, valid_update_data, mock_session)
    
    # Verificaciones
    assert mock_session.commit.called
    assert mock_session.refresh.called
    
    # Verificar que los atributos se hayan actualizado correctamente
    assert mock_crop.cropName == "Arroz Premium Actualizado"
    assert mock_crop.varietyId == 2
    assert mock_crop.slug == "nuevo-slug"
    # La fecha estimada de cosecha debería haberse actualizado

def test_update_crop_partial(mock_session, mock_crop):
    partial_update = CropUpdate(cropName="Parcial")
    
    # Mockear el comportamiento
    mock_session.query.return_value.filter.return_value.first.return_value = mock_crop
    
    result = updateCrop(1, partial_update, mock_session)
    
    assert mock_crop.cropName == "Parcial"
    assert mock_crop.varietyId == 1  # No cambia
    assert mock_session.commit.called

def test_update_crop_not_found(mock_session, valid_update_data):
    """Prueba el caso en que no se encuentra el cultivo para actualizar"""
    # Configurar el mock de la sesión para devolver None cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateCrop(999, valid_update_data, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Crop not found" in excinfo.value.detail
    
    # Verificar que no se llamó a commit ni refresh
    assert not mock_session.commit.called
    assert not mock_session.refresh.called

def test_update_crop_database_error(mock_session, mock_crop, valid_update_data):
    """Prueba el manejo de errores de base de datos durante la actualización"""
    # Configurar el mock de la sesión para lanzar una excepción al llamar a commit
    mock_session.query.return_value.filter.return_value.first.return_value = mock_crop
    mock_session.commit.side_effect = Exception("Database error")
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateCrop(1, valid_update_data, mock_session)
    
    assert excinfo.value.status_code == 500
    assert "Error al actualizar el cultivo" in excinfo.value.detail

def test_update_crop_empty_values(mock_session, mock_crop):
    """Prueba la actualización con valores vacíos o None"""
    # Crear datos de actualización con algunos valores vacíos
    empty_update = CropUpdate(cropName="", varietyId=None)
    
    # Configurar el mock de la sesión
    mock_session.query.return_value.filter.return_value.first.return_value = mock_crop
    
    # Ejecutar la función
    result = updateCrop(1, empty_update, mock_session)
    
    # Verificaciones
    assert mock_session.commit.called
    assert mock_session.refresh.called
    
    # Verificar que los atributos se hayan actualizado según lo esperado
    assert mock_crop.cropName == ""  # Se actualiza a cadena vacía
    
    # El varietyId debería conservar su valor original ya que se pasó None
    # Nota: Esto depende de cómo se implementa dict(exclude_unset=True), 
    # que excluye los campos no establecidos en el schema
    assert mock_crop.varietyId == 1  # No debería cambiar

if __name__ == "__main__":
    pytest.main()