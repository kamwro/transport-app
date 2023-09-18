import os
from dotenv import load_dotenv
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from typing import Annotated
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from ..utils import Tags, SecurityUtils
from ..dependencies import get_db, oauth2_scheme
from .. import crud, schemas


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


router = APIRouter(
    prefix="/users",
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)) -> schemas.User:
    """Checks if user exists and have verified password, then returns the user schema

    Args:
        username (str): login (email)
        password (str): password
        db (Session, optional): database session dependency. Defaults to Depends(get_db).

    Returns:
        schemas.User
    """
    user = crud.get_user_by_login(db, username)
    if user == None:
        return False
    if not SecurityUtils.verify_password(password, user.hashed_password):
        return False
    return user


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


@router.post("/", response_model=schemas.User, summary= "Create an user account",
          response_description = "Succesfully created an user account.",
          tags = [Tags.acc_create])
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Creates an user account, providing information:

    - **login** (str): an email address that will be used to log in,
    - **first_name** (str): first name of the user,
    - **last_name** (str): last_name of the user,
    - **address** (str): billing address,
    - **password** (str): password that will be used to log in and stored as a hash in the database
    - **is_admin** (bool): post **true** if you wish to create an admin account

    After posting the account informations, an verification link will be send to given email (login).
    In order to activate your account, paste the link into the browser with app working - will redirect
    you to the /users/me/{user_id}/activate/{activation_code} endpoint.

    **Users with the admin status are active by default and thus do not have to activate their account.**

    Returns JSONResponse with user data and confirmation about sending an activation email.
    """
    db_user = crud.get_user_by_login(db=db, user_login=user.login)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
            detail="Email already registered"
            )
    crud.create_user(db=db, user=user)
    new_user = crud.get_user_by_login(db=db, user_login=user.login)

    user_data = user.model_dump()
    user_data = {info:user_data[info] for info in user_data if info!='hashed_password'}
    
    if new_user.is_admin == False:
        template = """
            <html>
            <body>
            
    <p>Hi """+new_user.first_name+""",
            <br>your activation link: http://localhost:8008/users/"""+str(new_user.id)+"""/activate/"""+new_user.activation_code +""" </p>
    
    
            </body>
            </html>
            """
        email = schemas.EmailSchema(email=[new_user.login])
        message = MessageSchema(
            subject="Activate your account",
            recipients=email.model_dump().get("email"),
            body=template,
            subtype=MessageType.html
            )
    
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"user data: ": [user_data], "message": f"activation code has been sent to {new_user.login}"})
    else:
        return JSONResponse(status_code=200, content={"user data: ": [user_data], "message": "user is a superuser. Automatic account activation."})


@router.get("/me/", response_model = schemas.User, summary = "Read my info",
             response_description = "Successfully read current user info.", tags = [Tags.my_acc])
async def read_my_info(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
) -> schemas.User:
    """
    Returns an User object with your account information listed.
    Won't show your hashed password or activation code.
    """
    return current_user


@router.post("/me/send-activation-code", summary = "Resend activation code",
           response_description = "Successfully send activation email.", tags = [Tags.my_acc])
async def send_activation_code(current_user: Annotated[schemas.User, Depends(get_current_user)]) -> JSONResponse:
    """
    Sends an activation link to your email address. 
    Could be useful if the first activation email will gone missing, be stucked in the spam folder or deleted by accident.

    Returns JSONResponse with the success confirmation message or raises a HTTPException if user is already active.
    """
    if current_user.is_active == True:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="User already active",
            headers={"WWW-Authenticate": "Bearer"},
        )
    template = """
        <html>
        <body>
         
 
<p>Hi """+current_user.first_name+""",
        <br>your activation link: http://localhost:8008/users/"""+str(current_user.id)+"""/activate/"""+current_user.activation_code +""" </p>
 
 
        </body>
        </html>
        """
    email = schemas.EmailSchema(email=[current_user.login])
    message = MessageSchema(
        subject="Activate your account",
        recipients=email.model_dump().get("email"),
        body=template,
        subtype=MessageType.html
        )
 
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": f"activation code has been sent to {current_user.login}"})


@router.get("/{user_id}/activate/{activation_code}", summary = "Activate an user",
           response_description = "Successfully activated an account.", tags = [Tags.my_acc])
async def activate_my_account(user_id: int, activation_code: str,
db: Session = Depends(get_db)) -> JSONResponse:
    """
    This endpoint was created to serve as an account verification link, that's why its GET, not POST.

    You can also activate your account by providing some information: 

    - **user_id** (int): your user id,
    - **activation_code** (str): your activation code, generated by account creation.
    You can only get it straight from the database.

    After using this endpoint, the user should be now active.

    Returns JSONResponse with the success confirmation message.
    """
    user_login = crud.get_user_by_ID(db=db, user_id=user_id).login
    if crud.get_user_by_login(db=db,user_login=user_login).is_active == True:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="User already active",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif crud.get_user_by_login(db=db,user_login=user_login).activation_code != activation_code:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect activation code.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    crud.activate_user(db=db, user_login=user_login)
    return JSONResponse(status_code = 200, content={"message": "your account has been activated."})


@router.delete("/me/delete", response_model=schemas.User, summary = "Activate an user",
               response_description = "Successfully deleted an account.", tags = [Tags.my_acc])
async def delete_my_account(current_user: Annotated[schemas.User, Depends(get_current_user)],
db: Session = Depends(get_db)) -> JSONResponse:
    """
    Deletes your account permanently.

    After deletion, you will receive an email to your login email address confirming your action.

    Returns JSONResponse with the success confirmation message.
    """
    username = current_user.login
    template = """
        <html>
        <body>
         
 
<p>Hi """+current_user.first_name+""",
        <br>Your account has been successfully deleted.
        <br>We're sorry to hear it. Come back anytime. </p>
 

        </body>
        </html>
        """
    crud.remove_user(db=db, user_login=current_user.login)
    email = schemas.EmailSchema(email=[username])
    message = MessageSchema(
        subject="Your account has been deleted",
        recipients=email.model_dump().get("email"),
        body=template,
        subtype=MessageType.html
        )
    
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": f"Your account has been deleted. An email has been sent to the {username}."})
    
#admin

@router.get("/{username}", response_model = schemas.User, summary = "View an user info",
            response_description = "Successfully read an user info.", tags = [Tags.adm_actions_users])
async def view_user_info(username: str, current_user: Annotated[schemas.User, Depends(get_current_active_admin)],
                      db: Session = Depends(get_db)) -> schemas.User:
    """
    Views an user info providing **username** (str). 
    Hashed password and verification code won't be showed.

    Returns an User object or raises a HTTPException when there's no such user.
    """
    user = crud.get_user_by_login(db=db, user_login=username)
    if user is not None:
        return user
    else:
       raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=f"There's no user with email = {username}"
        )


@router.patch("/{username}/grant-adm", response_model = schemas.User, summary = "Grant the admin status to an user",
              response_description = "Successfully granted the admin status.", tags = [Tags.adm_actions_users])
async def grant_adm(username: str, current_user: Annotated[schemas.User, Depends(get_current_active_admin)],
                      db: Session = Depends(get_db)) -> schemas.User:
    """
    Grants an user the admin status providing **username** (str). 

    Returns an User object or raises a HTTPException if user is already an admin or there's no such user.
    """
    user = crud.get_user_by_login(db=db, user_login=username)
    if user is not None:
        if user.is_admin:
            raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="User already an admin"
            )
        else:
            return crud.grant_admin_status(db=db, user_login=username)
    else:
        raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=f"There's no user with email = {username}"
        )


@router.patch("/{username}/remove-adm", response_model = schemas.User, summary = "Remove the admin status from an user",
              response_description = "Successfully taken the admin status from an user.",  tags = [Tags.adm_actions_users])
async def remove_adm(username: str, current_user: Annotated[schemas.User, Depends(get_current_active_admin)],
                      db: Session = Depends(get_db)) -> schemas.User:
    """
    Takes the admin status from an user providing **username** (str).

    Returns an User object or raises a HTTPException if user is already not an admin or there's no such user. 
    """
    user = crud.get_user_by_login(db=db, user_login=username)
    if user is not None:
        if user.is_admin == False:
            raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="User not an admin"
            )
        else:
            return crud.remove_admin_status(db=db, user_login=username)
    else:
        raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=f"There's no user with email = {username}"
        )


@router.patch("/{username}/activate", response_model = schemas.User, summary = "Activate an user",
              response_description = "Successfully activated an user.", tags = [Tags.adm_actions_users])
async def activate_user(username: str, current_user: Annotated[schemas.User, Depends(get_current_active_admin)],
                      db: Session = Depends(get_db)) -> schemas.User:
    """
    Activate an user account providing **username** (str).
    Could be handy with problems with the email service.

    Returns an User object or raises a HTTPException if user is already active or there's no such user.
    """
    user = crud.get_user_by_login(db=db, user_login=username)
    if user is not None:
        if user.is_active:
            raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="User already active"
            )
        else:
            return crud.activate_user(db=db, user_login=username)
    else:
        raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=f"There's no user with email = {username}"
        )


@router.patch("/{username}/deactivate", response_model = schemas.User, summary = "Deactivate an user",
              response_description = "Successfully deactivated an user.", tags = [Tags.adm_actions_users])
async def deactivate_user(username: str, current_user: Annotated[schemas.User, Depends(get_current_active_admin)],
                      db: Session = Depends(get_db)) -> schemas.User:
    """
    Deactivates an user account providing **username** (str).

    Returns an User object or raises a HTTPException if user is already inactive or there's no such user.
    """
    user = crud.get_user_by_login(db=db, user_login=username)
    if user is not None:
        if user.is_active == False:
            raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="User already inactive"
            )
        else:
            return crud.deactivate_user(db=db, user_login=username)
    else:
        raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=f"There's no user with email = {username}"
        )


@router.delete("/{username}/delete", summary = "Delete an user",
               response_description = "Successfully deleted an user.", tags = [Tags.adm_actions_users])
async def delete_user(username: str, current_user: Annotated[schemas.User, Depends(get_current_active_admin),],
                      db: Session = Depends(get_db)) -> JSONResponse:
    """
    Deletes an user account permanently providing **username** (str).

    After deletion, an former user will receive an email to their login email address confirming your action.

    Returns JSONResponse with a success confirmation message or raises a HTTPException if there's no such user.
    """
    user = crud.get_user_by_login(db=db, user_login=username)
    if user is not None:
        template = """
            <html>
            <body>
            

    <p>Hi """+crud.get_user_by_login(db=db, user_login=username).first_name+""",
            <br>We're sorry to hear it, but your account has been deleted.
            <br>Hope to get you in touch in the future.</p>
    
    
            </body>
            </html>
            """
        crud.remove_user(db=db, user_login=username)
        email = schemas.EmailSchema(email=[username])
        message = MessageSchema(
            subject="Your account has been deleted",
            recipients=email.model_dump().get("email"),
            body=template,
            subtype=MessageType.html
            )
    
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code = 200, content={"message": f"user has been deleted. An email has been sent to the {username}."})
    else:
        raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=f"There's no user with email = {username}"
        )