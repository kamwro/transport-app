from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from typing import Annotated
from sqlalchemy.orm import Session
from ..utils import Tags, Envs
from ..dependencies import get_db, get_current_active_admin
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