import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.userModel import User
from src.controller.userController import getUsers, getUser

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
    return session

@pytest.fixture
def mock_users():
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

    """Crea una lista de usuarios mock"""
    user1 = MagicMock(spec=User)
    user1.id = 1
    user1.nombre = "Juan"
    user1.apellido = "Perez"
    user1.email = "juanperez@example.com"
    
    user2 = MagicMock(spec=User)
    user2.id = 2
    user2.nombre = "Maria"
    user2.apellido = "Lopez"
    user2.email = "marialopez@example.com"
    
    return [user1, user2]

@patch('src.controller.userController.get_current_user')
def test_get_users_success(mock_get_current_user, mock_session, mock_users):
    """Prueba la obtención exitosa de todos los usuarios"""
    # Configurar el mock de la sesión para devolver la lista de usuarios
    mock_session.query.return_value.all.return_value = mock_users
    
    # Configurar el mock para el usuario actual
    current_user = MagicMock(spec=User)
    current_user.id = 1
    mock_get_current_user.return_value = current_user
    
    # Ejecutar la función
    result = getUsers(mock_session, current_user)
    
    # Verificaciones
    assert result == mock_users
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2

def test_get_user_by_id_success(mock_session, mock_users):
    """Prueba la obtención exitosa de un usuario por ID"""
    # Configurar el mock de la sesión para devolver el usuario cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = mock_users[0]
    
    # Ejecutar la función
    result = getUser(1, mock_session)
    
    # Verificaciones
    assert result == mock_users[0]
    assert result.id == 1
    assert result.nombre == "Juan"
    assert result.apellido == "Perez"
    assert result.email == "juanperez@example.com"

def test_get_user_by_id_not_found(mock_session):
    """Prueba el caso en que no se encuentra un usuario por ID"""
    # Configurar el mock de la sesión para devolver None cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        getUser(999, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "User not found" in excinfo.value.detail

@patch('src.controller.userController.get_current_user')
def test_get_users_empty_list(mock_get_current_user, mock_session):
    """Prueba el caso en que no hay usuarios en la base de datos"""
    # Configurar el mock de la sesión para devolver una lista vacía
    mock_session.query.return_value.all.return_value = []
    
    # Configurar el mock para el usuario actual
    current_user = MagicMock(spec=User)
    current_user.id = 1
    mock_get_current_user.return_value = current_user
    
    # Ejecutar la función
    result = getUsers(mock_session, current_user)
    
    # Verificaciones
    assert result == []
    assert len(result) == 0

if __name__ == "__main__":
    pytest.main()