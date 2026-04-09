from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.locations import Location, BaseLocation as CreateLocation
from api.depends import (
    get_all_locations_use_case,
    get_location_by_id_use_case,
    create_location_use_case,
    delete_location_use_case,
    get_location_by_name_use_case
)
from core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
    LocationNameIsNotUniqueException,
    LocationNotFoundByNameException,
)

locations_router = APIRouter()


@locations_router.get("/", status_code=status.HTTP_200_OK, response_model=List[Location])
async def get_all_locations(
    use_case = Depends(get_all_locations_use_case)
) -> List[Location]:
    locations = await use_case.execute()
    return locations


@locations_router.get("/id/{location_id}", status_code=status.HTTP_200_OK, response_model=Location)
async def get_location_by_id(
    location_id: int,
    use_case = Depends(get_location_by_id_use_case)
) -> Location:
    try:
        location = await use_case.execute(location_id=location_id)
        return location
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

@locations_router.get("/name/{name}", status_code=status.HTTP_200_OK, response_model=Location)
async def get_location_by_name(
    name: str,
    use_case = Depends(get_location_by_name_use_case)
) -> Location:
    try:
        location = await use_case.execute(name=name)
        return location
    except LocationNotFoundByNameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )

@locations_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Location)
async def create_location(
    location_data: CreateLocation,
    use_case = Depends(create_location_use_case)
) -> Location:
    try:
        return await use_case.execute(location_data=location_data)
    except LocationNameIsNotUniqueException as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@locations_router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    use_case = Depends(delete_location_use_case)
) -> None:
    try:
        await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )