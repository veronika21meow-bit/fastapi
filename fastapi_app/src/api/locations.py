from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from schemas.locations import Location
from api.depends import (
    get_all_locations_use_case,
    get_location_by_id_use_case,
    create_location_use_case,
    delete_location_use_case,
    update_location_use_case,
    get_location_by_name_use_case
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
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Локация с id '{location_id}' не найдена"
            )
        return location
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@locations_router.get("/name/{name}", status_code=status.HTTP_200_OK, response_model=Location)
async def get_location_by_name(
    name: str,
    use_case = Depends(get_location_by_name_use_case)
) -> Location:
    try:
        location = await use_case.execute(name=name)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Локация с именем '{name}' не найдена"
            )
        return location
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@locations_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Location)
async def create_location(
    name: str, is_published: bool = True,
    use_case = Depends(create_location_use_case)
) -> Location:
    try:
        location = await use_case.execute(
            name=name,
            is_published=is_published
        )
        return location
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@locations_router.put("/{location_id}", status_code=status.HTTP_200_OK, response_model=Location)
async def update_location(
    location_id: int,
    location_data: Location,
    use_case = Depends(update_location_use_case)
) -> Location:
    try:
        location = await use_case.execute(
            id=location_id,
            name=location_data.name
        )
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Локация с id '{location_id}' не найдена"
            )
        return location
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )


@locations_router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    use_case = Depends(delete_location_use_case)
) -> None:
    try:
        result = await use_case.execute(location_id=location_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Локация с id '{location_id}' не найдена"
            )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )