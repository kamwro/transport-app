Module app.routers.users_adm
============================

Functions
---------

    
`activate_user(username: str, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_admin)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> app.schemas.User`
:   Activate an user account providing **username** (str).
    Could be handy with problems with the email service.
    
    Returns an User object or raises a HTTPException if user is already active or there's no such user.

    
`deactivate_user(username: str, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_admin)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> app.schemas.User`
:   Deactivates an user account providing **username** (str).
    
    Returns an User object or raises a HTTPException if user is already inactive or there's no such user.

    
`delete_user(username: str, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_admin)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> starlette.responses.JSONResponse`
:   Deletes an user account permanently providing **username** (str).
    
    After deletion, an former user will receive an email to their login email address confirming your action.
    
    Returns JSONResponse with a success confirmation message or raises a HTTPException if there's no such user.

    
`grant_adm(username: str, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_admin)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> app.schemas.User`
:   Grants an user the admin status providing **username** (str). 
    
    Returns an User object or raises a HTTPException if user is already an admin or there's no such user.

    
`remove_adm(username: str, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_admin)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> app.schemas.User`
:   Takes the admin status from an user providing **username** (str).
    
    Returns an User object or raises a HTTPException if user is already not an admin or there's no such user.

    
`view_user_info(username: str, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_admin)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> app.schemas.User`
:   Views an user info providing **username** (str). 
    Hashed password and verification code won't be showed.
    
    Returns an User object or raises a HTTPException when there's no such user.