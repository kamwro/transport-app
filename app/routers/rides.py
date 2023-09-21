from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from ..utils import Tags, EmailUtils
from ..dependencies import get_db, get_current_active_user
from .. import crud, schemas


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
        )
    if ride.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="The ride is no longer active."
        )
    crud.archivise_ride(db=db, ride_id=ride_id, user_id_taken=current_user.id)
    await EmailUtils.send_booking_confirmation_email(user=current_user, ride=ride)
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
async def get_all_rides_by_destination_city(destination_city: str, current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                        db: Session = Depends(get_db)) -> list[schemas.Ride]:
    """Gets list of all active rides to **destination_city** (str).
    """
    return crud.get_rides_by_destination_city(db=db, destination_city=destination_city)


@router.get("/{start_city}/{destination_city}", response_model=list[schemas.Ride], summary = "Show all available rides from one city to another", tags = [Tags.rides])
async def get_all_rides_from_one_city_to_another(start_city: str, destination_city: str, current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                        db: Session = Depends(get_db)) -> list[schemas.Ride]:
    """Gets list of all active rides from **start_city** (str) to **destination_city** (str).
    """
    return crud.get_rides_by_cities(db=db, start_city=start_city, destination_city=destination_city)