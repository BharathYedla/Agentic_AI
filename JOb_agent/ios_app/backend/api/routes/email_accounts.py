from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def email_accounts_root():
    return {"message": "Email Accounts module"}
