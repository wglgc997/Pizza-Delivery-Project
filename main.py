from fastapi import FastAPI ## Importing FastAPI library.
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext # Used to crypt the passwords
from dotenv import load_dotenv # Load and read the env variables on the code
import os

load_dotenv() #Load the variables from .env file
# Variables from .env file
SECRET_KEY = os.getenv("SECRET_KEY") # Search the secret key in .env and load it.
ALGORITHM = os.getenv("ALGORITHM") # Search the info  in .env and load it.
ACCESS_TOKEN_EXPIRED_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRED_MINUTES")) # Search the info in .env and load it.

# Set up the FastAPI class.
app = FastAPI()
# Security
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login_form")

# Import the routes files /routes
from routes.auth_routes import auth_router
from routes.order_routes import order_router
# Connect the routes files with the main API.
app.include_router(auth_router)
app.include_router(order_router)
