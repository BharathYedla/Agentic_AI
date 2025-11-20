from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def analytics_root():
    return {"message": "Analytics module"}
