from fastapi import APIRouter, Depends
from app.utils.auth import verify_access_token

router = APIRouter(dependencies=[Depends(verify_access_token)])


# Testing route
@router.get("")
async def get_characters():
    return {"Message": "This is all the characters (placeholder)"}
