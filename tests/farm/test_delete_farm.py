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
from src.controller.farmCrontroller import deleteFarm

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    session.delete = MagicMock()
    session.commit = MagicMock()
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

def test_delete_farm_success(mock_session, sample_farm):
    """Prueba la eliminación exitosa de una finca"""
    # Configurar el comportamiento del mock
    mock_session.query.return_value.filter.return_value.first.return_value = sample_farm
    
    # Ejecutar la función
    result = deleteFarm(1, mock_session)
    
    # Verificaciones
    mock_session.delete.assert_called_once_with(sample_farm)  # Sin usar assert
    mock_session.commit.assert_called_once()
    assert mock_session.commit.called
    assert "msg" in result
    assert result["msg"] == "Finca eliminada satisfactoriamente"

def test_delete_farm_not_found(mock_session):
    """Prueba la eliminación de una finca cuando el ID no existe"""
    # Configurar el comportamiento del mock para devolver None
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        deleteFarm(999, mock_session)
    
    # Verificaciones
    assert excinfo.value.status_code == 404
    assert "Finca con id 999 no encontrada" in excinfo.value.detail
    assert not mock_session.delete.called
    assert not mock_session.commit.called

if __name__ == "__main__":
    pytest.main()