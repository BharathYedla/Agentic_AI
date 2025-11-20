from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def applications_root():
    return {"message": "Applications module"}
