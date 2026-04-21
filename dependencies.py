from models import db
from sqlalchemy.orm import sessionmaker

def take_session():
    try:

        # Open session > use > commit/rollback > close the session
        Session = sessionmaker(bind=db)
        session = Session()
        yield session # Delivery the session to the route
    finally: # Route terminate, execute it
        session.close()
        
    # Handling errors/excepetions




