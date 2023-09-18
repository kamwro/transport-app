import os
from datetime import timedelta
from typing import Annotated
from starlette.responses import JSONResponse
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas
from .utils import Tags, description
from .database import engine
from .dependencies import get_db
from .utils import SecurityUtils
from .routers import users, rides
from dotenv import load_dotenv


load_dotenv("./.env")


class Envs:
    """Environmental variables
    """
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


models.Base.metadata.create_all(bind=engine)


app = FastAPI(    
    title = "Transport Management App",
    description = description,
    version = "pre-alpha",
    contact = {
        "name": "Kamil Wróbel",
        "url": "https://github.com/kamwro",
    }
)


app.include_router(users.router)
app.include_router(rides.router)


origins = [
    """Ports for middleware
    """    
    "http://localhost",
    "http://localhost:8080" #for frontend
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary = "Welcome to the app", tags = ["Hello World"])
async def welcome_to_the_app() -> JSONResponse:
    """Returns JSONResponse
    """
    return JSONResponse(status_code=200, content={"message": "Hello world! Go to the /docs."})

@app.post("/token", response_model=schemas.Token, summary = "Token login",
           tags = [Tags.acc_login])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
, db: Session = Depends(get_db)):
    """
    - Log in using Authorize button in the top right corner of swagger UI. 
    - User authentication uses OAuth2 password request form to get an access token.

    Returns access token.
    """
    user = users.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Envs.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = SecurityUtils.create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

