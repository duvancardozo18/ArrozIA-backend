import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.farmModel import Farm
from src.schemas.farmSchema import FarmSchema
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

from src.controller.farmCrontroller import createFarm

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()
    return session

@pytest.fixture
def valid_farm_data():
    """Crea datos válidos para una finca"""
    return FarmSchema(
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

def test_create_farm_success(mock_session, valid_farm_data):
    """Prueba la creación exitosa de una finca"""
    # Configuración del mock para simular la asignación de ID después de refresh
    def set_id(farm):
        farm.id = 1
    mock_session.refresh.side_effect = set_id

    # Relaciones mockeadas
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
    
    
    # Ejecutar la función
    result = createFarm(valid_farm_data, mock_session)
    
    # Verificaciones
    assert mock_session.add.call_count >= 1
    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called
    assert "msg" in result
    assert "finca" in result
    assert result["msg"] == "Finca creada satisfactoriamente"
    assert result["finca"].nombre == valid_farm_data.nombre
    assert result["finca"].ubicacion == valid_farm_data.ubicacion
    assert result["finca"].area_total == valid_farm_data.area_total

def test_create_farm_empty_name(mock_session):
    """Prueba la validación de nombre vacío"""
    # Crear datos con nombre vacío
    farm_data = FarmSchema(
        nombre="   ",  # Nombre con espacios en blanco
        ubicacion="Valle Central",
        area_total=120.5,
        latitud=4.5709,
        longitud=-74.2973,
        slug="finca-las-palmas",
        ciudad="Bogotá",
        departamento="Cundinamarca",
        pais="Colombia"
    )
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        createFarm(farm_data, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Farm name cannot be empty" in excinfo.value.detail

def test_create_farm_invalid_location(mock_session, valid_farm_data):
    """Prueba la validación de ubicación con caracteres especiales"""
    # Modificar ubicación para incluir caracteres no alfabéticos
    valid_farm_data.ubicacion = "Valle123!@#"
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        createFarm(valid_farm_data, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Farm location must only contain letters" in excinfo.value.detail

def test_create_farm_name_too_long(mock_session, valid_farm_data):
    """Prueba la validación de longitud del nombre"""
    # Crear nombre muy largo (más de 50 caracteres)
    valid_farm_data.nombre = "A" * 51
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        createFarm(valid_farm_data, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Farm name must be at most 50 characters" in excinfo.value.detail

def test_create_farm_location_too_long(mock_session, valid_farm_data):
    """Prueba la validación de longitud de la ubicación"""
    # Crear ubicación muy larga (más de 100 caracteres)
    valid_farm_data.ubicacion = "A" * 101
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        createFarm(valid_farm_data, mock_session)
    
    assert excinfo.value.status_code == 400
    assert "Location must be at most 100 characters" in excinfo.value.detail

if __name__ == "__main__":
    pytest.main()