from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def orders():
    """"
    All the order routes. All orders must be autenticated and authorized."""

    return {"Message": "You accessed the order page"} #fastapi transforma automaticamente em JSON