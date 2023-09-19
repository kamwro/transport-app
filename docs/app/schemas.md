Module app.schemas
==================

Classes
-------

`ActivateUser(**data: Any)`
:   Schema for activation code storage
    
    Args:
        UserBase (str): activation code
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `__init__` uses `__pydantic_self__` instead of the more common `self` for the first arg to
    allow `self` as a field name.

    ### Ancestors (in MRO)

    * app.schemas.UserBase
    * pydantic.main.BaseModel

    ### Class variables

    `activation_code: str`
    :

    `model_config`
    :

    `model_fields`
    :

`CreateUser(**data: Any)`
:   Create user schema based on user base schema
    
    Args:
        UserBase (str): password
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `__init__` uses `__pydantic_self__` instead of the more common `self` for the first arg to
    allow `self` as a field name.

    ### Ancestors (in MRO)

    * app.schemas.UserBase
    * pydantic.main.BaseModel

    ### Class variables

    `hashed_password: str`
    :

    `model_config`
    :

    `model_fields`
    :

`EmailSchema(**data: Any)`
:   Email schema based on pydantic BaseModel
    
    Args:
        BaseModel (EmailStr | str)
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `__init__` uses `__pydantic_self__` instead of the more common `self` for the first arg to
    allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `email: List[pydantic.networks.EmailStr | str]`
    :

    `model_config`
    :

    `model_fields`
    :

`Ride(**data: Any)`
:   Schema for default ride info: autoincremented id, calculated price, active status and id of user who took the ride (or will take)
    
    Args:
        RideBase (int | float | bool | None)
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `__init__` uses `__pydantic_self__` instead of the more common `self` for the first arg to
    allow `self` as a field name.

    ### Ancestors (in MRO)

    * app.schemas.RideBase
    * pydantic.main.BaseModel

    ### Class variables

    `Config`
    :   https://docs.pydantic.dev/latest/usage/models/#orm-mode-aka-arbitrary-class-instances

    `id: int`
    :

    `is_active: bool`
    :

    `model_config`
    :

    `model_fields`
    :

    `price: float`
    :

    `user_id_taken: int | None`
    :

`RideBase(**data: Any)`
:   Ride base schema based on pydantic BaseModel
    
    Args:
        BaseModel (str | float | datetime)
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `__init__` uses `__pydantic_self__` instead of the more common `self` for the first arg to
    allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Descendants

    * app.schemas.Ride
    * app.schemas.RideCreate

    ### Class variables

    `departure_date: datetime.datetime`
    :

    `destination_city: str`
    :

    `distance: float`
    :

    `km_fee: float`
    :

    `model_config`
    :

    `model_fields`
    :

    `start_city: str`
    :

`RideCreate(**data: Any)`
:   Create ride schema, actually empty 
        
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `__init__` uses `__pydantic_self__` instead of the more common `self` for the first arg to
    allow `self` as a field name.

    ### Ancestors (in MRO)

    * app.schemas.RideBase
    * pydantic.main.BaseModel

    ### Class variables

    `model_config`
    :

    `model_fields`
    :

`Token(**data: Any)`
:   Token schema based on pydantic BaseModel
    
    Args:
        BaseModel (str)
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `__init__` uses `__pydantic_self__` instead of the more common `self` for the first arg to
    allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `Config`
    :   https://docs.pydantic.dev/latest/usage/models/#orm-mode-aka-arbitrary-class-instances

    `access_token: str`
    :

    `model_config`
    :

    `model_fields`
    :

    `token_type: str`
    :

`TokenData(**data: Any)`
:   Schema containing username attached to the token data
    
    Args:
        BaseModel (str | None)
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `__init__` uses `__pydantic_self__` instead of the more common `self` for the first arg to
    allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `Config`
    :   https://docs.pydantic.dev/latest/usage/models/#orm-mode-aka-arbitrary-class-instances

    `model_config`
    :

    `model_fields`
    :

    `username: str`
    :

`User(**data: Any)`
:   Schema for default user info: autoincremented id and verification status
    
    Args:
        UserBase (int | bool)
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `__init__` uses `__pydantic_self__` instead of the more common `self` for the first arg to
    allow `self` as a field name.

    ### Ancestors (in MRO)

    * app.schemas.UserBase
    * pydantic.main.BaseModel

    ### Class variables

    `Config`
    :   https://docs.pydantic.dev/latest/usage/models/#orm-mode-aka-arbitrary-class-instances

    `id: int`
    :

    `is_active: bool`
    :

    `model_config`
    :

    `model_fields`
    :

`UserBase(**data: Any)`
:   User base schema based on pydantic BaseModel
    
    Args:
        BaseModel (str | bool): basic info about users
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `__init__` uses `__pydantic_self__` instead of the more common `self` for the first arg to
    allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Descendants

    * app.schemas.ActivateUser
    * app.schemas.CreateUser
    * app.schemas.User

    ### Class variables

    `address: str`
    :

    `first_name: str`
    :

    `is_admin: bool`
    :

    `last_name: str`
    :

    `login: str`
    :

    `model_config`
    :

    `model_fields`
    :