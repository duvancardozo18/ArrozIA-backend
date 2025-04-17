import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session

# Importamos los modelos
from src.models.rolModel import Rol
from src.models.permissionModel import RolPermiso
from src.schemas.roleShema import RoleCreate, RoleUpdate, Role

# Importamos directamente las funciones a probar
from src.controller.roleController import (
    create_role,
    get_roles,
    get_role_by_id,
    update_role,
    delete_role
)

# Fixtures para las pruebas
@pytest.fixture
def mock_db():
    """Crea un mock para la sesión de base de datos"""
    db = MagicMock(spec=Session)
    return db

@pytest.fixture
def sample_role():
    """Crea un rol de ejemplo para pruebas"""
    return Rol(id=1, nombre="Admin", descripcion="Rol de administrador")

@pytest.fixture
def sample_role_create():
    """Crea un objeto RoleCreate para pruebas"""
    return RoleCreate(nombre="Admin", descripcion="Rol de administrador", permisos=[1, 2])

@pytest.fixture
def sample_role_update():
    """Crea un objeto RoleUpdate para pruebas"""
    return RoleUpdate(nombre="Super Admin", descripcion="Rol de super administrador")

# Tests para create_role
def test_create_role_success(mock_db, sample_role_create):
    # Configurar el comportamiento del mock
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    mock_db.add = MagicMock()
    
    # Simular la asignación de ID después de refresh
    mock_db.refresh.side_effect = lambda x: setattr(x, "id", 1)
    
    # Ejecutar la función
    result = create_role(sample_role_create, mock_db)
    
    # Verificaciones
    assert mock_db.add.call_count == 3  # Una llamada para el rol + dos para los permisos
    assert mock_db.commit.call_count == 2  # Dos commits: uno para el rol y otro para los permisos
    assert mock_db.refresh.call_count == 1  # Un refresh para el rol
    assert result["message"] == "Role created successfully"
    assert result["role_id"] == 1

def test_create_role_without_permissions(mock_db):
    # Crear rol sin permisos
    role_create = RoleCreate(nombre="Viewer", descripcion="Rol de visualización", permisos=[])
    
    # Configurar el comportamiento del mock
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    mock_db.add = MagicMock()
    mock_db.refresh.side_effect = lambda x: setattr(x, "id", 1)
    
    # Ejecutar la función
    result = create_role(role_create, mock_db)
    
    # Verificaciones
    assert mock_db.add.call_count == 1  # Solo se agrega el rol
    assert mock_db.commit.call_count == 1  # Solo un commit para el rol
    assert result["message"] == "Role created successfully"
    assert result["role_id"] == 1

# Tests para get_roles
def test_get_roles_success(mock_db):
    # Configurar datos de prueba
    mock_roles = [
        Rol(id=1, nombre="Admin", descripcion="Rol de administrador"),
        Rol(id=2, nombre="User", descripcion="Rol de usuario")
    ]
    
    # Configurar el comportamiento del mock
    mock_db.query.return_value.all.return_value = mock_roles
    
    # Ejecutar la función
    result = get_roles(mock_db)
    
    # Verificaciones
    assert result["message"] == "2 roles found"
    assert result["roles"] == mock_roles
    mock_db.query.assert_called_once_with(Rol)

def test_get_roles_empty(mock_db):
    # Configurar el comportamiento del mock para devolver lista vacía
    mock_db.query.return_value.all.return_value = []
    
    # Ejecutar la función
    result = get_roles(mock_db)
    
    # Verificaciones
    assert result["message"] == "0 roles found"
    assert result["roles"] == []

# Tests para get_role_by_id
def test_get_role_by_id_success(mock_db, sample_role):
    # Configurar el comportamiento del mock
    mock_db.query.return_value.filter.return_value.first.return_value = sample_role
    
    # Mock para Role.from_orm
    sample_role_schema = MagicMock()
    Role.from_orm = MagicMock(return_value=sample_role_schema)
    
    # Ejecutar la función
    result = get_role_by_id(1, mock_db)
    
    # Verificaciones
    assert result["message"] == "Role found"
    assert result["role"] == sample_role_schema
    mock_db.query.assert_called_once_with(Rol)
    Role.from_orm.assert_called_once_with(sample_role)

def test_get_role_by_id_not_found(mock_db):
    # Configurar el comportamiento del mock para simular que no se encuentra el rol
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Ejecutar la función y verificar que lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        get_role_by_id(999, mock_db)
    
    # Verificar el código de estado y el detalle de la excepción
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Role not found"

# Tests para update_role
def test_update_role_success(mock_db, sample_role, sample_role_update):
    # Configurar el comportamiento del mock
    mock_db.query.return_value.filter.return_value.first.return_value = sample_role
    
    # Ejecutar la función
    result = update_role(1, sample_role_update, mock_db)
    
    # Verificaciones
    assert result["message"] == "Role updated successfully"
    assert sample_role.nombre == sample_role_update.nombre
    assert sample_role.descripcion == sample_role_update.descripcion
    mock_db.commit.assert_called_once()

def test_update_role_partial(mock_db, sample_role):
    # Crear un objeto de actualización con solo un campo
    partial_update = RoleUpdate(nombre="Manager", descripcion=None)
    
    # Configurar el comportamiento del mock
    mock_db.query.return_value.filter.return_value.first.return_value = sample_role
    
    # Guardar valores originales para comparar después
    original_descripcion = sample_role.descripcion
    
    # Ejecutar la función
    result = update_role(1, partial_update, mock_db)
    
    # Verificaciones
    assert result["message"] == "Role updated successfully"
    assert sample_role.nombre == "Manager"
    assert sample_role.descripcion == original_descripcion  # No debería cambiar
    mock_db.commit.assert_called_once()

def test_update_role_not_found(mock_db, sample_role_update):
    # Configurar el comportamiento del mock para simular que no se encuentra el rol
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Ejecutar la función y verificar que lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        update_role(999, sample_role_update, mock_db)
    
    # Verificar el código de estado y el detalle de la excepción
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Role not found"

# Tests para delete_role
def test_delete_role_success(mock_db, sample_role):
    # Configurar el comportamiento del mock
    mock_db.query.return_value.filter.return_value.first.return_value = sample_role
    
    # Ejecutar la función
    result = delete_role(1, mock_db)
    
    # Verificaciones
    assert result["message"] == "Role deleted successfully"
    mock_db.delete.assert_called_once_with(sample_role)
    mock_db.commit.assert_called_once()

def test_delete_role_not_found(mock_db):
    # Configurar el comportamiento del mock para simular que no se encuentra el rol
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Ejecutar la función y verificar que lanza la excepción correcta
    with pytest.raises(HTTPException) as excinfo:
        delete_role(999, mock_db)
    
    # Verificar el código de estado y el detalle de la excepción
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Role not found"