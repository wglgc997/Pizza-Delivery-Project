# Importing FastAPI library.
from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv # Load the env variables on code
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") # Search the secret key in .env and load it.

# Set up the FastAPI class.
app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Import the routes from files
from routes.auth_routes import auth_router
from routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)


# execute on the terminal : uvicorn main:app --reload
# GET, POST, PUT, DELETE