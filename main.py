import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.database import Base, engine

#Rutas
from src.routes.weatherRecordRoute import WEATHER_RECORD_ROUTES
from src.routes.laborCulturalRoutes import LABOR_CULTURAL_ROUTES
from src.routes.cropCycleRoutes import CROP_CYCLE_ROUTES
from src.routes.agriculturalInputRoutes import AGRICULTURAL_INPUT_ROUTES
from src.routes.authRoutes import AUTH_ROUTES
from src.routes.cropRoutes import CROP_ROUTES
from src.routes.farmLotRoutes import FARM_LOT_ROUTES
from src.routes.farmRoutes import FARM_ROUTES
from src.routes.landCropRoutes import LAND_CROP_ROUTES
from src.routes.landRoutes import LAND_ROUTES
from src.routes.passwordResetRoutes import PASSWORD_RESET_ROUTES
from src.routes.permissionRouter import PERMISSION_ROUTES
from src.routes.rol_permissionRoutes import ROL_PERMISSION_ROUTES
from src.routes.roleRoutes import ROLE_ROUTES
from src.routes.userFarmRoutes import USER_FARM_ROUTES
from src.routes.userRoleRoutes import USER_ROLE_ROUTES
from src.routes.userRoutes import USER_ROUTES
# from src.routes.unidadesAreasRoutes import UNIDAD_AREA_ROUTE
from src.routes.varietyArrozRoutes import VARIETY_ARROZ_ROUTES
from src.routes.opMechRoutes import OP_MECH_ROUTES
from src.routes.taskRouetes import TASK_ROUTES
from src.routes.machineryRoutes import MACHINERY_ROUTES
from src.routes.soilAnalysisRoutes import SOIL_ANALYSIS_ROUTES
from src.routes.diagnosticRoutes import DIAGNOSTIC_ROUTES

# Inicializar la aplicación FastAPI
app = FastAPI()

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Obtener las direcciones permitidas desde las variables de entorno
allow_origins = os.getenv("ALLOW_ORIGINS", "").split(",")

# Depuración: Imprimir los orígenes permitidos
print("Orígenes permitidos para CORS:", allow_origins)

# Configuración del middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde las URLs especificadas en la variable de entorno
    #allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir Rutas
app.include_router(AUTH_ROUTES)
app.include_router(USER_ROUTES)
app.include_router(ROLE_ROUTES)
app.include_router(PERMISSION_ROUTES)
app.include_router(ROL_PERMISSION_ROUTES)
app.include_router(USER_ROLE_ROUTES)
app.include_router(FARM_ROUTES)
app.include_router(USER_FARM_ROUTES)
app.include_router(LAND_ROUTES)
# app.include_router(UNIDAD_AREA_ROUTE)
app.include_router(VARIETY_ARROZ_ROUTES)
app.include_router(CROP_ROUTES)
app.include_router(LAND_CROP_ROUTES)
app.include_router(FARM_LOT_ROUTES)
app.include_router(PASSWORD_RESET_ROUTES)  
app.include_router(AGRICULTURAL_INPUT_ROUTES)  
app.include_router(LABOR_CULTURAL_ROUTES)
app.include_router(CROP_CYCLE_ROUTES)
app.include_router(OP_MECH_ROUTES)
app.include_router(TASK_ROUTES)
app.include_router(MACHINERY_ROUTES)
app.include_router(WEATHER_RECORD_ROUTES)
app.include_router(SOIL_ANALYSIS_ROUTES)
app.include_router(DIAGNOSTIC_ROUTES)

@app.get("/")
def read_root():
    return {"message": "Welcome to my API"}

