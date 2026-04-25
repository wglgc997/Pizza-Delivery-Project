from fastapi import APIRouter, Depends, HTTPException
from sympy import false
from models import User,db
from dependencies import take_session
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRED_MINUTES, SECRET_KEY
from schemas import SchemaUser, SchemaLogin
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRED_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration # Actual time + 30m
    dic_info = {"sub": user_id,"exp": expiration_date} # Infos are codify via JWT
    jwt_encode = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encode

def check_token(token, session: Session = Depends(take_session)):
    # verify if token is valid
    # extract the ID from user token
    user = session.query(User).filter(User.id == 1).first()
    return user

def user_auth(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return false
    elif not bcrypt_context.verify(password, user.password): # Compare hashes
        return false
    else:
        return user

@auth_router.get("/")
    async def home():
        """
        Authentication route for the system.
        """
        return {"message": "Authenticated"}

    @auth_router.post("/account_creation")
async def account_creation(schema_user:SchemaUser, session:Session = Depends(take_session)):
    """
    Create a new account for the system.
    """
    # Session = sessionmaker(bind=db) # Create the session/connection
    # session = Session() #Create the instance of class
    user = session.query(User).filter(User.email == schema_user.email).first() #Consult the User table

    if user:
        #User already exists
        raise HTTPException(status_code=400, detail="Account Already Exists") # If the email is already created, 400 error was flagged.
    else:
        #User created > consult the models file
        pass_cryp = bcrypt_context.hash(schema_user.password) # Cryp the password
        new_user = User(schema_user.name, schema_user.email, pass_cryp, schema_user.active, schema_user.admin)
        session.add(new_user)
        session.commit() # After changes make in the opened session, changes are saved in DB
        return {"message": f"Account {schema_user.email} has been created"}

#login > email and password > token JWT
@auth_router.post("/login")
async def login(schema_login: SchemaLogin, session: Session = Depends(take_session)): # DB instance
    user = user_auth(schema_login.email, schema_login.password, session)
    if not user:
        raise HTTPException(status_code=400, detail= "Incorrect email or password")
    else:
        # Create the token for the user
        access_token = create_token(user.id) # Return the created token # 30 minutes of duration
        refresh_token = create_token(user.id, token_duration=timedelta(days=7)) # Refresh in 7 days. After 7 days, new login is required
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"}


@auth_router.get("/refresh")
async def use_refresh_token(token):
    #Verify the token
    user = check_token(token)
    access_token = create_token(user.id)
    return {"access_token": access_token,
            "token_type": "bearer"}





