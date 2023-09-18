import os
from dotenv import load_dotenv
from typing import Annotated
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .database import SessionLocal
from . import crud, schemas

load_dotenv("./.env")


class Envs:
   """Environmental variables
   """ 
   SECRET_KEY=os.getenv('SECRET_KEY')
   ALGORITHM=os.getenv('ALGORITHM')

def get_db():
    """Tries to yield database session maker and closes it in any case

    Yields:
        Iterator[SessionLocal]
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> schemas.User:
    """Creates an user dependency based on a token and database session dependency.
    Uses JWT (JSON Web Token) to decode a token and get an username (subject), then uses it
    to get an user schemas.User object

    Args:
        token (Annotated[str, Depends): depended on oauth2 scheme
        db (Session, optional): database session dependency. Defaults to Depends(get_db).

    Raises:
        credentials_exception: if there is no username provided
        credentials_exception: when excepts JWTError (errors thrown by JWT api)
        credentials_exception: if there is no user matching the username

    Returns:
        schemas.User: current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Envs.SECRET_KEY, algorithms=[Envs.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_login(db, user_login=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
) -> schemas.User:
    """Creates an active user dependency based on the user dependency (get_current_user). 

    Args:
        current_user (Annotated[schemas.User, Depends): depended on get_current_user
    Raises:
        HTTPException: if user is inactive

    Returns:
        schemas.User: current active user
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
            )
    return current_user


async def get_current_active_admin(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
) -> schemas.User:
    """Creates an admin dependency based on the active user dependency (get_current_active_user). 

    Args:
        current_user (Annotated[schemas.User, Depends): depended on get_current_active_user

    Raises:
        HTTPException: when the current user is not an admin

    Returns:
        schemas.User: an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not a superuser."
            )
    return current_user

