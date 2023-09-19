Module app.main
===============

Functions
---------

    
`authenticate_user(username: str, password: str, db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> app.schemas.User | bool`
:   Checks if user exists and have verified password, then returns the user schema
    
    Args:
        username (str): login (email)
        password (str): password
        db (Session, optional): database session dependency. Defaults to Depends(get_db).
    
    Returns:
        schemas.User | False (couldn't find the user)

    
`login_for_access_token(form_data: typing.Annotated[fastapi.security.oauth2.OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)], db: sqlalchemy.orm.session.Session = Depends(get_db))`
:   - Log in using Authorize button in the top right corner of swagger UI. 
    - User authentication uses OAuth2 password request form to get an access token.
    
    Returns access token.

    
`welcome_to_the_app() ‑> starlette.responses.JSONResponse`
:   Returns JSONResponse