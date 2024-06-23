from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header
from ..enums.Tags import Tags


router = APIRouter()

@router.get('/users', tags = [Tags.users])
async def get_users():
  return [{"username": "Mustafa"}, {"username": "Alp"}]


@router.get("/users/me", tags = [Tags.users])
async def get_user_me():
  return {"username": "Mustafa"}


@router.get("/users/{username}", tags = [Tags.users])
async def read_user(username: str):
  return {"username": username}
