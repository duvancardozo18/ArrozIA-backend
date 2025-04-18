import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.models.userModel import User
from src.models.authModel import TokenTable
from src.schemas.authShema import LoginRequest
from src.controller.authController import login, logout

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
    user.password = "hashed_password"  # Esto será diferente en las pruebas reales
    user.primer_login = False
    return user

@pytest.fixture
def valid_login_request():
    """Crea una solicitud de inicio de sesión válida"""
    return LoginRequest(
        email="juanperez@example.com",
        password="Password123"
    )

@patch('src.controller.authController.verify_password')
@patch('src.controller.authController.create_access_token')
@patch('src.controller.authController.create_refresh_token')
def test_login_success(mock_create_refresh_token, mock_create_access_token, 
                      mock_verify_password, mock_session, mock_user, valid_login_request):
    """Prueba un inicio de sesión exitoso"""
    # Configurar mocks
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "test_access_token"
    mock_create_refresh_token.return_value = "test_refresh_token"
    
    # Ejecutar la función
    result = login(valid_login_request, mock_session)
    
    # Verificaciones
    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called
    
    assert result["access_token"] == "test_access_token"
    assert result["refresh_token"] == "test_refresh_token"
    
    # Verificar que se llamó a las funciones de verificación y creación de tokens
    mock_verify_password.assert_called_once_with(valid_login_request.password, mock_user.password)
    mock_create_access_token.assert_called_once_with(subject=mock_user.id)
    mock_create_refresh_token.assert_called_once_with(subject=mock_user.id)

@patch('src.controller.authController.verify_password')
@patch('src.controller.authController.create_access_token')
@patch('src.controller.authController.create_refresh_token')
def test_login_first_time(mock_create_refresh_token, mock_create_access_token, 
                         mock_verify_password, mock_session, mock_user, valid_login_request):
    """Prueba un primer inicio de sesión (necesita cambio de contraseña)"""
    # Configurar mocks
    mock_user.primer_login = True
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "test_access_token"
    mock_create_refresh_token.return_value = "test_refresh_token"
    
    # Ejecutar la función
    result = login(valid_login_request, mock_session)
    
    # Verificar que es una instancia de JSONResponse con código 403
    assert isinstance(result, JSONResponse)
    assert result.status_code == 403
    
    # Verificar el contenido de la respuesta
    content = result.body.decode()
    assert "You need to change your password" in content
    assert "change_password_required" in content
    assert "access_token" in content
    assert "refresh_token" in content
    
    # Verificar que no se guardó ningún token en la base de datos
    assert not mock_session.add.called

def test_login_user_not_found(mock_session, valid_login_request):
    """Prueba el caso en que no se encuentra el usuario por email"""
    # Configurar el mock de la sesión para devolver None cuando se filtra por email
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        login(valid_login_request, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Incorrect email" in excinfo.value.detail

@patch('src.controller.authController.verify_password')
def test_login_incorrect_password(mock_verify_password, mock_session, mock_user, valid_login_request):
    """Prueba el caso de contraseña incorrecta"""
    # Configurar mocks
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    mock_verify_password.return_value = False  # Contraseña incorrecta
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        login(valid_login_request, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Incorrect password" in excinfo.value.detail

def test_login_invalid_email_format(mock_session):
    """Prueba validación de formato de email"""
    # Email sin @
    invalid_login = LoginRequest(
        email="juanperezexample.com",
        password="Password123"
    )
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        login(invalid_login, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Invalid email format" in excinfo.value.detail

def test_login_invalid_password_format(mock_session):
    """Prueba validación de formato de contraseña"""
    # Contraseña simple
    weak_login = LoginRequest(
        email="juanperez@example.com",
        password="simple"
    )
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        login(weak_login, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Password must be at least 8 characters" in excinfo.value.detail

def test_logout_success(mock_session):
    """Prueba un cierre de sesión exitoso"""
    # Crear un token mock
    token = MagicMock(spec=TokenTable)
    token.status = True
    
    # Configurar el mock de la sesión para devolver el token
    mock_session.query.return_value.filter.return_value.first.return_value = token
    
    # Ejecutar la función
    result = logout(1, mock_session)
    
    # Verificaciones
    assert token.status == False  # Se actualizó el estado del token
    assert mock_session.commit.called
    
    # Verificar la respuesta
    assert isinstance(result, JSONResponse)
    assert result.status_code == 200
    content = result.body.decode()
    assert "Successfully logged out" in content

def test_logout_not_found(mock_session):
    """Prueba el caso en que no se encuentra un token activo para cerrar sesión"""
    # Configurar el mock de la sesión para devolver None
    mock_session.query