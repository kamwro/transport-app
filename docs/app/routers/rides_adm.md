Module app.routers.rides_adm
============================

Functions
---------

    
`archivise_ride(ride_id: int, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_admin)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> app.schemas.Ride`
:   Archivises a ride providing **ride_id** (int)
    
    Returns archivised ride or raises HTTPException if there's no such ride or ride already innactive.

    
`create_ride(ride: app.schemas.RideCreate, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_admin)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> app.schemas.Ride`
:   Creates a ride, providing information:
    - **start_city** (str): a city from which the ride starts,
    - **destination_city** (str): a city in which the ride ends,
    - **distance** (float): total trip distance measured in kilometers,
    - **km_fee** (float): amount of currency per kilometer,
    - **departure_date** (datetime): the departure date, accepted format: **YYYY/MM/DD HH:MM** (%Y/%m/%d %H:%M)

    
`delete_ride(ride_id: int, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_admin)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> starlette.responses.JSONResponse`
:   Permanently deletes a ride providing **ride_id** (int)
    
    Returns JSONResponse message about either success or trouble finding such ride.