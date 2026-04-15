from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/)")
async def authentication():
    """
    Authentication route for the system.
    """
    return {"message": "Authenticated"}