Module app.routers.rides
========================

Functions
---------

    
`get_all_rides(current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_user)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> list[app.schemas.Ride]`
:   Gets list of all active rides.

    
`get_all_rides_by_destination_city(destination_city: str, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_user)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> list[app.schemas.Ride]`
:   Gets list of all active rides to **destination_city** (str).

    
`get_all_rides_by_starting_city(start_city: str, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_user)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> list[app.schemas.Ride]`
:   Gets list of all active rides from **start_city** (str).

    
`get_all_rides_from_one_city_to_another(start_city: str, destination_city: str, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_user)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> list[app.schemas.Ride]`
:   Gets list of all active rides from **start_city** (str) to **destination_city** (str).

    
`reserve_ride(ride_id: int, current_user: typing.Annotated[app.schemas.User, Depends(get_current_active_user)], db: sqlalchemy.orm.session.Session = Depends(get_db)) ‑> starlette.responses.JSONResponse`
:   Reserves a ride providing **ride_id** (int) - user can get it, viewing rides at the GET /rides/ endpoints.
    
    After the booking process, the ride will be archivised and have id of current user bound to it.
    In addition, the user will have all the ride details mailed to him.
    
    Returns JSONResponse with the success confirmation message or raises HTTPException if there's no such ride.