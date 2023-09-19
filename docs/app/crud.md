Module app.crud
===============

Functions
---------

    
`activate_user(db: sqlalchemy.orm.session.Session, user_login: str) ‑> app.schemas.User`
:   Activates an user providing user login
    
    Args:
        db (Session): database session
        user_login (str): user login
    Raises:
        ValueError: if login doesnt match any of the users
    
    Returns:
        schemas.User

    
`archivise_ride(db: sqlalchemy.orm.session.Session, ride_id: int, user_id_taken: int) ‑> app.schemas.Ride`
:   Archivises a ride and binds it with id of the user who booked it providing ride id
    
    Args:
        db (Session): database session
        ride_id (int): ride id
        user_id_taken (int): id of the user who booked the ride
    
    Returns:
        schemas.Ride

    
`create_ride(db: sqlalchemy.orm.session.Session, new_ride: app.schemas.RideCreate) ‑> app.schemas.Ride`
:   Creates a ride based on the RideCreate schema
    
    Args:
        db (Session): database session
        new_ride (schemas.RideCreate): new ride
    
    Returns:
        schemas.Ride

    
`create_user(db: sqlalchemy.orm.session.Session, user: app.schemas.CreateUser) ‑> app.schemas.User`
:   Creates an User object based on the CreateUser schema.
    Activation code is created based on the pseudorandom algorithm.
    
    Args:
        db (Session): database session
        user (schemas.CreateUser): user creation schema object
    
    Returns:
        schemas.User

    
`deactivate_user(db: sqlalchemy.orm.session.Session, user_login: str) ‑> app.schemas.User`
:   Deactivates an user providing user login
    
    Args:
        db (Session): database session
        user_login (str): user login
    Raises:
        ValueError: if login doesnt match any of the users
    
    Returns:
        schemas.User

    
`get_all_rides(db: sqlalchemy.orm.session.Session, skip: int = 0, limit: int = 50) ‑> app.schemas.Ride`
:   Gets all active rides. Optionally providing offset and limit values
    
    Args:
        db (Session): database session
        skip (int, optional): skips x first records. Defaults to 0.
        limit (int, optional): limits to x records. Defaults to 50.
    
    Returns:
        schemas.Ride

    
`get_ride_by_ID(db: Session, ride_id: int) ‑> app.schemas.Ride`
:   Gets ride providing ride id
    
    Args:
        db (Session): database session
        ride_id (int): ride id
    
    Returns:
        schemas.Ride

    
`get_rides_by_cities(db: sqlalchemy.orm.session.Session, start_city: str, destination_city: str) ‑> app.schemas.Ride`
:   Gets all active rides from a given city to a second given city
    
    Args:
        db (Session): database session
        start_city (str): starting city
        destination_city (str): destination city
    
    Returns:
        schemas.Ride

    
`get_rides_by_destination_city(db: sqlalchemy.orm.session.Session, destination_city: str) ‑> app.schemas.Ride`
:   Gets all active rides to a given city
    
    Args:
        db (Session): database session
        destination_city (str): destination city
    
    Returns:
        schemas.Ride

    
`get_rides_by_start_city(db: sqlalchemy.orm.session.Session, start_city: str) ‑> app.schemas.Ride`
:   Gets all active rides from a given city
    
    Args:
        db (Session): database session
        start_city (str): starting city
    
    Returns:
        schemas.Ride

    
`get_user_by_ID(db: sqlalchemy.orm.session.Session, user_id: int) ‑> app.schemas.User`
:   Gets an User object providing user id
    
    Args:
        db (Session): database session
        user_id (int): user ID
    
    Returns:
        schemas.User

    
`get_user_by_login(db: sqlalchemy.orm.session.Session, user_login: str) ‑> app.schemas.User`
:   Gets an User object providing user login
    
    Args:
        db (Session): database session
        user_login (str): user login
    
    Returns:
        schemas.User

    
`grant_admin_status(db: sqlalchemy.orm.session.Session, user_login: str) ‑> app.schemas.User`
:   Grants the admin status to an user providing user login
    
    Args:
        db (Session): database session
        user_login (str): user login
    
    Returns:
        schemas.User

    
`remove_admin_status(db: Session, user_login: str) ‑> app.schemas.User`
:   Takes the admin status from an user providing user login
    
    Args:
        db (Session): database session
        user_login (str): user login
    
    Returns:
        schemas.User

    
`remove_ride(db: sqlalchemy.orm.session.Session, ride_id: int)`
:   Removing a ride from the database providing ride id
    
    Args:
        db (Session): database session
        ride_id (int): ride id

    
`remove_user(db: sqlalchemy.orm.session.Session, user_login: str)`
:   Removes user from database providing user login
    
    Args:
        db (Session): database session
        user_login (str): user login