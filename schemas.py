from pydantic import BaseModel
from typing import Optional


class SchemaUser(BaseModel):
    name:str
    email: str
    password: str
    active: bool = True
    admin: bool = False

    # Convert SQLAlchemy objects > schemas
    class Config:
        from_attributes = True

class SchemaOrder(BaseModel):
    user_id: int

    class Config:
        from_attributes = True

class SchemaLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
