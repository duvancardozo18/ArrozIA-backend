import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

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

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()
    return session

@pytest.fixture
def valid_crop_data():
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

    """Crea datos válidos para un cultivo"""
    return CropCreate(
        cropName="Arroz Premium",
        varietyId=1,
        plotId=1,
        plantingDate=datetime.now().date(),  # Usar .date()
        estimatedHarvestDate=(
            datetime.now().replace(month=datetime.now().month + 3)
        ).date() 
    )

@pytest.fixture
def mock_variety():
    """Crea un mock para la variedad de arroz"""
    variety = MagicMock(spec=VarietyArrozModel)
    variety.id = 1
    variety.nombre = "Variedad Premium"
    return variety

@pytest.fixture
def mock_land():
    """Crea un mock para el lote"""
    land = MagicMock(spec=Land)
    land.id = 1
    land.nombre = "Lote Norte"
    land.finca_id = 1
    land.slug = "lote-norte"
    return land

@pytest.fixture
def mock_farm():
    """Crea un mock para la finca"""
    farm = MagicMock(spec=Farm)
    farm.id = 1
    farm.nombre = "Finca Las Palmas"
    farm.slug = "finca-las-palmas"
    return farm

def test_create_crop_success(mock_session, valid_crop_data, mock_variety, mock_land, mock_farm):
    """Prueba la creación exitosa de un cultivo"""
    # Configuración del mock para simular la asignación de ID después de refresh
    def set_id_and_slug(crop):
        crop.id = 1
        crop.slug = "arroz-premium"
    mock_session.refresh.side_effect = set_id_and_slug
    
    # Configurar las consultas para los objetos relacionados
    def mock_query_side_effect(model):
        if model == VarietyArrozModel:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: mock_variety))
        elif model == Land:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: mock_land))
        elif model == Farm:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: mock_farm))
        return MagicMock()
    
    mock_session.query.side_effect = mock_query_side_effect
    
    # Ejecutar la función
    result = createCrop(valid_crop_data, mock_session)
    
    # Verificaciones
    assert mock_session.add.called
    assert mock_session.commit.called
    assert mock_session.refresh.called
    
    assert result["id"] == 1
    assert result["cropName"] == "Arroz Premium"
    assert result["varietyId"] == 1
    assert result["varietyName"] == "Variedad Premium"
    assert result["plotId"] == 1
    assert result["plotName"] == "Lote Norte"
    assert result["cropslug"] == "arroz-premium"
    assert result["slug"] == "arroz-premium"
    assert result["plotSlug"] == "lote-norte"
    assert result["fincaSlug"] == "finca-las-palmas"

def test_create_crop_variety_not_found(mock_session, valid_crop_data, mock_land, mock_farm):
    """Prueba la creación de un cultivo cuando no se encuentra la variedad"""
    # Configurar la asignación de ID después de refresh
    def set_id_and_slug(crop):
        crop.id = 1
        crop.slug = "arroz-premium"
    mock_session.refresh.side_effect = set_id_and_slug
    
    # Configurar las consultas para los objetos relacionados
    def mock_query_side_effect(model):
        if model == VarietyArrozModel:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: None))  # Variedad no encontrada
        elif model == Land:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: mock_land))
        elif model == Farm:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: mock_farm))
        return MagicMock()
    
    mock_session.query.side_effect = mock_query_side_effect
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        createCrop(valid_crop_data, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Variety or Plot not found" in excinfo.value.detail

def test_create_crop_land_not_found(mock_session, valid_crop_data, mock_variety, mock_farm):
    """Prueba la creación de un cultivo cuando no se encuentra el lote"""
    # Configurar la asignación de ID después de refresh
    def set_id_and_slug(crop):
        crop.id = 1
        crop.slug = "arroz-premium"
    mock_session.refresh.side_effect = set_id_and_slug
    
    # Configurar las consultas para los objetos relacionados
    def mock_query_side_effect(model):
        if model == VarietyArrozModel:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: mock_variety))
        elif model == Land:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: None))  # Lote no encontrado
        elif model == Farm:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: mock_farm))
        return MagicMock()
    
    mock_session.query.side_effect = mock_query_side_effect
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        createCrop(valid_crop_data, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Variety or Plot not found" in excinfo.value.detail

def test_create_crop_farm_not_found(mock_session, valid_crop_data, mock_variety, mock_land):
    """Prueba la creación de un cultivo cuando no se encuentra la finca"""
    # Configurar la asignación de ID después de refresh
    def set_id_and_slug(crop):
        crop.id = 1
        crop.slug = "arroz-premium"
    mock_session.refresh.side_effect = set_id_and_slug
    
    # Configurar las consultas para los objetos relacionados
    def mock_query_side_effect(model):
        if model == VarietyArrozModel:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: mock_variety))
        elif model == Land:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: mock_land))
        elif model == Farm:
            return MagicMock(filter_by=lambda **kwargs: MagicMock(first=lambda: None))  # Finca no encontrada
        return MagicMock()
    
    mock_session.query.side_effect = mock_query_side_effect
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        createCrop(valid_crop_data, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Finca not found" in excinfo.value.detail

def test_create_crop_database_error(mock_session, valid_crop_data):
    """Prueba el manejo de errores de base de datos durante la creación"""
    # Configurar el mock de la sesión para lanzar una excepción al llamar a commit
    mock_session.commit.side_effect = Exception("Database error")
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        createCrop(valid_crop_data, mock_session)
    
    assert excinfo.value.status_code == 500
    assert "Error inesperado al crear el cultivo" in excinfo.value.detail

if __name__ == "__main__":
    pytest.main()