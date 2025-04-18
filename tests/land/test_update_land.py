import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.landModel import Land
from src.schemas.landSchema import UpdateLandSchema
from src.controller.landController import updateLand

@pytest.fixture
def mock_session():
    """Crea un mock para la sesión de base de datos"""
    session = MagicMock(spec=Session)
    session.commit = MagicMock()
    session.refresh = MagicMock()
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

@pytest.fixture
def valid_update_data():
    """Crea datos válidos para actualizar un lote"""
    return UpdateLandSchema(
        nombre="Lote Norte Actualizado",
        area=60.5,
        latitud=4.5710,
        longitud=-74.2974
    )

def test_update_land_success(mock_session, mock_land, valid_update_data):
    """Prueba la actualización exitosa de un lote"""
    # Configurar el mock de la sesión para devolver el lote cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = mock_land
    
    # Ejecutar la función
    result = updateLand(1, valid_update_data, mock_session)
    
    # Verificaciones
    assert mock_session.commit.called
    assert mock_session.refresh.called
    assert "msg" in result
    assert result["msg"] == "Lote actualizado satisfactoriamente"
    
    # Verificar que los atributos se hayan actualizado correctamente
    assert mock_land.nombre == "Lote Norte Actualizado"
    assert mock_land.area == 60.5
    assert mock_land.latitud == 4.5710
    assert mock_land.longitud == -74.2974

def test_update_land_partial(mock_session, mock_land):
    """Prueba la actualización parcial de un lote (solo algunos campos)"""
    # Crear datos de actualización parcial (solo nombre)
    partial_update = UpdateLandSchema(nombre="Lote Norte Parcial")
    
    # Configurar el mock de la sesión
    mock_session.query.return_value.filter.return_value.first.return_value = mock_land
    
    # Ejecutar la función
    result = updateLand(1, partial_update, mock_session)
    
    # Verificaciones
    assert mock_session.commit.called
    assert mock_session.refresh.called
    assert "msg" in result
    assert result["msg"] == "Lote actualizado satisfactoriamente"
    
    # Verificar que solo el nombre se haya actualizado
    assert mock_land.nombre == "Lote Norte Parcial"
    # Los otros atributos deben permanecer sin cambios
    assert mock_land.area == 50.5
    assert mock_land.latitud == 4.5709
    assert mock_land.longitud == -74.2973

def test_update_land_not_found(mock_session, valid_update_data):
    """Prueba el caso en que no se encuentra el lote para actualizar"""
    # Configurar el mock de la sesión para devolver None cuando se filtra por ID
    mock_session.query.return_value.filter.return_value.first.return_value = None
    
    # Verificar que se lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        updateLand(999, valid_update_data, mock_session)
    
    assert excinfo.value.status_code == 404
    assert "Lote con id 999 no encontrado" in excinfo.value.detail
    
    # Verificar que no se llamó a commit ni refresh
    assert not mock_session.commit.called
    assert not mock_session.refresh.called

def test_update_land_empty_values(mock_session, mock_land):
    """Prueba la actualización con valores vacíos o None"""
    # Crear datos de actualización con algunos valores vacíos
    empty_update = UpdateLandSchema(nombre="", area=None)
    
    # Configurar el mock de la sesión
    mock_session.query.return_value.filter.return_value.first.return_value = mock_land
    
    # Ejecutar la función
    result = updateLand(1, empty_update, mock_session)
    
    # Verificaciones
    assert mock_session.commit.called
    assert mock_session.refresh.called
    
    # Verificar que los atributos se hayan actualizado según lo esperado
    assert mock_land.nombre == ""  # Se actualiza a cadena vacía
    assert mock_land.area == 50.5  # No se debería actualizar ya que es None en el update

if __name__ == "__main__":
    pytest.main()