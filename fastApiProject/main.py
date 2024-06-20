from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel

from pydantic import BaseModel

app = FastAPI()


# GET /
@app.get("/", description="This is our first route.")
async def base_get_route():
    return {"message": "Hello World"}


# GET /hello/Connectinno
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# GET /users
@app.get("/users", description="Endpoint to list users.")
async def list_users():
    return {"message": "list users route"}


# GET /products/1
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    return {"product_id": product_id}


# GET /users/1
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}


class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"


# GET /food/fruits
@app.get("/food/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name": food_name, "message": "you are healthy"}

    if food_name.value == "fruits":
        return {
            "food_name": food_name,
            "message": "you are still healthy, but like sweet things"
        }

    return {"food_name": food_name, "message": "i like chocolate milk"}


fake_items_db = [{"item_id": "1", "food_name": "Apple"},
                 {"item_id": "2", "food_name": "Banana"},
                 {"item_id": "3", "food_name": "Cherry"},
                 {"item_id": "4", "food_name": "Date"},
                 {"item_id": "5", "food_name": "Elderberry"},
                 {"item_id": "6", "food_name": "Fig"},
                 {"item_id": "7", "food_name": "Grape"},
                 {"item_id": "8", "food_name": "Honeydew"},
                 {"item_id": "9", "food_name": "Kiwi"},
                 {"item_id": "10", "food_name": "Lemon"}]


# GET /items?skip=0&limit=3
@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# GET /items/1?sample_query_param=hello&short=true
@app.get("/items/{item_id}")
async def get_item(item_id: str, sample_query_param: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "sample_query_param": sample_query_param}
    if q:
        item.update({"q": q})
    if not short:
        item.update({
            "description": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."
        })
    return item

"""
Parametrede bulunan değişkenlere default değer bir kez atanırsa 
hepsine atamak zorundayız
"""
# /users/1/items/45?short=false
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({
            "description": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."
        })
    return item


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price * item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result