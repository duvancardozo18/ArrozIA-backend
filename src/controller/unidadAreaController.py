# from fastapi import Depends
# from sqlalchemy.orm import Session

# from src.database.database import get_session
# from src.models.landModel import UnidadArea


# def getUnidadArea(session: Session = Depends(get_session)):
#     unidades_areas= session.query(UnidadArea).all()
#     return unidades_areas