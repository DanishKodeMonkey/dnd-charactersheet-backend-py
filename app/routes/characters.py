from fastapi import APIRouter, HTTPException

router = APIRouter()


# Testing route
@router.get("")
async def get_characters():
    return {"Message": "This is all the characters (placeholder)"}
