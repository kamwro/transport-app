from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

#actual database

SQLALCHEMY_DATABASE_URL = "postgresql://myuser:secret@db:5432/rides_db"

engine = create_engine (SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker (autocommit=False, autoflush=False, bind=engine)

#tests database

engine_tests = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_tests)


Base = declarative_base()

