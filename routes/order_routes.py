from fastapi import APIRouter, Depends, HTTPException
from dependencies import take_session, check_token
from schemas import SchemaOrder
from sqlalchemy.orm import Session
from models import Order, User

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(check_token)]) #GLOBAL dependencie


@order_router.post("/orders")
async def create_order(order_schema: SchemaOrder, session: Session = Depends(take_session)):
    """Create a new order"""
    new_order = Order(user=order_schema.user_id, status="PENDING", price=0.0)
    session.add(new_order)
    session.commit()
    return {"message": f"Order created successfully! New ID {new_order.id}"}


@order_router.get("/")
async def orders(session: Session = Depends(take_session)):
    """"
    All the order routes. All orders must be autenticated and authorized."""
    orders = session.query(Order).all()
    return orders

@order_router.post("/cancel/{order_id}")
async def cancel_order(order_id: int, user: User = Depends(check_token), session=Depends(take_session)):
    """Cancel a specific order, only owner/admin"""
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="User not authorized")

    else:
        order.status = "CANCELED"
        session.commit()
        order_id = order_id # Force the object load
        return {"message": f"Order {order.id} canceled!", "order": order_id}




