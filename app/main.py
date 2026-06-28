# ------- IMPORTS -------
from fastapi import FastAPI
from fastapi_swagger_ui_theme import setup_swagger_ui_theme

from database import Base, engine
from routes import users

# ------- SETUP -------
app = FastAPI(docs_url = None)

Base.metadata.create_all(bind = engine)

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
def home():
    return {"message": "Biscuit Backend is running"}