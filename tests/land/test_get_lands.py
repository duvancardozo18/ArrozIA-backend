import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.landModel import Land
from src.models.farmModel import Farm
from src.controller.landController import getLandById, getAllLands

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    return session

@pytest.fixture
def mock_land():
    """Crea un mock de un objeto Land"""
    land = MagicMock(spec=Land)
    land.id = 1
    land.nombre = "Lote Norte"
    land.finca_id = 1
    land.area = 50.5
    land.latitud = 4.5709
    land.longitud = -74.2973
    land.slug = "lote-norte"
    
    # Mock para la relación finca
    mock_finca = MagicMock(spec=Farm)
    mock_finca.nombre = "Finca Las Palmas"
    land.finca = mock_finca
    
    return land

def test_get_all_lands_success(mock_session):
    """Prueba obtener todos los lotes exitosamente"""
    # Crear una lista de lotes mock
    mock_land1 = MagicMock(spec=Land)
    mock_land1.id = 1
    mock_land1.nombre = "Lote Norte"
    
    mock_land2 = MagicMock(spec=Land)
    mock_land2.id = 2
    mock_land2.nombre = "Lote Sur"
    
    mock_lands = [mock_land1, mock_land2]
    
    # Configurar el mock de la sesión para devolver los lotes
    mock_session.query.return_value.all.return_value = mock_lands
    
    # Ejecutar la función
    result = getAllLands(mock_session)
    
    # Verificaciones
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].nombre == "Lote Norte"
    assert result[1].id == 2
    assert result[1].nombre == "Lote Sur"

def test_get_all_lands_empty(mock_session):
    """Prueba el caso en que no hay lotes"""
    # Configurar el mock de la sesión para devolver una lista vacía
    mock_session.query.return_value.all.return_value = []
    
    # Ejecutar la función
    result = getAllLands(mock_session)
    
    # Verificaciones
    assert len(result) == 0
    assert result == []

def test_get_land_by_id_success(mock_session, mock_land):
    """Prueba obtener un lote por ID exitosamente"""
    # Configurar el mock de la sesión para devolver el lote cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = mock_land
    
    # Ejecutar la función
    result = getLandById(1, mock_session)
    
    # Verificaciones
    assert result["id"] == 1
    assert result["nombre"] == "Lote Norte"
    assert result["finca_id"] == 1
    assert result["finca_nombre"] == "Finca Las Palmas"
    assert result["area"] == 50.5
    assert result["latitud"] == 4.5709
    assert result["longitud"] == -74.2973
    assert result["slug"] == "lote-norte"

def test_get_land_by_id_not_found(mock_session):
    """Prueba el caso en que no se encuentra el lote por ID"""
    # Configurar el mock de la sesión para devolver None cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        getLandById(999, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Lote con id 999 no encontrado" in excinfo.value.detail

def test_get_land_by_id_no_farm(mock_session):
    """Prueba el caso en que el lote no tiene finca asociada"""
    # Crear un lote sin finca asociada
    land_no_farm = MagicMock(spec=Land)
    land_no_farm.id = 1
    land_no_farm.nombre = "Lote Sin Finca"
    land_no_farm.finca_id = None
    land_no_farm.area = 50.5
    land_no_farm.latitud = 4.5709
    land_no_farm.longitud = -74.2973
    land_no_farm.slug = "lote-sin-finca"
    land_no_farm.finca = None
    
    # Configurar el mock de la sesión
    mock_session.query.return_value.filter.return_value.first.return_value = land_no_farm
    
    # Ejecutar la función
    result = getLandById(1, mock_session)
    
    # Verificaciones
    assert result["finca_nombre"] == "Finca desconocida"

if __name__ == "__main__":
    pytest.main()