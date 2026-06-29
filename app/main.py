# ------- IMPORTS -------
from fastapi import FastAPI
from fastapi_swagger_ui_theme import setup_swagger_ui_theme

from contextlib import asynccontextmanager

from database import Base, engine
from routes import users

# ------- SETUP -------
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # On Startup.
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(lifespan = lifespan, docs_url = None)

app.include_router(
    users.router, 
    prefix = "/api/users",
    tags = ["users"]
)

# Dark Mode
setup_swagger_ui_theme(
    app, 
    docs_path = "/docs", 
    title = "Swagger Docs"
)

# ------- HOME -------
@app.get("/", include_in_schema = False)
async def home():
    return {"message": "Biscuit Backend is running"}