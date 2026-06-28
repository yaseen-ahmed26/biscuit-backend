# ------- IMPORTS -------
from fastapi import FastAPI, status, HTTPException, Request, Depends
from fastapi_swagger_ui_theme import setup_swagger_ui_theme

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from typing import Annotated

from database import Base, get_database, engine
from schemas import UserCreate, UserResponse, UserUpdate
import models

# ------- SETUP -------
app = FastAPI(docs_url = None)

Base.metadata.create_all(bind = engine)

# Dark Mode
setup_swagger_ui_theme(
    app, 
    docs_path = "/docs", 
    title = "Swagger Docs"
)

# ------- HOME -------
@app.get("/", include_in_schema = False)
def home():
    return {"message": "Biscuit Backend is running"}

# ------- (Temporary) USERS -------
@app.post(
    "/api/users",
    response_model = UserResponse,
    status_code = status.HTTP_201_CREATED
)
def create_user(user_info: UserCreate, database: Annotated[Session, Depends(get_database)]):
    new_user = models.User(
        username = user_info.username,
        email = user_info.email,
        created_at = datetime.now()
    )

    database.add(new_user)
    database.commit()
    database.refresh(new_user)

    return new_user

@app.delete(
    "/api/users/{user_id}",
    status_code = status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int, database: Annotated[Session, Depends(get_database)]):
    result = database.execute(
        select(models.User)
        .where(models.User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"user with ID of {user_id} not found"
        )
    
    database.delete(user)
    database.commit()

@app.patch(
    "/api/users/{user_id}",
    response_model = UserResponse,
    status_code = status.HTTP_200_OK
)
def update_user(user_id: int, updated_info: UserUpdate, database: Annotated[Session, Depends(get_database)]):
    result = database.execute(
        select(models.User)
        .where(models.User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"user with ID of {user_id} not found"
        )

    update_data = updated_info.model_dump(exclude_unset = True)

    for field, value in update_data.items():
        setattr(user, field, value)

    database.commit()
    database.refresh(user)
    
    return user

@app.get(
    "/api/users",
    response_model = list[UserResponse]
)
def get_all_users(database: Annotated[Session, Depends(get_database)]):
    result = database.execute(select(models.User))
    users = result.scalars().all()

    return users

@app.get(
    "/api/users/{user_id}",
    response_model = UserResponse
)
def get_specific_user(user_id: int, database: Annotated[Session, Depends(get_database)]):
    result = database.execute(
        select(models.User)
        .where(models.User.id == user_id)
    )
    user = result.scalars().first()

    if user: return user
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"user with ID of {user_id} not found"
    )