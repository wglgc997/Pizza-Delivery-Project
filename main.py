from fastapi import FastAPI ## Importing FastAPI library.
from networkx.algorithms.tree.mst import ALGORITHMS
from passlib.context import CryptContext # Used to crypt the passwords
from dotenv import load_dotenv # Load and read the env variables on the code
import os

load_dotenv() #Load the .env file

SECRET_KEY = os.getenv("SECRET_KEY") # Search the secret key in .env and load it.
ALGORITHM = os.getenv("ALGORITHM")

# Set up the FastAPI class.
app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Import the routes files /routes
from routes.auth_routes import auth_router
from routes.order_routes import order_router

# Connect the routes files with the main API.
app.include_router(auth_router)
app.include_router(order_router)



# execute on the terminal : uvicorn main:app --reload

# GET → buscar dados
# POST → criar
# PUT → atualizar
# DELETE → deletar