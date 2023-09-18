from .database import SessionLocal
from fastapi.security import OAuth2PasswordBearer

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