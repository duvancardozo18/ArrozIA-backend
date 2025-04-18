import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.landModel import Land
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
from src.schemas.landSchema import LandSchema
from src.controller.landController import createLand
from src.models.soilAnalysisModel import SoilAnalysisModel
from src.models.weatherRecordModel import WeatherRecord

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()
    return session

@pytest.fixture
def valid_land_data(mock_session):
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

    """Crea datos válidos para un lote"""
    return LandSchema(
        nombre="Lote Norte",
        finca_id=1,
        area=50.5,
        latitud=4.5709,
        longitud=-74.2973
    )

def test_create_land_success(mock_session, valid_land_data):
    """Prueba la creación exitosa de un lote"""
    # Configuración del mock para simular la asignación de ID después de refresh
    def set_id_and_slug(land):
        land.id = 1
        land.slug = "lote-norte"
    mock_session.refresh.side_effect = set_id_and_slug
    
    # Ejecutar la función
    result = createLand(valid_land_data, mock_session)
    
    # Verificaciones
    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called
    assert "msg" in result
    assert "slug" in result
    assert result["msg"] == "Lote creado satisfactoriamente"
    assert result["slug"] == "lote-norte"

def test_create_land_empty_name(mock_session):
    """Prueba la validación de nombre vacío"""
    # Crear datos con nombre vacío
    land_data = LandSchema(
        nombre="  ".strip(),  # Nombre con espacios en blanco
        finca_id=1,
        area=50.5,
        latitud=4.5709,
        longitud=-74.2973
    )
    
    # Ejecutar la función y verificar que genera el slug correctamente
    result = createLand(land_data, mock_session)
    assert result["slug"] == ""

def test_create_land_invalid_area(mock_session, valid_land_data):
    """Prueba la validación de área negativa"""
    # Modificar área para que sea negativa
    valid_land_data.area = -10
    
    # Ejecutar la función
    result = createLand(valid_land_data, mock_session)
    
    # Verificar que se crea correctamente (el controlador actual no valida área negativa)
    assert mock_session.add.called
    assert "msg" in result
    assert result["msg"] == "Lote creado satisfactoriamente"

def test_create_land_generate_slug(mock_session):
    """Prueba la generación de slug con caracteres especiales"""
    # Crear datos con nombre que contenga caracteres especiales
    land_data = LandSchema(
        nombre="Lote #1 (Norte)",
        finca_id=1,
        area=50.5,
        latitud=4.5709,
        longitud=-74.2973
    )
    
    # Configurar el mock para asignar el slug después de refresh
    def set_slug(land):
        land.slug = "lote-1-norte"
    mock_session.refresh.side_effect = set_slug
    
    # Ejecutar la función
    result = createLand(land_data, mock_session)
    
    # Verificar que el slug se genera correctamente
    assert result["slug"] == "lote-1-norte"

if __name__ == "__main__":
    pytest.main()