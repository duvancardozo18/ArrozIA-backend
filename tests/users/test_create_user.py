import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.userModel import User
from src.schemas.userShema import CrearUsuario
from src.controller.userController import registerUser
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
def valid_user_data():
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

    """Crea datos válidos para un nuevo usuario"""
    return CrearUsuario(
        nombre="Juan",
        apellido="Perez",
        email="juanperez@example.com",
        password="Password123"
    )

def test_register_user_success(mock_session, valid_user_data):
    """Prueba el registro exitoso de un nuevo usuario"""
    # Configuramos el mock para que no encuentre usuarios existentes con el correo
    mock_session.query.return_value.filter_by.return_value.first.return_value = None
    
    # Crear un mock para el nuevo usuario
    new_user = MagicMock(spec=User)
    new_user.id = 1
    mock_session.refresh.side_effect = lambda x: setattr(x, 'id', 1) if isinstance(x, User) else None
    
    # Parcheamos la función add para capturar el usuario creado
    def mock_add(user):
        if isinstance(user, User):
            return new_user
    mock_session.add.side_effect = mock_add
    
    # Ejecutar la función
    result = registerUser(valid_user_data, mock_session)
    
    # Verificaciones
    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called
    assert result["message"] == "user created successfully"
    assert result["id"] == 1

def test_register_user_email_exists(mock_session, valid_user_data):
    """Prueba que no se pueda registrar un usuario con un correo ya existente"""
    # Configuramos el mock para que encuentre un usuario existente con el correo
    existing_user = MagicMock(spec=User)
    mock_session.query.return_value.filter_by.return_value.first.return_value = existing_user
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        registerUser(valid_user_data, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Email already registered" in excinfo.value.detail
    
    # Verificar que no se llamó a add, commit ni refresh
    assert not mock_session.add.called
    assert not mock_session.commit.called
    assert not mock_session.refresh.called

def test_register_user_empty_fields(mock_session):
    """Prueba validaciones de campos vacíos"""
    # Casos de prueba con campos vacíos
    cases = [
        (CrearUsuario(nombre="", apellido="Perez", email="jp@example.com", password="Password123"), "Name cannot be empty"),
        (CrearUsuario(nombre="Juan", apellido="", email="jp@example.com", password="Password123"), "Last name cannot be empty"),
        (CrearUsuario(nombre="Juan", apellido="Perez", email="", password="Password123"), "Email cannot be empty"),
        (CrearUsuario(nombre="Juan", apellido="Perez", email="jp@example.com", password=""), "Password cannot be empty")
    ]
    
    for user_data, expected_error in cases:
        with pytest.raises(HTTPException) as excinfo:
            registerUser(user_data, mock_session)
        
        assert excinfo.value.status_code == 400
        assert expected_error in excinfo.value.detail

def test_register_user_length_validations(mock_session):
    """Prueba validación de longitud de campos"""
    # Nombre muy largo
    long_name_user = CrearUsuario(
        nombre="A" * 51,  # 51 caracteres
        apellido="Perez",
        email="jp@example.com",
        password="Password123"
    )
    
    with pytest.raises(HTTPException) as excinfo:
        registerUser(long_name_user, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Name must be at most 50 characters" in excinfo.value.detail
    
    # Apellido muy largo
    long_lastname_user = CrearUsuario(
        nombre="Juan",
        apellido="P" * 51,  # 51 caracteres
        email="jp@example.com",
        password="Password123"
    )
    
    with pytest.raises(HTTPException) as excinfo:
        registerUser(long_lastname_user, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Last name must be at most 50 characters" in excinfo.value.detail

def test_register_user_email_format(mock_session):
    """Prueba validación de formato de email"""
    invalid_email_user = CrearUsuario(
        nombre="Juan",
        apellido="Perez",
        email="juanperezexample.com",  # Sin @
        password="Password123"
    )
    
    with pytest.raises(HTTPException) as excinfo:
        registerUser(invalid_email_user, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Invalid email format" in excinfo.value.detail

def test_register_user_password_complexity(mock_session):
    """Prueba validación de complejidad de contraseña"""
    # Contraseña sin mayúsculas
    weak_password1 = CrearUsuario(
        nombre="Juan",
        apellido="Perez",
        email="jp@example.com",
        password="password123"
    )
    
    with pytest.raises(HTTPException) as excinfo:
        registerUser(weak_password1, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Password must be at least 8 characters" in excinfo.value.detail
    
    # Contraseña sin números
    weak_password2 = CrearUsuario(
        nombre="Juan",
        apellido="Perez",
        email="jp@example.com",
        password="PasswordABC"
    )
    
    with pytest.raises(HTTPException) as excinfo:
        registerUser(weak_password2, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Password must be at least 8 characters" in excinfo.value.detail

def test_register_user_name_with_special_chars(mock_session):
    """Prueba validación de nombres y apellidos sin caracteres especiales"""
    user_with_special_chars = CrearUsuario(
        nombre="Juan123",
        apellido="Perez",
        email="jp@example.com",
        password="Password123"
    )
    
    with pytest.raises(HTTPException) as excinfo:
        registerUser(user_with_special_chars, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Name and last name must only contain letters" in excinfo.value.detail

if __name__ == "__main__":
    pytest.main()