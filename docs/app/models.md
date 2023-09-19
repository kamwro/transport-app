Module app.models
=================

Classes
-------

`Ride(**kwargs)`
:   Sqlalchemy model of Ride table based on the database sqlalchemic declarative_base()
        
    
    A simple constructor that allows initialization from kwargs.
    
    Sets attributes on the constructed instance using the names and
    values in ``kwargs``.
    
    Only keys that are present as
    attributes of the instance's class are allowed. These could be,
    for example, any mapped columns or relationships.

    ### Ancestors (in MRO)

    * sqlalchemy.orm.decl_api.Base

    ### Instance variables

    `departure_date`
    :

    `destination_city`
    :

    `distance`
    :

    `id`
    :

    `is_active`
    :

    `km_fee`
    :

    `price`
    :

    `start_city`
    :

    `user_id_taken`
    :

`User(**kwargs)`
:   Sqlalchemy model of User table based on the database sqlalchemic declarative_base()
        
    
    A simple constructor that allows initialization from kwargs.
    
    Sets attributes on the constructed instance using the names and
    values in ``kwargs``.
    
    Only keys that are present as
    attributes of the instance's class are allowed. These could be,
    for example, any mapped columns or relationships.

    ### Ancestors (in MRO)

    * sqlalchemy.orm.decl_api.Base

    ### Instance variables

    `activation_code`
    :

    `address`
    :

    `first_name`
    :

    `hashed_password`
    :

    `id`
    :

    `is_active`
    :

    `is_admin`
    :

    `last_name`
    :

    `login`
    :