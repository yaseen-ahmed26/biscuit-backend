# ------- IMPORTS -------
from fastapi import FastAPI, status, HTTPException
from fastapi_swagger_ui_theme import setup_swagger_ui_theme

from datetime import datetime

from schemas import UserCreate, UserResponse, UserUpdate

# Temporary
users: list[dict] = [
    {
        "id": 1,
        "username": "corporal.chicken",
        "email": "yaseen@example.com",
        "created_at": datetime.today()
    },
    {
        "id": 2,
        "username": "chocolate_biscuit",
        "email": "choco.biscuit@example.com",
        "created_at": datetime.today()
    }
]

# ------- SETUP -------
app = FastAPI(docs_url = None)

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
def create_user(user: UserCreate):
    new_id = max(p["id"] for p in users) + 1 if users else 1

    new_user = {
        "id": new_id,
        "username": user.username,
        "email": user.email,
        "created_at": datetime.today(),
    }

    users.append(new_user)

    return new_user

@app.delete(
    "/api/users/{user_id}",
    status_code = status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int):
    for user in users:
        if user.get("id") == user_id:
            users.remove(user)

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"user with ID of {user_id} not found"
    )

@app.patch(
    "/api/users/{user_id}",
    response_model = UserResponse,
    status_code = status.HTTP_200_OK
)
def update_user(user_id: int, updated_info: UserUpdate):
    found_user = None

    for user in users:
        if user.get("id") == user_id:
            found_user = user
            break

    if found_user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"user with ID of {user_id} not found"
        )

    if updated_info.username is not None:
        found_user["username"] = updated_info.username
    if updated_info.email is not None:
        found_user["email"] = updated_info.email

    return found_user

@app.get(
    "/api/users",
    response_model = list[UserResponse]
)
def get_all_users():
    return users

@app.get(
    "/api/users/{user_id}",
    response_model = UserResponse
)
def get_specific_user(user_id: int):
    for user in users:
        if user.get("id") == user_id:
            return user
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"user with ID of {user_id} not found"
    )