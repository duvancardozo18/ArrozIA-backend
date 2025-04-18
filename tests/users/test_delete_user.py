import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.userModel import User
from src.controller.userController import deleteUser

from src.models.taskModel import Task
from src.models.cropModel import Crop
from src.models.agriculturalInputModel import AgriculturalInput
from src.models.laborCulturalModel import LaborCultural
from src.models.machineryModel import Machinery
from src.models.estadoModel import Estado
from src.models.farmModel import Farm
from src.models.soilAnalysisModel import SoilAnalysisModel
from src.models.weatherRecordModel import WeatherRecord
from src.models.varietyRiceStageModel import VarietyRiceStageModel
from src.models.monitoringModel import Monitoring
from src.models.harvestModel import Harvest
from src.models.costsModel import Costs
from src.models.opMechModel import OpMech

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    session.commit = MagicMock()
    return session

@pytest.fixture
def mock_user():
    MagicMock(spec=Task)
    MagicMock(spec=Crop)
    MagicMock(spec=AgriculturalInput)
    MagicMock(spec=LaborCultural)
    MagicMock(spec=Machinery)
    MagicMock(spec=Estado)
    MagicMock(spec=Farm)
    MagicMock(spec=SoilAnalysisModel)
    MagicMock(spec=WeatherRecord)
    MagicMock(spec=VarietyRiceStageModel)
    MagicMock(spec=Monitoring)
    MagicMock(spec=Harvest)
    MagicMock(spec=Costs)
    MagicMock(spec=OpMech)
    
    """Crea un mock para un usuario existente"""
    user = MagicMock(spec=User)
    user.id = 1
    user.nombre = "Juan"
    user.apellido = "Perez"
    user.email = "juanperez@example.com"
    return user

def test_delete_user_success(mock_session, mock_user):
    """Prueba la eliminación exitosa de un usuario"""
    # Configurar el mock de la sesión para devolver el usuario cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Ejecutar la función
    result = deleteUser(1, mock_session)
    
    # Verificaciones
    mock_session.delete.assert_called_once_with(mock_user)
    assert mock_session.commit.called
    
    # Verificar la respuesta
    assert result["message"] == "User deleted successfully"
    assert result["status"] == status.HTTP_200_OK

def test_delete_user_not_found(mock_session):
    """Prueba el caso en que no se encuentra el usuario para eliminar"""
    # Configurar el mock de la sesión para devolver None cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        deleteUser(999, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "User not found" in excinfo.value.detail
    
    # Verificar que no se llamó a delete ni commit
    assert not mock_session.delete.called
    assert not mock_session.commit.called

def test_delete_user_database_error(mock_session, mock_user):
    """Prueba el manejo de errores de base de datos durante la eliminación"""
    # Configurar el mock de la sesión para devolver el usuario pero lanzar una excepción al eliminar
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    mock_session.commit.side_effect = Exception("Database error")
    
    # Verificar que se maneja correctamente la excepción
    with pytest.raises(Exception) as excinfo:
        deleteUser(1, mock_session)
    
    assert str(excinfo.value) == "Database error"
    
    # Verificar que se llamó a delete pero la excepción ocurrió en commit
    mock_session.delete.assert_called_once_with(mock_user)
    assert mock_session.commit.called

if __name__ == "__main__":
    pytest.main()