import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
import datetime

from src.models.cropModel import Crop
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
from src.controller.cropController import deleteCrop

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    session.commit = MagicMock()
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
    return crop

def test_delete_crop_success(mock_session, mock_crop):
    """Prueba la eliminación exitosa de un cultivo"""
    # Configurar el mock de la sesión para devolver el cultivo cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = mock_crop
    
    # Ejecutar la función
    result = deleteCrop(1, mock_session)
    
    # Verificaciones
    mock_session.delete.assert_called_once_with(mock_crop)
    assert mock_session.commit.called
    assert result["message"] == "Crop deleted successfully"

def test_delete_crop_not_found(mock_session):
    """Prueba el caso en que no se encuentra el cultivo para eliminar"""
    # Configurar el mock de la sesión para devolver None cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        deleteCrop(999, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Crop not found" in excinfo.value.detail
    
    # Verificar que no se llamó a delete ni commit
    assert not mock_session.delete.called
    assert not mock_session.commit.called

def test_delete_crop_database_error(mock_session, mock_crop):
    """Prueba el manejo de errores de base de datos durante la eliminación"""
    # Configurar el mock de la sesión para devolver el cultivo pero lanzar una excepción al eliminar
    mock_session.query.return_value.filter.return_value.first.return_value = mock_crop
    mock_session.commit.side_effect = Exception("Database error")
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        deleteCrop(1, mock_session)
    
    assert excinfo.value.status_code == 500
    assert "Error al eliminar el cultivo" in excinfo.value.detail

def test_delete_crop_with_invalid_id(mock_session):
    """Prueba la eliminación con un ID inválido (por ejemplo, None o no numérico)"""
    # Configuramos el mock para que lance una excepción si se intenta filtrar con un ID inválido
    mock_session.query.return_value.filter.side_effect = Exception("Invalid ID type")
    
    # Verificar que se maneja correctamente la excepción
    with pytest.raises(HTTPException) as excinfo:
        deleteCrop(None, mock_session)
    
    assert excinfo.value.status_code == 500
    assert "Error al eliminar el cultivo" in excinfo.value.detail

if __name__ == "__main__":
    pytest.main()