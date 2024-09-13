from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.database import Base, engine
from src.routes.cropRoutes import CROP_ROUTES
from src.routes.farmRoleRoutes import USER_FARM_ROL_ROUTES
from src.routes.farmRoutes import FARM_ROUTES
from src.routes.landRoutes import LAND_ROUTES
from src.routes.user_farmRoutes import USER_FARM_ROUTES
from src.routes.passwordResetRouter import PASSWORD_RESET_ROUTES
from src.routes.permissionRouter import PERMISSION_ROUTES
from src.routes.rol_permissionRoutes import ROL_PERMISSION_ROUTES
from src.routes.roleRoutes import ROLE_ROUTES
from src.routes.unidadesAreasRoutes import UNIDAD_AREA_ROUTE
from src.routes.userRouter import USER_ROUTES
from src.routes.varietyArrozRoutes import VARIETY_ARROZ_ROUTES
from src.routes.farmLotRoutes import FARM_LOT_ROUTES 
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()


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
app.include_router(FARM_ROUTES)

# Incluir las rutas de finca
app.include_router(USER_FARM_ROUTES)

# Incluir las rutas de lote
app.include_router(LAND_ROUTES)

# Incluir las rutas de unidad de área
app.include_router(UNIDAD_AREA_ROUTE)

# Incluir las rutas para variedades de arroz
app.include_router(VARIETY_ARROZ_ROUTES, prefix="/varieties", tags=["Varieties of Rice"])

# Incluir las rutas para cultivo
app.include_router(CROP_ROUTES)


# Incluir las rutas para lotes de la finca
app.include_router(FARM_LOT_ROUTES)  # Añadir esta línea

# Incluir las rutas para USUARIO FINCA ROLE
app.include_router(USER_FARM_ROL_ROUTES)

# Obtener las direcciones permitidas desde las variables de entorno
allow_origins = os.getenv("ALLOW_ORIGINS", "").split(",")


# Configuración del middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # Permite solicitudes desde las URLs especificadas en la variable de entorno
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)
