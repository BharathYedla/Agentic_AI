from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def sync_root():
    return {"message": "Sync module"}
