import re
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from typing import Annotated
from sqlalchemy.orm import Session
from ..utils import Tags, Envs
from ..dependencies import get_db, get_current_user, get_current_active_user
from .. import crud, schemas


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

    If email address is not valid, the method will raise a HTTPException. That doesn't apply to admin users.

    **Users with the admin status are active by default and thus do not have to activate their account.**

    Returns JSONResponse with user data and confirmation about sending an activation email.
    """
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    user_login_invalid = not re.fullmatch(email_regex, user.login)
    if user_login_invalid and user.is_admin == False:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
            detail="Login is not a valid email address."
        )
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