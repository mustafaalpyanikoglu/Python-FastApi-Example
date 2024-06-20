from fastapi import FastAPI, Query, Path, Body
from enum import Enum
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


fake_items_db = [{"item_id": "1", "food_name": "Apple"}, {"item_id": "2", "food_name": "Banana"},
                 {"item_id": "3", "food_name": "Cherry"}, {"item_id": "4", "food_name": "Date"},
                 {"item_id": "5", "food_name": "Elderberry"}, {"item_id": "6", "food_name": "Fig"},
                 {"item_id": "7", "food_name": "Grape"}, {"item_id": "8", "food_name": "Honeydew"},
                 {"item_id": "9", "food_name": "Kiwi"}, {"item_id": "10", "food_name": "Lemon"}]


# GET /
@app.get("/", description="This is our first route.")
async def base_get_route():
    return {"message": "Hello World"}


# GET /hello/Connectinno
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# # GET /users
# @app.get("/users", description="Endpoint to list users.")
# async def list_users():
#     return {"message": "list users route"}
#
#
# # GET /products/1
# @app.get("/products/{product_id}")
# async def get_product(product_id: int):
#     return {"product_id": product_id}
#
#
# # GET /users/1
# @app.get("/users/{user_id}")
# async def get_user(user_id: str):
#     return {"user_id": user_id}
#
#
# class FoodEnum(str, Enum):
#     fruits = "fruits"
#     vegetables = "vegetables"
#     dairy = "dairy"
#
#
# # GET /food/fruits
# @app.get("/food/{food_name}")
# async def get_food(food_name: FoodEnum):
#     if food_name == FoodEnum.vegetables:
#         return {"food_name": food_name, "message": "you are healthy"}
#
#     if food_name.value == "fruits":
#         return {"food_name": food_name, "message": "you are still healthy, but like sweet things"}
#
#     return {"food_name": food_name, "message": "i like chocolate milk"}


# # GET /items?skip=0&limit=3
# @app.get("/items")
# async def list_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]
#
#
# # GET /items/1?sample_query_param=hello&short=true
# @app.get("/items/{item_id}")
# async def get_item(item_id: str, sample_query_param: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id, "sample_query_param": sample_query_param}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update({
#             "description": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."})
#     return item
#
#
# """
# Parametrede bulunan değişkenlere default değer bir kez atanırsa
# hepsine atamak zorundayız
# """
#
#
# # /users/1/items/45?short=false
# @app.get("/users/{user_id}/items/{item_id}")
# async def get_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update({
#             "description": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."})
#     return item
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#
# @app.post("/items")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price * item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result
#
#
# @app.get("/readItems")
# async def read_items(q: str = Query("fixedquery", min_length=3, max_length=10)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# @app.get("/readItems2")
# async def read_items(q: list[str] = Query(["foo", "bar"], min_length=3, max_length=10)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# @app.get("/readItems3")
# async def read_items(
#         q: str | None = Query(
#             None,
#             min_length=3,
#             max_length=10,
#             title="Sample Query String",
#             description="This is a sample query string",
#             alias = "item-query"
#         )):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# @app.get("/items_hidden")
# async def hidden_query_route(
#         hidden_query: str | None = Query(
#             None,
#             include_in_schema = False)
# ):
#     if hidden_query:
#         return {"hidden_query": hidden_query}
#     return {"hidden_query": "Not Found"}
#
#
# @app.get("/items_validation/{item_id}")
# async def read_items_validation(
#     *,
#     item_id: int = Path(..., title = "The ID of the item to get", ge = 10, le = 100),
#     q: str = "hello",
#     size: float = Query(..., gt = 0, lt = 7.75)
# ):
#     results = {"item_id": item_id, "size": size}
#     if q:
#         results.update({"q": q})
#     return results

"""
Part 7 -> Body - Multiple Parameters
"""


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
        *,
        item_id: int = Path(..., title = "Th ID of the item to get", ge = 0, le = 150),
        q: str | None = None,
        item: Item = Body(..., embed = True)
        # user: User,
        # importance: int = Body(...)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    # if user:
    #     results.update({"user": user})
    # if importance:
    #     results.update({"importance": importance})
    return results