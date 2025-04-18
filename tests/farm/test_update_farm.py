import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.farmModel import Farm
from src.models.cropModel import Crop
from src.models.soilAnalysisModel import SoilAnalysisModel
from src.models.weatherRecordModel import WeatherRecord
from src.models.varietyArrozModel import VarietyArrozModel
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
from src.schemas.farmSchema import UpdateFarmSchema
from src.controller.farmCrontroller import updateFarm

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    session.commit = MagicMock()
    session.refresh = MagicMock()
    return session

@pytest.fixture
def sample_farm(mock_session):
    MagicMock(spec=Crop)
    MagicMock(spec=SoilAnalysisModel)
    MagicMock(spec=WeatherRecord)
    MagicMock(spec=VarietyArrozModel)
    MagicMock(spec=VarietyRiceStageModel)
    MagicMock(spec=Task)
    MagicMock(spec=Monitoring)
    MagicMock(spec=AgriculturalInput)
    MagicMock(spec=Harvest)
    MagicMock(spec=Costs)
    MagicMock(spec=PhenologicalStage)
    MagicMock(spec=LaborCultural)
    MagicMock(spec=User)
    MagicMock(spec=Machinery)
    MagicMock(spec=Estado)
    MagicMock(spec=OpMech)

    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    """Crea una finca de ejemplo para pruebas"""
    return Farm(
        id=1,
        nombre="Finca Las Palmas",
        ubicacion="Valle Central",
        area_total=120.5,
        latitud=4.5709,
        longitud=-74.2973,
        slug="finca-las-palmas",
        ciudad="Bogotá",
        departamento="Cundinamarca",
        pais="Colombia"
    )

@pytest.fixture
def valid_update_data():
    """Crea datos válidos para actualizar una finca"""
    return UpdateFarmSchema(
        nombre="Finca El Paraíso",
        ubicacion="Montaña",
        area_total=200.0,
        latitud=4.6123,
        longitud=-74.1234,
        ciudad="Medellín",
        departamento="Antioquia",
        pais="Colombia"
    )

def test_update_farm_success(mock_session, sample_farm, valid_update_data):
    """Prueba la actualización exitosa de una finca"""
    # Configurar el comportamiento del mock
    mock_session.query.return_value.filter.return_value.first.return_value = sample_farm
    
    # Ejecutar la función
    result = updateFarm(1, valid_update_data, mock_session)
    
    # Verificaciones
    assert mock_session.commit.called
    assert mock_session.refresh.called
    assert "msg" in result
    assert "finca" in result
    assert result["msg"] == "Finca actualizada satisfactoriamente"
    assert sample_farm.nombre == valid_update_data.nombre
    assert sample_farm.ubicacion == valid_update_data.ubicacion
    assert sample_farm.area_total == valid_update_data.area_total

def test_update_farm_not_found(mock_session, valid_update_data):
    """Prueba la actualización de una finca cuando el ID no existe"""
    # Configurar el comportamiento del mock para devolver None
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateFarm(999, valid_update_data, mock_session)
    
    # Verificaciones
    assert excinfo.value.status_code == 404
    assert "Finca con id 999 no encontrada" in excinfo.value.detail
    assert not mock_session.commit.called
    assert not mock_session.refresh.called

def test_update_farm_partial(mock_session, sample_farm):
    """Prueba la actualización parcial de una finca"""
    # Crear datos de actualización con solo algunos campos
    partial_update = UpdateFarmSchema(
        nombre="Finca Renovada",
        ubicacion=None,  # No actualizar ubicación
        area_total=None,  # No actualizar área
        latitud=None,
        longitud=None,
        ciudad=None,
        departamento=None,
        pais=None
    )
    
    # Guardar valores originales para comparar
    original_ubicacion = sample_farm.ubicacion
    original_area = sample_farm.area_total
    
    # Configurar el comportamiento del mock
    mock_session.query.return_value.filter.return_value.first.return_value = sample_farm
    
    # Ejecutar la función
    result = updateFarm(1, partial_update, mock_session)
    
    # Verificaciones
    assert sample_farm.nombre == "Finca Renovada"  # Debe actualizarse
    assert sample_farm.ubicacion == original_ubicacion  # No debe cambiar
    assert sample_farm.area_total == original_area  # No debe cambiar
    assert mock_session.commit.called
    assert mock_session.refresh.called

def test_update_farm_invalid_location(mock_session, sample_farm):
    """Prueba la validación de ubicación con caracteres especiales"""
    # Crear datos de actualización con ubicación inválida
    invalid_update = UpdateFarmSchema(
        nombre=None,
        ubicacion="Valle123!@#",  # Ubicación con caracteres no alfabéticos
        area_total=None,
        latitud=None,
        longitud=None,
        ciudad=None,
        departamento=None,
        pais=None
    )
    
    # Configurar el comportamiento del mock
    mock_session.query.return_value.filter.return_value.first.return_value = sample_farm
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateFarm(1, invalid_update, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Location must only contain letters" in excinfo.value.detail
    assert not mock_session.commit.called
    assert not mock_session.refresh.called

def test_update_farm_name_too_long(mock_session, sample_farm):
    """Prueba la validación de longitud del nombre"""
    # Crear datos de actualización con nombre muy largo
    invalid_update = UpdateFarmSchema(
        nombre="A" * 51,  # Nombre con más de 50 caracteres
        ubicacion=None,
        area_total=None,
        latitud=None,
        longitud=None,
        ciudad=None,
        departamento=None,
        pais=None
    )
    
    # Configurar el comportamiento del mock
    mock_session.query.return_value.filter.return_value.first.return_value = sample_farm
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateFarm(1, invalid_update, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Farm name must be at most 50 characters" in excinfo.value.detail
    assert not mock_session.commit.called
    assert not mock_session.refresh.called

if __name__ == "__main__":
    pytest.main()