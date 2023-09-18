import random
from sqlalchemy import and_
from sqlalchemy.orm import Session
from .utils import SecurityUtils
from . import models, schemas


def get_user_by_ID (db: Session, user_id: int) -> schemas.User:
    """Gets an User object providing user id

    Args:
        db (Session): database session
        user_id (int): user ID

    Returns:
        schemas.User
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


def get_user_by_login (db: Session, user_login: str) -> schemas.User:
    """Gets an User object providing user login

    Args:
        db (Session): database session
        user_login (str): user login

    Returns:
        schemas.User
    """
    user = db.query(models.User).filter(models.User.login == user_login).first()
    return user


def create_user(db: Session, user: schemas.CreateUser) -> schemas.User:
    """Creates an User object based on the CreateUser schema.
    Activation code is created based on the pseudorandom algorithm.

    Args:
        db (Session): database session
        user (schemas.CreateUser): user creation schema object

    Returns:
        schemas.User
    """
    user = models.User(login = user.login, first_name = user.first_name,
                       last_name = user.last_name, address = user.address,
                        hashed_password =  SecurityUtils.get_password_hash(user.hashed_password),
                        is_admin = user.is_admin, is_active = user.is_admin,
                        activation_code = user.last_name[-1]+str(random.randint(1,10))+user.login[0]+user.address[-1]+str(random.randint(1,6539)))
    db.add(user)
    db.commit()
    db.refresh(user)
    return schemas.User.from_orm(user)


def remove_user(db: Session, user_login: str):
    """Removes user from database providing user login

    Args:
        db (Session): database session
        user_login (str): user login
    """    
    user = get_user_by_login(db, user_login)
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        print(f"{type(e)} - there is no user.")


def activate_user(db: Session, user_login: str) -> schemas.User:
    """Activates a user providing user login

    Args:
        db (Session): database session
        user_login (str): user login
    Raises:
        ValueError: if login doesnt match any of the users

    Returns:
        schemas.User
    """
    user = get_user_by_login(db, user_login)
    if user != None:
        user.is_active = True
        db.commit()
    return user

        
def deactivate_user(db: Session, user_login: str) -> schemas.User:
    """Deactivates a user providing user login

    Args:
        db (Session): database session
        user_login (str): user login
    Raises:
        ValueError: if login doesnt match any of the users

    Returns:
        schemas.User
    """
    user = get_user_by_login(db, user_login)
    user.is_active = False
    if user != None:
        db.commit()
    return user


def grant_admin_status(db: Session, user_login: str) -> schemas.User:
    """Grants the admin status to an user providing user login

    Args:
        db (Session): database session
        user_login (str): user login

    Returns:
        schemas.User
    """
    user = get_user_by_login(db, user_login)
    if user is not None:
        user.is_admin = True
        db.commit()
    return user


def remove_admin_status(db: "Session", user_login: str) -> schemas.User:
    """Takes the admin status from an user providing user login

    Args:
        db (Session): database session
        user_login (str): user login

    Returns:
        schemas.User
    """
    user = get_user_by_login(db, user_login)
    if user is not None:
        user.is_admin = False
        db.commit()
    return user
    
#rides

def get_ride_by_ID (db: "Session", ride_id: int) -> schemas.Ride:
    """Gets ride providing ride id

    Args:
        db (Session): database session
        ride_id (int): ride id

    Returns:
        schemas.Ride
    """
    ride = db.query(models.Ride).filter(models.Ride.id == ride_id).first()
    return ride
    

def get_rides_by_start_city(db: Session, start_city: str) -> schemas.Ride:
    """Gets all active rides from a given city

    Args:
        db (Session): database session
        start_city (str): starting city

    Returns:
        schemas.Ride
    """
    rides = db.query(models.Ride).filter(and_(models.Ride.start_city == start_city, models.Ride.is_active == True)).all()
    return rides


def get_rides_by_destination_city(db: Session, destination_city: str) -> schemas.Ride:
    """Gets all active rides to a given city

    Args:
        db (Session): database session
        destination_city (str): destination city

    Returns:
        schemas.Ride
    """
    rides = db.query(models.Ride).filter(and_(models.Ride.destination_city == destination_city, models.Ride.is_active == True)).all()
    return rides


def get_rides_by_cities(db: Session, start_city: str, destination_city: str) -> schemas.Ride:
    """Gets all active rides from a given city to a second given city

    Args:
        db (Session): database session
        start_city (str): starting city
        destination_city (str): destination city

    Returns:
        schemas.Ride
    """
    rides = db.query(models.Ride).filter(and_(models.Ride.destination_city == destination_city,
                                        models.Ride.start_city == start_city,models.Ride.is_active == True)).all()
    return rides


def get_all_rides(db: Session, skip: int = 0, limit: int = 50) -> schemas.Ride:
    """Gets all active rides. Optionally providing offset and limit values

    Args:
        db (Session): database session
        skip (int, optional): skips x first records. Defaults to 0.
        limit (int, optional): limits to x records. Defaults to 50.

    Returns:
        schemas.Ride
    """
    rides = db.query(models.Ride).filter(models.Ride.is_active == True).offset(skip).limit(limit).all()
    return rides
    

def create_ride(db: Session, new_ride: schemas.RideCreate) -> schemas.Ride:
    """Creates a ride based on the RideCreate schema

    Args:
        db (Session): database session
        new_ride (schemas.RideCreate): new ride

    Returns:
        schemas.Ride
    """
    ride = models.Ride(start_city = new_ride.start_city, destination_city = new_ride.destination_city,
                       distance = new_ride.distance, km_fee = new_ride.km_fee,
                       departure_date = new_ride.departure_date, price = round(new_ride.km_fee * new_ride.distance, 2),
                       is_active = True, user_id_taken = None)
    db.add(ride)
    db.commit()
    db.refresh(ride)
    return schemas.Ride.from_orm(ride)


def archivise_ride(db: Session, ride_id: int, user_id_taken: int) -> schemas.Ride:
    """Archivises a ride and binds it with id of the user who booked it providing ride id

    Args:
        db (Session): database session
        ride_id (int): ride id
        user_id_taken (int): id of the user who booked the ride

    Returns:
        schemas.Ride
    """
    ride = db.query(models.Ride).filter(models.Ride.id == ride_id).first()
    if ride != None:
        ride.is_active = False
        ride.user_id_taken = user_id_taken
        db.commit()
    return ride


def remove_ride(db: Session, ride_id: int):
    """Removing a ride from the database providing ride id

    Args:
        db (Session): database session
        ride_id (int): ride id
    """
    ride = db.query(models.Ride).filter(models.Ride.id == ride_id).first()
    if ride != None:
        db.delete(ride)
        db.commit()