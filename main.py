from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.database import Base, engine
from src.routes.fincaRoutes import FINCA_ROUTES
from src.routes.loteRoutes import LOTE_ROUTES
from src.routes.passwordResetRouter import PASSWORD_RESET_ROUTES
from src.routes.permissionRouter import PERMISSION_ROUTES
from src.routes.rol_permissionRoutes import ROL_PERMISSION_ROUTES
from src.routes.roleRoutes import ROLE_ROUTES
from src.routes.unidadesAreasRoutes import UNIDAD_AREA_ROUTE
from src.routes.userRouter import USER_ROUTES
from src.routes.varietyArrozRoutes import VARIETY_ARROZ_ROUTES  # Importa el router correcto para variedades de arroz

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Incluir las rutas de usuario
app.include_router(USER_ROUTES)

# Incluir las rutas de permisos
app.include_router(PERMISSION_ROUTES)

# Incluir las rutas de restablecimiento de contraseña
app.include_router(PASSWORD_RESET_ROUTES)

# Verificar permisos
app.include_router(ROL_PERMISSION_ROUTES)

# Incluir las rutas de roles
app.include_router(ROLE_ROUTES)

# Incluir las rutas de finca
app.include_router(FINCA_ROUTES)

# Incluir las rutas de lote
app.include_router(LOTE_ROUTES)

# Incluir las rutas de unidad de área
app.include_router(UNIDAD_AREA_ROUTE)

# Incluir las rutas para variedades de arroz
app.include_router(VARIETY_ARROZ_ROUTES, prefix="/varieties", tags=["Varieties of Rice"])

# Configuración del middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permite solicitudes solo desde el frontend en localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

