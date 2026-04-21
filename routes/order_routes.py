from fastapi import APIRouter, Depends
from dependencies import take_session
from schemas import SchemaOrder
from sqlalchemy.orm import Session
from models import Order

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def orders():
    """"
    All the order routes. All orders must be autenticated and authorized."""

    return {"Message": "You accessed the order page"} #fastapi transforma automaticamente em JSON

@order_router.post("/orders")
async def create_order(order_schema: SchemaOrder, session: Session = Depends(take_session)):
    new_order = Order(user=order_schema.user_id)
    session.add(new_order)
    session.commit()
    return {"message": f"Order created successfully! New ID {new_order.id}"}


