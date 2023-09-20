from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from ..utils import Tags
from ..dependencies import get_db, get_current_active_admin
from .. import crud, schemas


router = APIRouter(
    prefix="/rides",
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


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


@router.patch("/{ride_id}/archivise", response_model=schemas.Ride, summary = "Archivise a ride", tags = [Tags.adm_actions_rides])
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


@router.delete("/{ride_id}/delete", response_model=schemas.Ride, summary = "Delete a ride", tags = [Tags.adm_actions_rides])
async def delete_ride(ride_id: int, current_user: Annotated[schemas.User, Depends(get_current_active_admin)],
                      db: Session = Depends(get_db)) -> JSONResponse:
    """Permanently deletes a ride providing **ride_id** (int)

    Returns JSONResponse message about either success or trouble finding such ride.
    """
    ride = crud.get_ride_by_ID(db=db, ride_id=ride_id)
    if ride is not None:
        crud.remove_ride(db=db, ride_id=ride_id)
        return JSONResponse(status_code = 200, content={"message": f"ride with id = {ride_id} successfully deleted."})
    else:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"couldn't find a ride with id = {ride_id}."
        )