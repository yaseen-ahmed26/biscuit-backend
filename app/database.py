# ------- IMPORTS -------
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ------- SETUP -------
SQLALCHEMY_DATABASE_URL = "sqlite:///./biscuit.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {
        "check_same_thread": False
    }
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

# ------- CLASSES -------
class Base(DeclarativeBase):
    pass

# ------- FUNCTIONS -------
def get_database():
    with SessionLocal() as database:
        yield database