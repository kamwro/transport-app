import os
from dotenv import load_dotenv
from enum import Enum
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt


load_dotenv("./.env")


class Envs:
   """Environmental variables
   """ 
   MAIL_USERNAME=os.getenv('MAIL_USERNAME')
   MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
   MAIL_FROM = os.getenv('MAIL_FROM')
   MAIL_PORT=os.getenv('MAIL_PORT')
   MAIL_SERVER=os.getenv('MAIL_SERVER')
   SECRET_KEY=os.getenv('SECRET_KEY')
   ALGORITHM=os.getenv('ALGORITHM')


class SecurityUtils():
    """Security utils static functions and pwd_context for cryptograhics
    """    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Checks if plain password matches hashed password

        Args:
            plain_password (str): plain password
            hashed_password (str): hashed password

        Returns:
            bool: plain password == hashed password
        """
        return SecurityUtils.pwd_context.verify(plain_password, hashed_password)


    @staticmethod
    def get_password_hash(password: str) -> str:
        """Gets a password hash

        Args:
            password (str): plain password

        Returns:
            str: password hash
        """
        return SecurityUtils.pwd_context.hash(password)


    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None  = None) -> str:
        """Gets an access token

        Args:
            data (dict): key:value pair of "sub":user login
            expires_delta (timedelta | None, optional): time until the token expires. Defaults to None.

        Returns:
            str: access token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Envs.SECRET_KEY, algorithm=Envs.ALGORITHM)
        return encoded_jwt


class Tags(Enum):
    """Tags for API endpoints

    Args:
        Enum (str): tags
    """    
    acc_create = "account creation"
    acc_login = "login"
    my_acc = "my account"
    rides = "rides"
    adm_actions_rides = "admin actions - rides"
    adm_actions_users = "admin actions - users"


description = """
## markdown
"""