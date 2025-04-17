# test_get_all_farms.py
import fastapi
import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.farmModel import Farm
from src.controller.farmCrontroller import getAllFarms, getFarmById
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

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    return session

@pytest.fixture
def sample_farm():
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

def test_get_all_farms_success(mock_session):
    """Prueba la obtención exitosa de todas las fincas"""

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

    # Crear datos simulados de fincas
    farm1 = Farm(
        id=1,
        nombre="Finca Las Palmas",
        ubicacion="Valle Central",
        area_total=120.5,
        latitud=4.5709,
        longitud=-74.2973,
        ciudad="Bogotá",
        departamento="Cundinamarca",
        pais="Colombia"
    )
    
    farm2 = Farm(
        id=2,
        nombre="Finca El Paraíso",
        ubicacion="Montaña",
        area_total=200.0,
        latitud=4.6123,
        longitud=-74.1234,
        ciudad="Medellín",
        departamento="Antioquia",
        pais="Colombia"
    )
    
    # Configurar el comportamiento del mock
    mock_session.query.return_value.all.return_value = [farm1, farm2]
    
    # Ejecutar la función
    result = getAllFarms(mock_session)
    
    # Verificaciones
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["nombre"] == "Finca Las Palmas"
    assert result[1]["id"] == 2
    assert result[1]["nombre"] == "Finca El Paraíso"
    mock_session.query.assert_called_once_with(Farm)

def test_get_all_farms_empty(mock_session):
    """Prueba la obtención de fincas cuando no hay fincas registradas"""
    # Configurar el comportamiento del mock para devolver lista vacía
    mock_session.query.return_value.all.return_value = []
    
    # Ejecutar la función
    result = getAllFarms(mock_session)
    
    # Verificaciones
    assert isinstance(result, list)
    assert len(result) == 0
    mock_session.query.assert_called_once_with(Farm)

def test_get_all_farms_null_fields(mock_session):
    """Prueba la obtención de fincas con campos nulos"""
    # Crear datos simulados de fincas con campos nulos
    farm_with_nulls = Farm(
        id=3,
        nombre="Finca Incompleta",
        ubicacion=None,  # Campo nulo
        area_total=None,  # Campo nulo
        latitud=4.5000,
        longitud=-74.5000,
        ciudad="Cali",
        departamento="Valle del Cauca",
        pais="Colombia"
    )
    
    # Configurar el comportamiento del mock
    mock_session.query.return_value.all.return_value = [farm_with_nulls]
    
    # Ejecutar la función
    result = getAllFarms(mock_session)
    
    # Verificaciones
    assert len(result) == 1
    assert result[0]["id"] == 3
    assert result[0]["nombre"] == "Finca Incompleta"
    assert result[0]["ubicacion"] == ""  # Debe convertir None a string vacío
    assert result[0]["area_total"] == 0.0  # Debe convertir None a 0.0

def test_get_farm_by_id_success(mock_session, sample_farm):
    """Prueba la obtención exitosa de una finca por ID"""
    # Configurar el comportamiento del mock
    mock_session.query.return_value.filter.return_value.first.return_value = sample_farm
    
    # Ejecutar la función
    result = getFarmById(1, mock_session)
    
    # Verificaciones
    assert result.id == 1
    assert result.nombre == "Finca Las Palmas"
    assert result.ubicacion == "Valle Central"
    mock_session.query.assert_called_once_with(Farm)
    mock_session.query.return_value.filter.assert_called_once()

def test_get_farm_by_id_not_found(mock_session):
    """Prueba la obtención de una finca cuando el ID no existe"""
    # Configurar el comportamiento del mock para devolver None
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        getFarmById(999, mock_session)
    
    # Verificaciones
    assert excinfo.value.status_code == 404
    assert "Finca con id 999 no encontrada" in excinfo.value.detail
    mock_session.query.assert_called_once_with(Farm)
    mock_session.query.return_value.filter.assert_called_once()

if __name__ == "__main__":
    pytest.main()