from sqlalchemy import Boolean, Column, Integer, Float, String, DateTime
from .database import Base


class User(Base):
    """Sqlalchemy model of User table based on the database sqlalchemic declarative_base()
    """    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    is_active = Column(Boolean)
    is_admin = Column(Boolean)
    activation_code = Column(String)


class Ride(Base):
    """Sqlalchemy model of Ride table based on the database sqlalchemic declarative_base()
    """    
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    start_city = Column(String)
    destination_city = Column(String)
    distance = Column(Float)
    km_fee = Column(Float)
    price = Column(Float)
    departure_date = Column(DateTime)
    is_active = Column(Boolean)
    user_id_taken = Column(Integer)