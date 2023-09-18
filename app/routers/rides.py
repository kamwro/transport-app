import os
from dotenv import load_dotenv
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from typing import Annotated
from sqlalchemy.orm import Session
from .users import get_current_active_user, get_current_active_admin
from ..utils import Tags
from ..dependencies import get_db
from .. import crud, schemas


load_dotenv("./.env")

class Envs:
   """Environmental variables
   """   
   MAIL_USERNAME=os.getenv('MAIL_USERNAME')
   MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
   MAIL_FROM = os.getenv('MAIL_FROM')
   MAIL_PORT=os.getenv('MAIL_PORT')
   MAIL_SERVER=os.getenv('MAIL_SERVER')

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
    prefix="/rides",
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@router.post("/{ride_id}/reserve", summary= "Book an available ride", tags = [Tags.rides])
async def reserve_ride(ride_id: int, current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                        db: Session = Depends(get_db)) -> JSONResponse:
    """Reserves a ride providing **ride_id** (int) - user can get it, viewing rides at the GET /rides/ endpoints.

    After the booking process, the ride will be archivised and have id of current user bound to it.
    In addition, the user will have all the ride details mailed to him.

    Returns JSONResponse with the success confirmation message or raises HTTPException if there's no such ride.
    """
    ride = crud.get_ride_by_ID(db=db, ride_id=ride_id)
    if ride is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Can't find any ride with id = {ride_id}."
            # headers={"WWW-Authenticate": "Bearer"},
        )
    if ride.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="The ride is no longer active."
        )
    crud.archivise_ride(db=db, ride_id=ride_id, user_id_taken=current_user.id)
    template = """
        <html>
        <body>
         
 
<p>Hi """+current_user.first_name+""",
        <br>Here are the details regarding your reserved ride: </p>
        <br>
        <strong> From: </strong> """+ride.start_city+""" <br>
        <strong> To: </strong> """+ride.destination_city+""" <br>
        <strong> Distance (km): </strong> """+str(ride.distance)+""" <br>
        <strong> Fee per km: </strong> """+str(ride.km_fee)+""" <br>
        <strong> Total price: </strong> """+str(ride.price)+""" <br>
        <strong> Departure date: </strong> """+ride.departure_date.strftime('%y-%m-%d %H:%M')+""" <br>
        <br>
        <p> Thank you for using our services. </p>
 
 
        </body>
        </html>
        """
    email = schemas.EmailSchema(email=[current_user.login])
    message = MessageSchema(
        subject=f"Your ride from {ride.start_city} to {ride.destination_city}",
        recipients=email.model_dump().get("email"),
        body=template,
        subtype=MessageType.html
        )
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": f"The ride was booked successfully and a detailed email has been sent to {current_user.login}"})
    

@router.get("/", response_model=list[schemas.Ride], summary = "Show available rides", tags = [Tags.rides])
async def get_all_rides(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                        db: Session = Depends(get_db)) -> list[schemas.Ride]:
    """Gets list of all active rides.
    """
    return crud.get_all_rides(db=db)

@router.get("/{start_city}/", response_model=list[schemas.Ride], summary = "Show available rides from specific city", tags = [Tags.rides])
async def get_all_rides_by_starting_city(start_city: str, current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                        db: Session = Depends(get_db)) -> list[schemas.Ride]:
    """Gets list of all active rides from **start_city** (str).
    """
    return crud.get_rides_by_start_city(db=db, start_city=start_city)

@router.get("/all/{destination_city}", response_model=list[schemas.Ride], summary = "Show available rides to specific city", tags = [Tags.rides])
async def get_all_rides_by_starting_city(destination_city: str, current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                        db: Session = Depends(get_db)) -> list[schemas.Ride]:
    """Gets list of all active rides to **destination_city** (str).
    """
    return crud.get_rides_by_destination_city(db=db, destination_city=destination_city)

@router.get("/{start_city}/{destination_city}", response_model=list[schemas.Ride], summary = "Show all available rides from one city to another", tags = [Tags.rides])
async def get_all_rides_by_starting_city(start_city: str, destination_city: str, current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                        db: Session = Depends(get_db)) -> list[schemas.Ride]:
    """Gets list of all active rides from **start_city** (str) to **destination_city** (str).
    """
    return crud.get_rides_by_cities(db=db, start_city=start_city, destination_city=destination_city)

#admin

@router.post("/", response_model=schemas.Ride, summary = "Create a ride", tags = [Tags.adm_actions_rides])
async def create_ride(ride: schemas.RideCreate, current_user: Annotated[schemas.User, Depends(get_current_active_admin)],
                      db: Session = Depends(get_db)) -> schemas.Ride:
    """
    Creates a ride, providing information:
    - **start_city** (str): a city from which the ride starts,
    - **destination_city** (str): a city in which the ride ends,
    - **distance** (float): total trip distance measured in kilometers,
    - **km_fee** (float): amount of currency per kilometer,
    - **departure_date** (datetime): the departure date, accepted format: **YYYY/MM/DD HH:MM** (%Y/%m/%d %H:%M)
    """
    return crud.create_ride(db=db, new_ride=ride)

@router.patch("/{ride_id}/archivise", response_model=schemas.Ride, summary = "Archivise a ride.", tags = [Tags.adm_actions_rides])
async def archivise_ride(ride_id: int, current_user: Annotated[schemas.User, Depends(get_current_active_admin)],
                      db: Session = Depends(get_db)) -> schemas.Ride:
    """Archivises a ride providing **ride_id** (int)

    Returns archivised ride or raises HTTPException if there's no such ride or ride already innactive.
    """
    ride = crud.get_ride_by_ID(db=db, ride_id=ride_id)
    if ride is not None:
        if ride.is_active == True:
            return crud.archivise_ride(db=db, ride_id=ride_id, user_id_taken=-1)
        else:
            raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="ride already deactivated."
        )
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"couldn't find a ride with id = {ride_id}"
        )

@router.delete("/{ride_id}/delete", response_model=schemas.Ride, summary = "Delete a ride.", tags = [Tags.adm_actions_rides])
async def delete_ride(ride_id: int, current_user: Annotated[schemas.User, Depends(get_current_active_admin)],
                      db: Session = Depends(get_db)) -> JSONResponse:
    """Permanently deletes a ride providing **ride_id** (int)

    Returns JSONResponse message about either success or trouble finding such ride.
    """
    ride = crud.get_ride_by_ID(db=db, ride_id=ride_id)
    if ride is not None:
        crud.remove_ride(db=db, ride_id=ride_id)
        return JSONResponse(status_code = 200, content={"message: ": f"ride with id = {ride_id} successfully deleted."})
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"couldn't find a ride with id = {ride_id}."
        )