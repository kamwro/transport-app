Module app.dependencies
=======================

Functions
---------

    
`get_current_active_admin(current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_user)]) ‑> app.schemas.User`
:   Creates an admin dependency based on the active user dependency (get_current_active_user). 
    
    Args:
        current_user (Annotated[schemas.User, Depends): depended on get_current_active_user
    
    Raises:
        HTTPException: when the current user is not an admin
    
    Returns:
        schemas.User: an admin

    
`get_current_active_user(current_user: typing.Annotated[app.schemas.User, Depends(get_current_user)]) ‑> app.schemas.User`
:   Creates an active user dependency based on the user dependency (get_current_user). 
    
    Args:
        current_user (Annotated[schemas.User, Depends): depended on get_current_user
    Raises:
        HTTPException: if user is inactive
    
    Returns:
        schemas.User: current active user

    
`get_current_user(token: typing.Annotated[str, Depends(OAuth2PasswordBearer)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> app.schemas.User`
:   Creates an user dependency based on a token and database session dependency.
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

    
`get_db()`
:   Tries to yield database session maker and closes it in any case
    
    Yields:
        Iterator[SessionLocal]

    
`override_get_db()`
:   Tries to yield in-memory database session maker and closes it in any case
    
    Yields:
        Iterator[SessionLocal]

Classes
-------

`Envs()`
:   Environmental variables

    ### Class variables

    `ALGORITHM`
    :

    `SECRET_KEY`
    :