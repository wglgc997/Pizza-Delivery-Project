# Importing FastAPI library.
from fastapi import FastAPI
# Set up the FastAPI class.
app = FastAPI()



# Import the routes from files
from routes.auth_routes import auth_router
from routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)


# execute on the terminal : uvicorn main:app --reload
# GET, POST, PUT, DELETE