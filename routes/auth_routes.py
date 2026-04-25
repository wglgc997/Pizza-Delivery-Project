from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import User, db
from dependencies import take_session,check_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRED_MINUTES, SECRET_KEY
from schemas import SchemaUser, SchemaLogin
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

# Functions
def create_token(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRED_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration # Actual time + 30m
    dic_info = {"sub": user_id,"exp": expiration_date} # Infos are codify via JWT
    jwt_encode = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encode

def user_auth(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return false
    elif not bcrypt_context.verify(password, user.password): # Compare hashes
        return false
    else:
        return user

# Routes
@auth_router.get("/")
async def home():
        """
        Main authentication route for the system.
        """
        return {"message": "Authenticated"}

@auth_router.post("/account_creation")
async def account_creation(schema_user:SchemaUser, session:Session = Depends(take_session)):
    """
    Create a new account for the system with crip password.
    """
    user = session.query(User).filter(User.email == schema_user.email).first() ## Consult the user on DB
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
async def login(schema_login: SchemaLogin, session: Session = Depends(take_session)):
    """Log the user and return tokens"""
    """Login via JSON"""
    """Return access token and refresh token"""

    user = user_auth(schema_login.email, schema_login.password, session) # Consult the user on DB
    if not user:
        raise HTTPException(status_code=400, detail= "Incorrect email or password") # If user dont exist, raise 400 error
    else:# Create the token for a know user
        access_token = create_token(user.id) # Create an access token (30 minutes of duration)
        refresh_token = create_token(user.id, token_duration=timedelta(days=7)) # Refresh in 7 days. After 7 days, new login is required
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"}

@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(check_token)):
    """Generate a new Access token from the Refresh the token"""

    #Verify the existent token
    new_access_token = create_token(str(user.id))
    return {"access_token": new_access_token, "token_type": "bearer"}

@auth_router.post("/login_form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(take_session)):
    """Login form via OAuth2 for the doc"""
    """Login via OAuth2"""
    """Return access token"""

    user = session.query(User).filter(User.email == form_data.username).first() # Consult the user on DB
    if not user or not bcrypt_context.verify(form_data.password, user.password): # If user not exists on DB, 401 error is raised
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = create_token(str(user.id))
    return{"access_token": access_token_expires, "token_type": "bearer"}



