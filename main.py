from src.database.database import Base, engine
from fastapi import FastAPI
from src.routes.userRouter import USER_ROUTES
from src.routes.permissionRouter import PERMISSION_ROUTES
from src.routes.passwordResetRouter import PASSWORD_RESET_ROUTES
from src.routes.rol_permissionRoutes import ROL_PERMISSION_ROUTES
from src.routes.roleRoutes import ROLE_ROUTES

Base.metadata.create_all(engine)    

app = FastAPI()

# Incluir las rutas de usuario
app.include_router(USER_ROUTES)

# Incluir las rutas de permisos
app.include_router(PERMISSION_ROUTES)

# Incluir las rutas de restablecimiento de contraseña sin prefijo adicional
app.include_router(PASSWORD_RESET_ROUTES)

#verificar permisos
app.include_router(ROL_PERMISSION_ROUTES)

app.include_router(ROLE_ROUTES)




















































































# @app.post('/logout')
# def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_session)):
#     token=dependencies
#     payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
#     user_id = payload['sub']
#     token_record = db.query(models.TokenTable).all()
#     info=[]
#     for record in token_record :
#         print("record",record)
#         if (datetime.utcnow() - record.created_date).days >1:
#             info.append(record.user_id)
#     if info:
#         existing_token = db.query(models.TokenTable).where(TokenTable.user_id.in_(info)).delete()
#         db.commit()
        
#     existing_token = db.query(models.TokenTable).filter(models.TokenTable.user_id == user_id, models.TokenTable.access_toke==token).first()
#     if existing_token:
#         existing_token.status=False
#         db.add(existing_token)
#         db.commit()
#         db.refresh(existing_token)
#     return {"message":"Logout Successfully"} 