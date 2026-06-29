from fastapi import status, HTTPException, Depends, APIRouter

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from schemas import UserCreate, UserResponse, UserUpdate
from database import get_database
import models

# ------- SETUP -------
router = APIRouter()

# ------- ENDPOINTS -------
@router.post(
    "",
    response_model = UserResponse,
    status_code = status.HTTP_201_CREATED
)
async def create_user(user_info: UserCreate, database: Annotated[AsyncSession, Depends(get_database)]):
    result = await database.execute(
        select(models.User)
        .where(models.User.username == user_info.username)
    )
    existing_username = result.scalars().first()

    if existing_username:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"username '{user_info.username}' already exists"
        )
    
    result = await database.execute(
        select(models.User)
        .where(models.User.email == user_info.email)
    )
    existing_email = result.scalars().first()

    if existing_email:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"email '{user_info.email}' already exists"
        )

    new_user = models.User(
        username = user_info.username,
        email = user_info.email,
        created_at = datetime.now()
    )

    database.add(new_user)
    await database.commit()
    await database.refresh(new_user)

    return new_user

@router.delete(
    "/{user_id}",
    status_code = status.HTTP_204_NO_CONTENT
)
async def delete_user(user_id: int, database: Annotated[AsyncSession, Depends(get_database)]):
    result = await database.execute(
        select(models.User)
        .where(models.User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"user with ID of {user_id} not found"
        )
    
    await database.delete(user)
    await database.commit()

@router.patch(
    "/{user_id}",
    response_model = UserResponse,
    status_code = status.HTTP_200_OK
)
async def update_user(user_id: int, updated_info: UserUpdate, database: Annotated[AsyncSession, Depends(get_database)]):
    result = await database.execute(
        select(models.User)
        .where(models.User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"user with ID of {user_id} not found"
        )
    
    if updated_info.username is not None:
        result = await database.execute(
            select(models.User)
            .where(models.User.username == updated_info.username)
        )
        existing_username = result.scalars().first()

        if existing_username:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = f"username '{updated_info.username}' already exists"
            )
    
    if updated_info.email is not None:
        result = await database.execute(
            select(models.User)
            .where(models.User.email == updated_info.email)
        )
        existing_email = result.scalars().first()

        if existing_email:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = f"email '{updated_info.email}' already exists"
            )

    update_data = updated_info.model_dump(exclude_unset = True)

    for field, value in update_data.items():
        setattr(user, field, value)

    await database.commit()
    await database.refresh(user)
    
    return user

@router.get(
    "",
    response_model = list[UserResponse]
)
async def get_all_users(database: Annotated[AsyncSession, Depends(get_database)]):
    result = await database.execute(select(models.User))
    users = result.scalars().all()

    return users

@router.get(
    "/{user_id}",
    response_model = UserResponse
)
async def get_specific_user(user_id: int, database: Annotated[AsyncSession, Depends(get_database)]):
    result = await database.execute(
        select(models.User)
        .where(models.User.id == user_id)
    )
    user = result.scalars().first()

    if user: return user
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"user with ID of {user_id} not found"
    )