from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from models import User,db
from main import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import sessionmaker


def take_session():
    """Open and close a DB session"""
    try:
        # Open session > use > commit/rollback > close the session
        Session = sessionmaker(bind=db)
        session = Session()
        yield session # Delivery the session to the route
    finally: # Route terminate, execute it
        session.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login_form")

def check_token(token: str = Depends(oauth2_scheme), session: Session = Depends(take_session)):
    """ Dependency that allow just auth user could access"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # Decode the token
        user_id = payload.get("sub") # Extract the user ID/sub of the user in the token
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        # Validate if the user exist in the DB, if not, raise an error
        user = session.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError: # Error on JWT
        raise HTTPException(status_code=401, detail="Invalid Token")






