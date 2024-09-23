from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.database.database import Base, engine
from dotenv import load_dotenv
import os

from src.routes.authRoutes import AUTH_ROUTES
from src.routes.userRoutes import USER_ROUTES
from src.routes.roleRoutes import ROLE_ROUTES
from src.routes.permissionRouter import PERMISSION_ROUTES
from src.routes.rol_permissionRoutes import ROL_PERMISSION_ROUTES
from src.routes.farmRoutes import FARM_ROUTES
from src.routes.user_farmRoutes import USER_FARM_ROUTES
from src.routes.landRoutes import LAND_ROUTES
from src.routes.cropRoutes import CROP_ROUTES
from src.routes.farmLotRoutes import FARM_LOT_ROUTES
from src.routes.landCropRoutes import LAND_CROP_ROUTES
from src.routes.passwordResetRoutes import PASSWORD_RESET_ROUTES
from src.routes.unidadesAreasRoutes import UNIDAD_AREA_ROUTE
from src.routes.varietyArrozRoutes import VARIETY_ARROZ_ROUTES

from src.helpers.utils import get_current_user

# Inicializar la aplicación FastAPI sin protección global
app = FastAPI()

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Ruta raíz sin protección
@app.get("/")
def read_root():
    return {"message": "Welcome to my API"}

# Incluir las rutas de autenticación sin protección
app.include_router(AUTH_ROUTES)

# Incluir rutas protegidas con autenticación
app.include_router(USER_ROUTES)
app.include_router(ROLE_ROUTES, dependencies=[Depends(get_current_user)])
app.include_router(PERMISSION_ROUTES, dependencies=[Depends(get_current_user)])
app.include_router(ROL_PERMISSION_ROUTES, dependencies=[Depends(get_current_user)])
app.include_router(FARM_ROUTES, dependencies=[Depends(get_current_user)])
app.include_router(USER_FARM_ROUTES, dependencies=[Depends(get_current_user)])
app.include_router(LAND_ROUTES, dependencies=[Depends(get_current_user)])
app.include_router(UNIDAD_AREA_ROUTE, dependencies=[Depends(get_current_user)])
app.include_router(VARIETY_ARROZ_ROUTES, dependencies=[Depends(get_current_user)])
app.include_router(CROP_ROUTES, dependencies=[Depends(get_current_user)])
app.include_router(LAND_CROP_ROUTES, dependencies=[Depends(get_current_user)])
app.include_router(FARM_LOT_ROUTES, dependencies=[Depends(get_current_user)])
app.include_router(PASSWORD_RESET_ROUTES, dependencies=[Depends(get_current_user)])

# Obtener las direcciones permitidas desde las variables de entorno
allow_origins = os.getenv("ALLOW_ORIGINS", "").split(",")

# Configuración del middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)
