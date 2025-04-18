import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.landModel import Land
from src.controller.landController import deleteLand

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    session.delete = MagicMock()
    session.commit = MagicMock()
    return session

@pytest.fixture
def mock_land():
    """Crea un mock de un objeto Land existente"""
    land = MagicMock(spec=Land)
    land.id = 1
    land.nombre = "Lote Norte"
    land.finca_id = 1
    land.area = 50.5
    land.latitud = 4.5709
    land.longitud = -74.2973
    land.slug = "lote-norte"
    return land

def test_delete_land_success(mock_session, mock_land):
    """Prueba la eliminación exitosa de un lote"""
    # Configurar el mock de la sesión para devolver el lote cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = mock_land
    
    # Ejecutar la función
    result = deleteLand(1, mock_session)
    
    # Verificaciones
    assert mock_session.delete.called
    assert mock_session.commit.called
    assert "msg" in result
    assert result["msg"] == "Lote eliminado satisfactoriamente"
    
    # Verificar que se llamó a delete con el objeto correcto
    mock_session.delete.assert_called_with(mock_land)

def test_delete_land_not_found(mock_session):
    """Prueba el caso en que no se encuentra el lote para eliminar"""
    # Configurar el mock de la sesión para devolver None cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        deleteLand(999, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Lote con id 999 no encontrado" in excinfo.value.detail
    
    # Verificar que no se llamó a delete ni commit
    assert not mock_session.delete.called
    assert not mock_session.commit.called

def test_delete_land_database_error(mock_session, mock_land):
    """Prueba el manejo de errores de base de datos durante la eliminación"""
    # Configurar el mock de la sesión para lanzar una excepción al llamar a commit
    mock_session.query.return_value.filter.return_value.first.return_value = mock_land
    mock_session.commit.side_effect = Exception("Database error")
    
    # Verificar que se propaga la excepción
    with pytest.raises(Exception) as excinfo:
        deleteLand(1, mock_session)
    
    assert str(excinfo.value) == "Database error"
    
    # Verificar que se llamó a delete pero no se completó el commit
    assert mock_session.delete.called
    assert mock_session.commit.called

if __name__ == "__main__":
    pytest.main()