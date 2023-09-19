import os
import re
from dotenv import load_dotenv
from enum import Enum
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from passlib.context import CryptContext
from jose import jwt
from .schemas import EmailSchema, User


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
   ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')


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

class EmailUtils():
    """Class container for email utils, like methods sending emails
    """    

    conf = ConnectionConfig(
        MAIL_USERNAME=Envs.MAIL_USERNAME,
        MAIL_PASSWORD=Envs.MAIL_PASSWORD,
        MAIL_FROM=Envs.MAIL_FROM,
        MAIL_PORT=Envs.MAIL_PORT,
        MAIL_SERVER=Envs.MAIL_SERVER,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )
    
    @staticmethod
    def is_email_valid(username: str) -> bool:
        """Validates an email address using regex

        Args:
            username (str): email to validate

        Returns:
            bool: is the email valid
        """        
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        return re.fullmatch(email_regex, username)
    
    @staticmethod
    async def send_activation_link(user: User):
        """Sends an activation link to the user email

        Args:
            user (User): user
        """    
        template = """
                <html>
                <body>
                
        <p>Hi """+user.first_name+""",
                <br>your activation link: http://localhost:8008/users/"""+str(user.id)+"""/activate/"""+user.activation_code +""" </p>
        
        
                </body>
                </html>
                """
        email = EmailSchema(email=[user.login])
        message = MessageSchema(
                subject="Activate your account",
                recipients=email.model_dump().get("email"),
                body=template,
                subtype=MessageType.html
                )
        
        fm = FastMail(EmailUtils.conf)
        await fm.send_message(message)
    
    @staticmethod
    async def send_self_deletion_email(user: User):
        """Sends an deletion confirmation to the user email

        Args:
            user (User): user
        """      
        template = """
            <html>
            <body>
            
    
    <p>Hi """+user.first_name+""",
            <br>Your account has been successfully deleted.
            <br>We're sorry to hear it. Come back anytime. </p>
    

            </body>
            </html>
            """
        
        email = EmailSchema(email=[user.login])
        message = MessageSchema(
            subject="Your account has been deleted",
            recipients=email.model_dump().get("email"),
            body=template,
            subtype=MessageType.html
            )
        
        fm = FastMail(EmailUtils.conf)
        await fm.send_message(message)

    @staticmethod
    async def send_deletion_email(user: User):
        """Sends an deletion confirmation to the user email

        Args:
            user (User): user
        """      
        template = """
            <html>
            <body>
            

    <p>Hi """+user.first_name+""",
            <br>We're sorry to hear it, but your account has been deleted.
            <br>Hope to get you in touch in the future.</p>
    
    
            </body>
            </html>
            """
        
        email = EmailSchema(email=[user.login])
        message = MessageSchema(
            subject="Your account has been deleted",
            recipients=email.model_dump().get("email"),
            body=template,
            subtype=MessageType.html
            )
    
        fm = FastMail(EmailUtils.conf)
        await fm.send_message(message)


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