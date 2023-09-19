Module app.utils
================

Classes
-------

`EmailUtils()`
:   Class container for email utils, like methods sending emails

    ### Class variables

    `conf`
    :

    ### Static methods

    `is_email_valid(username: str) ‑> bool`
    :   Validates an email address using regex
        
        Args:
            username (str): email to validate
        
        Returns:
            bool: is the email valid

    `send_activation_link(user: app.schemas.User)`
    :   Sends an activation link to the user email
        
        Args:
            user (User): user

    `send_deletion_email(user: app.schemas.User)`
    :   Sends an deletion confirmation to the user email
        
        Args:
            user (User): user

    `send_self_deletion_email(user: app.schemas.User)`
    :   Sends an deletion confirmation to the user email
        
        Args:
            user (User): user

`Envs()`
:   Environmental variables

    ### Class variables

    `ACCESS_TOKEN_EXPIRE_MINUTES`
    :

    `ALGORITHM`
    :

    `MAIL_FROM`
    :

    `MAIL_PASSWORD`
    :

    `MAIL_PORT`
    :

    `MAIL_SERVER`
    :

    `MAIL_USERNAME`
    :

    `SECRET_KEY`
    :

`SecurityUtils()`
:   Security utils static functions and pwd_context for cryptograhics

    ### Class variables

    `pwd_context`
    :

    ### Static methods

    `create_access_token(data: dict, expires_delta: datetime.timedelta | None = None) ‑> str`
    :   Gets an access token
        
        Args:
            data (dict): key:value pair of "sub":user login
            expires_delta (timedelta | None, optional): time until the token expires. Defaults to None.
        
        Returns:
            str: access token

    `get_password_hash(password: str) ‑> str`
    :   Gets a password hash
        
        Args:
            password (str): plain password
        
        Returns:
            str: password hash

    `verify_password(plain_password: str, hashed_password: str) ‑> bool`
    :   Checks if plain password matches hashed password
        
        Args:
            plain_password (str): plain password
            hashed_password (str): hashed password
        
        Returns:
            bool: plain password == hashed password

`Tags(*args, **kwds)`
:   Tags for API endpoints
    
    Args:
        Enum (str): tags

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `acc_create`
    :

    `acc_login`
    :

    `adm_actions_rides`
    :

    `adm_actions_users`
    :

    `my_acc`
    :

    `rides`
    :