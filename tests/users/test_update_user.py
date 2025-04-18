import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.userModel import User
from src.schemas.userShema import UpdateUser
from src.controller.userController import updateUser

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
    session.refresh = MagicMock()
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
    user.password = "hashedPassword123"
    user.primer_login = True
    return user

@pytest.fixture
def valid_update_data():
    """Crea datos válidos para actualizar un usuario"""
    return UpdateUser(
        nombre="Juan Carlos",
        apellido="Perez Gomez",
        email="jcperez@example.com",
        password="NewPassword123",
        primer_login=False
    )

def test_update_user_success(mock_session, mock_user, valid_update_data):
    """Prueba la actualización exitosa de un usuario"""
    # Configurar el mock de la sesión para devolver el usuario cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Ejecutar la función
    result = updateUser(1, valid_update_data, mock_session)
    
    # Verificaciones
    assert mock_session.commit.called
    assert mock_session.refresh.called
    
    # Verificar que los atributos se hayan actualizado correctamente
    assert mock_user.nombre == "Juan Carlos"
    assert mock_user.apellido == "Perez Gomez"
    assert mock_user.email == "jcperez@example.com"
    # No verificamos la contraseña directamente porque se hashea
    assert mock_user.primer_login == False
    
    # Verificar la respuesta
    assert result["message"] == "User updated successfully"
    assert result["user"] == mock_user

def test_update_user_partial(mock_session, mock_user):
    """Prueba la actualización parcial de un usuario"""
    # Crear datos de actualización parcial
    partial_update = UpdateUser(nombre="Juan Carlos")
    
    # Configurar el mock de la sesión
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Ejecutar la función
    result = updateUser(1, partial_update, mock_session)
    
    # Verificaciones
    assert mock_session.commit.called
    assert mock_session.refresh.called
    
    # Verificar que solo se actualizó el nombre
    assert mock_user.nombre == "Juan Carlos"
    assert mock_user.apellido == "Perez"  # No cambia
    assert mock_user.email == "juanperez@example.com"  # No cambia
    assert mock_user.primer_login == True  # No cambia

def test_update_user_not_found(mock_session, valid_update_data):
    """Prueba el caso en que no se encuentra el usuario para actualizar"""
    # Configurar el mock de la sesión para devolver None cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateUser(999, valid_update_data, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "User not found" in excinfo.value.detail
    
    # Verificar que no se llamó a commit ni refresh
    assert not mock_session.commit.called
    assert not mock_session.refresh.called

def test_update_user_invalid_name(mock_session, mock_user):
    """Prueba validación de formato de nombre"""
    # Nombre con números
    invalid_name = UpdateUser(nombre="Juan123")
    
    # Configurar el mock de la sesión
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateUser(1, invalid_name, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Name must only contain letters" in excinfo.value.detail

def test_update_user_invalid_lastname(mock_session, mock_user):
    """Prueba validación de formato de apellido"""
    # Apellido con caracteres especiales
    invalid_lastname = UpdateUser(apellido="Perez@123")
    
    # Configurar el mock de la sesión
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateUser(1, invalid_lastname, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Last name must only contain letters" in excinfo.value.detail

def test_update_user_invalid_email_format(mock_session, mock_user):
    """Prueba validación de formato de email"""
    # Email sin @
    invalid_email = UpdateUser(email="juanperezexample.com")
    
    # Configurar el mock de la sesión
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateUser(1, invalid_email, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Email must contain '@'" in excinfo.value.detail

def test_update_user_password_complexity(mock_session, mock_user):
    """Prueba validación de complejidad de contraseña"""
    # Contraseña simple
    weak_password = UpdateUser(password="simple")
    
    # Configurar el mock de la sesión
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateUser(1, weak_password, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Password must be at least 8 characters" in excinfo.value.detail

def test_update_user_with_long_fields(mock_session, mock_user):
    """Prueba validación de longitud de campos"""
    # Nombre muy largo
    long_name = UpdateUser(nombre="A" * 51)  # 51 caracteres
    
    # Configurar el mock de la sesión
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateUser(1, long_name, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Name must be at most 50 characters" in excinfo.value.detail

if __name__ == "__main__":
    pytest.main()