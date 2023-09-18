from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    """User base schema based on pydantic BaseModel

    Args:
        BaseModel (str | bool): basic info about users
    """    
    login: str
    first_name: str
    last_name: str
    address: str
    is_admin: bool = False

class CreateUser(UserBase):
    """Create user schema based on user base schema

    Args:
        UserBase (str): password
    """    
    hashed_password: str

class ActivateUser(UserBase):
    """Schema for activation code storage

    Args:
        UserBase (str): activation code
    """    
    activation_code: str

class User(UserBase):
    """Schema for default user info: autoincremented id and verification status

    Args:
        UserBase (int | bool)
    """    
    id: int
    is_active: bool = False
    
    class Config:
        """https://docs.pydantic.dev/latest/usage/models/#orm-mode-aka-arbitrary-class-instances
        """        
        from_attributes=True
        orm_mode = True

class RideBase(BaseModel):
    """Ride base schema based on pydantic BaseModel

    Args:
        BaseModel (str | float | datetime)
    """    
    start_city: str
    destination_city: str
    distance: float
    km_fee: float
    departure_date: datetime

class RideCreate(RideBase):
    """Create ride schema, actually empty 
    """
    pass 

class Ride(RideBase):
    """Schema for default ride info: autoincremented id, calculated price, active status and id of user who took the ride (or will take)

    Args:
        RideBase (int | float | bool | None)
    """    
    id: int
    price: float
    is_active: bool = True
    user_id_taken: int | None = None

    class Config:
        """https://docs.pydantic.dev/latest/usage/models/#orm-mode-aka-arbitrary-class-instances
        """        
        from_attributes=True
        orm_mode = True

class Token(BaseModel):
    """Token schema based on pydantic BaseModel

    Args:
        BaseModel (str)
    """    
    access_token: str
    token_type: str

    class Config:
        """https://docs.pydantic.dev/latest/usage/models/#orm-mode-aka-arbitrary-class-instances
        """        
        orm_mode = True

class TokenData(BaseModel):
    """Schema containing username attached to the token data

    Args:
        BaseModel (str | None)
    """    
    username: str or None = None

    class Config:
        """https://docs.pydantic.dev/latest/usage/models/#orm-mode-aka-arbitrary-class-instances
        """        
        orm_mode = True

class EmailSchema(BaseModel):
    """Email schema based on pydantic BaseModel

    Args:
        BaseModel (EmailStr | str)
    """   
    email: List[EmailStr | str]


