from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controller.agricultralInputController import (createInput,
                                                       deleteInput,
                                                       getAllInput,
                                                       getInputById,
                                                       updateInput)
from src.database.database import get_session
from src.schemas.agriculturalInputSchema import (AgriculturalInputCreate,
                                                 AgriculturalInputUpdate)

AGRICULTURAL_INPUT_ROUTES = APIRouter()

@AGRICULTURAL_INPUT_ROUTES.post('/register-input')
def registerinput(input: AgriculturalInputCreate, session: Session = Depends(get_session)):
    return createInput(input, session)
    
@AGRICULTURAL_INPUT_ROUTES.get('/inputs', response_model=list[AgriculturalInputCreate])
def listinputs(session: Session = Depends(get_session)):
    return getAllInput(session)

@AGRICULTURAL_INPUT_ROUTES.get('/input/{input_id}', response_model=AgriculturalInputCreate)
def getinput(input_id: int, session: Session = Depends(get_session)):
    return getInputById(input_id, session)

@AGRICULTURAL_INPUT_ROUTES.put('/update/input/{input_id}')
def updateinputRoute(input_id: int, input: AgriculturalInputUpdate, session: Session = Depends(get_session)):
    return updateInput(input_id, input, session)

@AGRICULTURAL_INPUT_ROUTES.delete('/delete/input/{input_id}')
def deleteinputRoute(input_id: int, session: Session = Depends(get_session)):
    return deleteInput(input_id, session)
