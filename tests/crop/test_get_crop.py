import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
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
from src.models.varietyArrozModel import VarietyArrozModel
from src.controller.cropController import getCrop, getAllCrops, getCropsByLand, getCropInfo

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    return session

@pytest.fixture
def mock_crop():
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

    """Crea un mock para un cultivo"""
    crop = MagicMock(spec=Crop)
    crop.id = 1
    crop.cropName = "Arroz Premium"
    crop.varietyId = 1
    crop.plotId = 1
    crop.plantingDate = datetime.now()
    crop.estimatedHarvestDate = datetime.now().replace(month=datetime.now().month + 3)
    crop.slug = "arroz-premium"
    
    # Configurar la relación con variedad
    mock_variety = MagicMock()
    mock_variety.id = 1
    mock_variety.nombre = "Variedad Premium"
    crop.variety = mock_variety
    
    return crop

@pytest.fixture
def mock_crops():
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
    
    """Crea una lista de mocks para cultivos"""
    crop1 = MagicMock(spec=Crop)
    crop1.id = 1
    crop1.cropName = "Arroz Premium"
    crop1.varietyId = 1
    crop1.plotId = 1
    crop1.plantingDate = datetime.now()
    crop1.estimatedHarvestDate = datetime.now().replace(month=datetime.now().month + 3)
    crop1.slug = "arroz-premium"
    
    # Configurar la relación con variedad
    mock_variety1 = MagicMock()
    mock_variety1.id = 1
    mock_variety1.nombre = "Variedad Premium"
    crop1.variety = mock_variety1
    
    crop2 = MagicMock(spec=Crop)
    crop2.id = 2
    crop2.cropName = "Arroz Estándar"
    crop2.varietyId = 2
    crop2.plotId = 2
    crop2.plantingDate = datetime.now()
    crop2.estimatedHarvestDate = datetime.now().replace(month=datetime.now().month + 3)
    crop2.slug = "arroz-estandar"
    
    # Configurar la relación con variedad
    mock_variety2 = MagicMock()
    mock_variety2.id = 2
    mock_variety2.nombre = "Variedad Estándar"
    crop2.variety = mock_variety2
    
    return [crop1, crop2]

def test_get_crop_success(mock_session, mock_crop):
    """Prueba obtener un cultivo por ID exitosamente"""
    # Configurar el mock de la sesión
    mock_query = MagicMock()
    mock_options = MagicMock()
    mock_filter = MagicMock()
    mock_first = MagicMock(return_value=mock_crop)
    
    mock_session.query.return_value = mock_query
    mock_query.options.return_value = mock_options
    mock_options.filter.return_value = mock_filter
    mock_filter.first.return_value = mock_crop
    
    # Ejecutar la función
    result = getCrop(1, mock_session)
    
    # Verificaciones
    assert result["id"] == 1
    assert result["cropName"] == "Arroz Premium"
    assert result["varietyId"] == 1
    assert result["varietyName"] == "Variedad Premium"
    assert result["plotId"] == 1
    assert result["slug"] == "arroz-premium"

def test_get_crop_not_found(mock_session):
    """Prueba el caso en que no se encuentra el cultivo"""
    # Configurar el mock de la sesión para devolver None
    mock_query = MagicMock()
    mock_options = MagicMock()
    mock_filter = MagicMock()
    mock_first = MagicMock(return_value=None)
    
    mock_session.query.return_value = mock_query
    mock_query.options.return_value = mock_options
    mock_options.filter.return_value = mock_filter
    mock_filter.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        getCrop(999, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Crop not found" in excinfo.value.detail

def test_get_crop_variety_not_found(mock_session):
    """Prueba el caso en que el cultivo no tiene variedad asociada"""
    # Crear un crop sin variedad
    crop_no_variety = MagicMock(spec=Crop)
    crop_no_variety.id = 1
    crop_no_variety.cropName = "Arroz Sin Variedad"
    crop_no_variety.varietyId = None
    crop_no_variety.plotId = 1
    crop_no_variety.variety = None  # Sin variedad
    
    # Configurar el mock de la sesión
    mock_query = MagicMock()
    mock_options = MagicMock()
    mock_filter = MagicMock()
    mock_first = MagicMock(return_value=crop_no_variety)
    
    mock_session.query.return_value = mock_query
    mock_query.options.return_value = mock_options
    mock_options.filter.return_value = mock_filter
    mock_filter.first.return_value = crop_no_variety
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        getCrop(1, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Variety not found" in excinfo.value.detail

def test_get_all_crops_success(mock_session, mock_crops):
    """Prueba obtener todos los cultivos exitosamente"""
    # Configurar el mock de la sesión
    mock_query = MagicMock()
    mock_options = MagicMock()
    mock_all = MagicMock(return_value=mock_crops)
    
    mock_session.query.return_value = mock_query
    mock_query.options.return_value = mock_options
    mock_options.all.return_value = mock_crops
    
    # Ejecutar la función
    result = getAllCrops(mock_session)
    
    # Verificaciones
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["cropName"] == "Arroz Premium"
    assert result[0]["varietyName"] == "Variedad Premium"
    assert result[1]["id"] == 2
    assert result[1]["cropName"] == "Arroz Estándar"
    assert result[1]["varietyName"] == "Variedad Estándar"

def test_get_all_crops_empty(mock_session):
    """Prueba obtener todos los cultivos cuando no hay ninguno"""
    # Configurar el mock de la sesión para devolver lista vacía
    mock_query = MagicMock()
    mock_options = MagicMock()
    mock_all = MagicMock(return_value=[])
    
    mock_session.query.return_value = mock_query
    mock_query.options.return_value = mock_options
    mock_options.all.return_value = []
    
    # Ejecutar la función
    result = getAllCrops(mock_session)
    
    # Verificaciones
    assert len(result) == 0
    assert result == []

def test_get_crops_by_land_success(mock_session, mock_crops):
    """Prueba obtener cultivos por lote exitosamente"""
    # Asumir que ambos cultivos pertenecen al mismo lote
    for crop in mock_crops:
        crop.plotId = 1
    
    # Configurar el mock de la sesión
    mock_query = MagicMock()
    mock_options = MagicMock()
    mock_filter = MagicMock()
    mock_all = MagicMock(return_value=mock_crops)
    
    mock_session.query.return_value = mock_query
    mock_query.options.return_value = mock_options
    mock_options.filter.return_value = mock_filter
    mock_filter.all.return_value = mock_crops
    
    # Ejecutar la función
    result = getCropsByLand(1, mock_session)
    
    # Verificaciones
    assert len(result) == 2
    assert result[0]["plotId"] == 1
    assert result[1]["plotId"] == 1

def test_get_crops_by_land_empty(mock_session):
    """Prueba obtener cultivos por lote cuando no hay ninguno"""
    # Configurar el mock de la sesión para devolver lista vacía
    mock_query = MagicMock()
    mock_options = MagicMock()
    mock_filter = MagicMock()
    mock_all = MagicMock(return_value=[])
    
    mock_session.query.return_value = mock_query
    mock_query.options.return_value = mock_options
    mock_options.filter.return_value = mock_filter
    mock_filter.all.return_value = []
    
    # Ejecutar la función
    result = getCropsByLand(1, mock_session)
    
    # Verificaciones
    assert len(result) == 0
    assert result == []

def test_get_crop_info_success(mock_session):
    """Prueba obtener información del cultivo por slugs exitosamente"""
    # Mocks para finca, lote, cultivo y variedad
    mock_farm = MagicMock(spec=Farm)
    mock_farm.id = 1
    mock_farm.nombre = "Finca Las Palmas"
    mock_farm.slug = "finca-las-palmas"
    
    mock_land = MagicMock(spec=Land)
    mock_land.id = 1
    mock_land.nombre = "Lote Norte"
    mock_land.finca_id = 1
    mock_land.slug = "lote-norte"
    
    mock_crop = MagicMock(spec=Crop)
    mock_crop.id = 1
    mock_crop.cropName = "Arroz Premium"
    mock_crop.varietyId = 1
    mock_crop.plotId = 1
    mock_crop.plantingDate = datetime.now()
    mock_crop.estimatedHarvestDate = datetime.now().replace(month=datetime.now().month + 3)
    mock_crop.slug = "arroz-premium"
    
    mock_variety = MagicMock(spec=VarietyArrozModel)
    mock_variety.id = 1
    mock_variety.nombre = "Variedad Premium"
    
    # Configurar los mocks de las consultas
    def mock_query_filter_first_side_effect(model, filter_args):
        if model == Farm:
            return mock_farm
        elif model == Land:
            return mock_land
        elif model == Crop:
            return mock_crop
        elif model == VarietyArrozModel:
            return mock_variety
        return None
    
    # Configurar las consultas para devolver los diferentes objetos
    def mock_query_side_effect(model):
        mock_filter = MagicMock()
        if model == Farm:
            mock_filter.filter.return_value.first.return_value = mock_farm
        elif model == Land:
            mock_filter.filter.return_value.first.return_value = mock_land
        elif model == Crop:
            mock_filter.filter.return_value.first.return_value = mock_crop
        elif model == VarietyArrozModel:
            mock_filter.filter.return_value.first.return_value = mock_variety
        return mock_filter
    
    mock_session.query.side_effect = mock_query_side_effect
    
    # Ejecutar la función
    result = getCropInfo("finca-las-palmas", "lote-norte", "arroz-premium", mock_session)
    
    # Verificaciones
    assert result["id"] == 1
    assert result["cropName"] == "Arroz Premium"
    assert result["cropSlug"] == "arroz-premium"
    assert result["varietyId"] == 1
    assert result["varietyName"] == "Variedad Premium"
    assert result["plotId"] == 1
    assert result["plotName"] == "Lote Norte"
    assert result["plotSlug"] == "lote-norte"
    assert result["fincaSlug"] == "finca-las-palmas"

def test_get_crop_info_finca_not_found(mock_session):
    """Prueba obtener información cuando no se encuentra la finca"""
    # Configurar la consulta para devolver None para la finca
    def mock_query_side_effect(model):
        mock_filter = MagicMock()
        if model == Farm:
            mock_filter.filter.return_value.first.return_value = None
        return mock_filter
    
    mock_session.query.side_effect = mock_query_side_effect
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        getCropInfo("finca-inexistente", "lote-norte", "arroz-premium", mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Finca not found" in excinfo.value.detail

def test_get_crop_info_lote_not_found(mock_session):
    """Prueba obtener información cuando no se encuentra el lote"""
    # Mocks para finca
    mock_farm = MagicMock(spec=Farm)
    mock_farm.id = 1
    mock_farm.slug = "finca-las-palmas"
    
    # Configurar las consultas
    def mock_query_side_effect(model):
        mock_filter = MagicMock()
        if model == Farm:
            mock_filter.filter.return_value.first.return_value = mock_farm
        elif model == Land:
            mock_filter.filter.return_value.first.return_value = None
        return mock_filter
    
    mock_session.query.side_effect = mock_query_side_effect
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        getCropInfo("finca-las-palmas", "lote-inexistente", "arroz-premium", mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Lote not found" in excinfo.value.detail

if __name__ == "__main__":
    pytest.main()