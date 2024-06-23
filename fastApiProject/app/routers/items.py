from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_token_header
from ..enums.Tags import Tags
from ..enums.Prefix import Prefix


router = APIRouter(
    prefix = Prefix.items,
    tags = [Tags.items],
    dependencies = [Depends(get_token_header)],
    responses = {
        status.HTTP_404_NOT_FOUND: {"description": "Not found"}
    },
)

fake_items_db = {
    "plumbus": {"name": "Plumbus"},
    "gun": {"name": "Portal Gun"},
}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Item not found!"
        )
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags = ["custom"],
    responses = {status.HTTP_403_FORBIDDEN: {"description": "Operation forbidden"}}
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The greate Plumbus"}



