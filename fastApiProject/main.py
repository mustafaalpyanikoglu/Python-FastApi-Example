from enum import Enum
import time
from typing import Optional, List, Union, Literal
from urllib.request import Request
from uuid import UUID
from datetime import datetime, timedelta

from fastapi import (
  FastAPI, Query, HTTPException,
  File, UploadFile, Form,
  Path, Body, Cookie,
  Header, status, Depends,
  BackgroundTasks,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from starlette.responses import JSONResponse, PlainTextResponse
from passlib.context import CryptContext
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Part 33 -  Static Files - Testing - Debugging

fake_secret_token = "conneofsilence"
fake_db = dict(
  foo = dict(
    id = "foo", title = "Foo", description = "There goes my hero",
  ),
  bar = dict(
    id = "bar", title = "Bar", description = "The bartenders"
  )
)

class Item(BaseModel):
  id: str
  title: str
  description: str | None = None

@app.get("/items/{item_id}", response_model = Item)
async def read_main(item_id: str, x_token: str = Header(...)):
  if x_token != fake_secret_token:
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Invalid X-Token header")
  if item_id not in fake_db:
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Item not found")
  return fake_db[item_id]


# Part 33 - End

# Part 32 - Metadata and Docs URLs

# description = ChimichanApp API helpers you do awesome stuff.
#
# ## Items
#
# You can **read items**.
#
# ##Users
#
# You will be able to:
#
# * **Create users**(_not implemented_).
# * **Read users**(_not implemented_).


# tags_metadata = [
#   dict(
#     name = "users",
#     description = "Operations with users. The **login** logic is also here."
#   ),
#   dict(
#     name = "items",
#     description = "Manage items. so _fancy_ the have their  own docs.",
#     externalDocs = dict(
#       description = "Items external docs",
#       url = "https://www.hvp.design"
#     )
#   ),
#
# ]
#
#
# app = FastAPI(
#   title = "ChimichanApp",
#   description=description,
#   version = "0.0.1",
#   terms_of_service = "http://example.com/terms/",
#   contact = dict(
#     name = "Deadpoolio the Amazing",
#     url="http://x-force.example.com/contact",
#     email="dp@xforce.example.com",
#   ),
#   license_info = dict(
#     name = "Apache 2.0",
#     url = "https://www.apache.org/licenses/LICENSE-2.0.txt"
#   ),
#   openapi_tags = tags_metadata,
#   openapi_url = "/api/v1/openapi.json",
#   docs_url = "/hello-world",
#   #redoc_url = None
#
# )
#
#
# @app.get("/users/", tags = ["users"])
# async def get_users():
#   return [dict(name="Harry"), dict(name="Ron")]
#

@app.get("/items/", tags = ["items"])
async def read_items():
  return [dict(name="wand"), dict(name="flying broom")]

# Part 32

# Part 31 - Background Tasks


# def write_notification(email:str, message= ""):
#   with open('log.txt', mode='w') as email_file:
#     content = f"notification for {email} : {message}"
#     time.sleep(5)
#     email_file.write(content)
#
#
# @app.post("/send-notification/{email}", status_code = status.HTTP_202_ACCEPTED)
# async def send_notification(email: str, background_tasks: BackgroundTasks):
#   background_tasks.add_task(write_notification, email, message = "some notification")
#   return {"message": "Notification sent in the background"}


# def write_log(message: str):
#   with open('log.txt', mode='a') as log:
#     log.write(message + '\n')
#
# def get_query(
#         background_task: BackgroundTasks,
#         q: str | None = None
# ):
#   if q:
#     message = f"found query: {q}\n"
#     background_task.add_task(write_log, message)
#   return q
#
# @app.post("/send-notification/{email}")
# async def send_notification(
#         email: EmailStr,
#         background_task: BackgroundTasks,
#         q: str = Depends(get_query)
# ):
#   message = f"message to {email}\n"
#   background_task.add_task(write_log, message)
#   return {"message": "Message send", "query": q}
#

# Part 31 - End


# Part 28 - Middleware and CORS

# class MyMiddleware:
#   async def dispatch(self, request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers['X-Process-Time'] = str(process_time)
#     return response
#
#
# origins = ["http://localhost:3000", "http://localhost:8000"]
# @app.add_middleware(MyMiddleware)
# @app.add_middleware(
#   CORSMiddleware,
#   allow_origins=origins
# )
#
# @app.get("/blah")
# async def blah():
#   return {"Hello": "world"}


# Part 28 - End

#Part 27 - Security

# SECRET_KEY = "thequickbrownfoxjumpsoverthelazydog"
# ALGORITHM = 'HS256'
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# fake_users_db = {
#     "alp": {
#         "username": "alp",
#         "full_name": "Mustafa Alp",
#         "email": "malpyanikgolu@gmail.com",
#         "hashed_password": "$2b$12$8kgY0HAUn.xaZZi3zegpY.6Bp1VAezr4Az4i1NPlPqqF7S5k7RqFu",
#         "disabled": False,
#     },
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$8kgY0HAUn.xaZZi3zegpY.6Bp1VAezr4Az4i1NPlPqqF7S5k7RqFu",
#         "disabled": True,
#     },
# }
#
# class Token(BaseModel):
#   access_token: str
#   token_type: str
#
# class TokenData(BaseModel):
#   username: Optional[str] = None
#
# class User(BaseModel):
#   username: str
#   email: Optional[EmailStr] = None
#   full_name: Optional[str] = None
#   disabled: bool = False
#
# class UserInDB(User):
#   hashed_password: str
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
#
# def verify_password(plain_password, hashed_password):
#   return pwd_context.verify(plain_password, hashed_password)
#
# def get_password_hash(password):
#   return pwd_context.hash(password)
#
# def get_user(db, username: str):
#   if username in db:
#     user_dict = db[username]
#     return UserInDB(**user_dict)
#
# def authecticate_user(fake_db, username: str, password: str):
#   user=  get_user(fake_db, username)
#   if not user:
#     return False
#   if not verify_password(password, user.hashed_password):
#     return False
#   return user
#
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#   to_encode = data.copy()
#   if expires_delta:
#     expire = datetime.utcnow() + expires_delta
#   else:
#     expire = datetime.utcnow() + timedelta(minutes=15)
#   to_encode.update({'exp': expire})
#   encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#   return encoded_jwt
#
# @app.post("/token", response_model = Token)
# async def login_for_access_Token(
#         form_data: OAuth2PasswordRequestForm = Depends()
# ):
#   user = authecticate_user(fake_users_db, form_data.username, form_data.password)
#   if not user:
#     raise HTTPException(
#       status_code=status.HTTP_401_UNAUTHORIZED,
#       detail="Incorrect username or password",
#       headers={"WWW-Authenticate": "Bearer"},
#     )
#   access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#   access_token = create_access_token(
#     data = {"sub": user.username},
#     expires_delta= access_token_expires
#   )
#   return {"access_token": access_token, "token_type": "bearer", "expires_in": access_token_expires}
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#   credentials_exception = HTTPException(
#     status_code = status.HTTP_401_UNAUTHORIZED,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
#   )
#
#   try:
#     payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
#     username: str = payload.get("sub")
#     if username is None:
#       raise credentials_exception
#     token_data = TokenData(username=username)
#   except JWTError:
#     raise credentials_exception
#   user = get_user(fake_users_db, username=token_data.username)
#   if user is None:
#     raise credentials_exception
#   return user
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#   if current_user.disabled:
#     raise HTTPException(
#       status_code=status.HTTP_400_BAD_REQUEST,
#       detail="Inactive user"
#     )
#   return current_user
#
# @app.get("/users/me", response_model = User)
# async def get_me(current_user: User = Depends(get_current_active_user)):
#   return current_user
#
# @app.get("/users/me/items")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#   return [{"item_id": "Foo", "owner": current_user.username}]

#Part 27 - End


#Part 26 - Security

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
#
# fake_users_db = {
#   "mustafaalp": dict(
#     username="alp",
#     full_name="Mustafa Alp",
#     email="malpyanikgolu@gmail.com",
#     hashed_password="fakehashedsecret",
#     disabled=False
#   ),
# "johndoe": dict(
#     username="johndoe",
#     full_name="John Doe",
#     email="johndoe@example.com",
#     hashed_password="fakehashedsecret2",
#     disabled=True
#   ),
# }
#
# def fake_hash_password(password: str) -> str:
#   return f"fakehashed{password}"
#
# class User(BaseModel):
#   username: str
#   email: EmailStr | None = None
#   full_name: str | None = None
#   password: str | None = None
#
#
# class UserInDb(User):
#   hashed_password: str
#
# def get_user(db, username: str):
#   if username in db:
#     user_dict = db[username]
#     return User(**user_dict)
#
#
# def fake_decode_token(token):
#   return get_user(fake_users_db, token)
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#   user = fake_decode_token(token)
#   if not user:
#     raise HTTPException(
#       status_code = status.HTTP_401_UNAUTHORIZED,
#       detail = "Invalid authentication credentials",
#       headers = {"WWW-Authenticate": "Bearer"},
#     )
#   return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#   if current_user.disabled:
#     raise HTTPException(
#       status_code = status.HTTP_400_BAD_REQUEST,
#       detail = "Inactive user",
#     )
#
#
# @app.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#   user_dict = fake_users_db.get(form_data.username)
#   if not user_dict:
#     raise HTTPException(
#       status_code = status.HTTP_401_UNAUTHORIZED,
#       detail = "Incorrect username or password",
#     )
#   user = UserInDb(**user_dict)
#   hashed_password = fake_hash_password(form_data.password)
#   if not hashed_password == user.hashed_password:
#     raise HTTPException(
#       status_code = status.HTTP_401_UNAUTHORIZED,
#       detail = "Incorrect username or password",
#     )
#
#   return {"access_token": user.username, "token_type": "bearer"}
#
# @app.get("/users/me")
# async def get_me(current_user: User = Depends(get_current_active_user)):
#   return current_user
#
#
# @app.get("/items")
# async def read_items(token: str = Depends(oauth2_scheme)):
#   return {"token": token}


#Part 26 - End



#Part 22 - Dependencies

# async def hello():
#   return "world"
#
# async def common_parameters(
#         q: str | None = None,
#         skip: int = 0,
#         limit: int = 100,
#         blah: str = Depends(hello)
# ):
#   return {"q": q, "skip": skip, "limit": limit, "hello": blah}


# @app.get("/items", tags = ["items"])
# async def read_items(commons: dict = Depends(common_parameters)):
#   return commons
#
#
# @app.get("/users", tags = ["items"])
# async def read_users(commons: dict = Depends(common_parameters)):
#   return commons


# fake_items_db = [
#   {"item_name": "Foo"},
#   {"item_name": "Bar"},
#   {"item_name": "Baz"},
# ]
#
# class CommonQueryParams:
#   def __init__(self, q:str | None = None, skip: int = 0, limit: int = 100):
#     self.q = q
#     self.skip = skip
#     self.limit = limit
#
# @app.get("/items")
# async def read_items(commons: CommonQueryParams = Depends()):
#   response = {}
#   if commons.q:
#     response.update({"q": commons.q})
#   items = fake_items_db[commons.skip: commons.skip + commons.limit]
#   response.update({"items": items})
#   return response

# def query_extractor(q: str | None = None):
#   return q
#
# def query_or_body_extractor(
#         q: str = Depends(query_extractor),
#         last_query: str | None = Body(None)
# ):
#   if q:
#     return q
#   return last_query
#
# @app.post("/item")
# async def try_query(query_or_body: str = Depends(query_or_body_extractor)):
#   return {"q_or_body": query_or_body}

# async def verify_token(x_token: str = Header(...)):
#   if x_token != "fake-super-secret-token":
#     raise HTTPException(
#       status_code = status.HTTP_400_BAD_REQUEST,
#       detail = "X-Token header invalid."
#     )
#
# async def verify_key(x_key: str = Header(...)):
#   if x_key != "fake-super-secret-token":
#     raise HTTPException(
#       status_code = status.HTTP_400_BAD_REQUEST,
#       detail = "X-Key header invalid."
#     )
#   return x_key
#
# app = FastAPI(dependencies = [Depends(verify_token), Depends(verify_key)])
#
#
# @app.get("/items", dependencies = [Depends(verify_token), Depends(verify_key)])
# async def read_items():
#   return [{"item": "foo"}, {"item": "bar"}]
#
#
# @app.get("/users", dependencies = [Depends(verify_token), Depends(verify_key)])
# async def read_users():
#   return [{"username": "Mustafa"}, {"username": "Alp"}]

#Part 22 - End


#Part 21 - JSON Compatible Encoder
#
# class Item(BaseModel):
#   name: str | None = None
#   description: str | None = None
#   price: float | None = None
#   tax: float = 10.5
#   tags: list[str] = []
#
# items = {
#   "foo": {"name": "Foo", "price": 50.2},
#   "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#   "baz": {
#     "name": "Baz",
#     "description": "50.2",
#     "price": 50.2,
#     "tax": 33,
#     "tags": []
#   }
# }
#
# @app.get("/items/{item_id}", response_model = Item)
# async def read_item(item_id: str):
#   return items.get(item_id)
#
# @app.put("/items/{item_id}", response_model = Item)
# def update_item(item_id: str, item: Item):
#   update_item_encoded = jsonable_encoder(item)
#   items[item_id] = update_item_encoded
#   return update_item_encoded
#
# @app.patch("/items/{item_id}", response_model = Item)
# async def read_item(item_id: str, item: Item):
#   stored_item_data = items.get(item_id)
#   if stored_item_data is not None:
#     stored_item_model = Item(**stored_item_data)
#   else:
#     stored_item_model = Item()
#   update_data = item.dict(exclude_unset = True)
#   updated_item = stored_item_model.copy(update=update_data)
#   items[item_id] = jsonable_encoder(updated_item)
#   print(items[item_id])
#   return updated_item


#Part 21 - End

#Part 20 - Path Operation Configuration
#
# class Item(BaseModel):
#   name: str
#   description: str | None = None
#   price: float
#   tax: float | None = None
#   tags: set[str] | None = None
#
# class Tags(Enum):
#   items = "items"
#   users = "users"
#
# @app.post(
#   "/items/",
#   response_model = Item,
#   status_code = status.HTTP_201_CREATED,
#   tags = [Tags.items],
#   # summary = "Create an Item",
#   # description = "Create an item with all the information: name; description; tax; and a set of unique tags"
#   response_description = "The created item",
# )
# async def create_item(item: Item):
#   """
#   Create an item with all the information
#   - **name**: each item must have a name
#   - **description**: a long description
#   - **tax**: if the item doesn't have tax, you can omit this
#   - **tags** a set of unique tag strings for this item
#   """
#   return item
#
#
# @app.get("/items/", tags = [Tags.items, Tags.users])
# async def read_items():
#   return [{"name": "Foo", "price": 43}]
#
#
# @app.get("/users/", tags = [Tags.users])
# async def read_users():
#   return [{"username": "Alp"}]
#
#
# @app.get("/elements/", tags = [Tags.items], deprecated = True)
# async def read_element():
#   return [{"item_id": "Foo"}]

#Part 20 - End

"""
Start
"""


# fake_items_db = [{"item_id": "1", "food_name": "Apple"}, {"item_id": "2", "food_name": "Banana"},
#                  {"item_id": "3", "food_name": "Cherry"}, {"item_id": "4", "food_name": "Date"},
#                  {"item_id": "5", "food_name": "Elderberry"}, {"item_id": "6", "food_name": "Fig"},
#                  {"item_id": "7", "food_name": "Grape"}, {"item_id": "8", "food_name": "Honeydew"},
#                  {"item_id": "9", "food_name": "Kiwi"}, {"item_id": "10", "food_name": "Lemon"}]
#


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

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#
# class User(BaseModel):
#     username: str
#     full_name: str | None = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(
#         *,
#         item_id: int = Path(..., title = "Th ID of the item to get", ge = 0, le = 150),
#         q: str | None = None,
#         item: Item = Body(..., embed = True)
#         # user: User,
#         # importance: int = Body(...)
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     # if user:
#     #     results.update({"user": user})
#     # if importance:
#     #     results.update({"importance": importance})
#     return results


"""
Part 8 -> Body - Fields
"""

#
# class Item(BaseModel):
#     name: str
#     description: str | None = Field(
#         title = "The description of the item",
#         max_length = 300
#     )
#     price: float = Field(..., gt = 0, description = "The price must be a greater than zero.")
#     tax: float | None = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(
#         item_id: str,
#         item: Item = Body(..., embed = True),
# ):
#     results = {"item_id": item_id, "item": item}
#     return results


"""
Part 9 -> Body - Nested Models
"""

# class Image(BaseModel):
#     url: HttpUrl
#     name: str
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()
#     image: list[Image] | None = None
#
#
# class Offer(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     item: list[Item]
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results
#
# @app.post("/offers")
# async def create_offer(offer: Offer = Body(..., embed = True)):
#     return offer
#
# @app.post("/images/multiple")
# async def create_multiple_images(images: list[Image]):
#     return images
#
# @app.post("blah")
# async def create_some_blahs(blahs: dict[int, float]):
#     return blahs


"""
Part 10 -> Declare Request Example Data
"""

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#     # class Config:
#     #     schema_extra = {
#     #         "example": {
#     #             "name": "Foo",
#     #             "description": "A very nice Item",
#     #             "price": 5.24,
#     #             "tax": 0.99,
#     #         }
#     #     }
#
#
# @app.put("/items/{item_id}")
# async def update_item(
#         item_id: int,
#         item: Item = Body(
#             ...,
#             examples = {
#                 "normal": {
#                     "summary": "A normal example",
#                     "description": "A __normal__item works _correctly_",
#                     "value": {
#                         "description": "A very nice Item",
#                         "name": "Foo",
#                         "price": 16.25,
#                         "tax": 1.67,
#                     },
#                 },
#                 "converted": {
#                     "summary": "An example with converted data",
#                     "description": "FastAPI can convert price 'strings' to actual 'numbers' automatically",
#                     "value": {"name": "Bar", "price": "16.25"}
#                 },
#                 "invalid": {
#                     "summary": "Invalid data is rejected with an error",
#                     "description": "Hello world",
#                     "value": {"name": "Bar", "price": "16.25"}
#                 },
#             })
# ):
#     results = {"item_id": item_id, "item": item}
#     return results


"""
Part 11 -> Extra Data Types
"""

# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_date: datetime | None = Body(None),
#     end_date: datetime | None = Body(None),
#     repeat_at: time | None = Body(None),
#     process_after: timedelta | None = Body(None),
# ):
#     start_process = start_date + process_after
#     duration = end_date - start_process
#     return {
#         "item_id": item_id,
#         "start_date": start_date,
#         "end_date": end_date,
#         "repeat_at": repeat_at,
#         "process_after": process_after,
#         "duration": duration
#     }


"""
Part 12 -> Cookie and Header Parameters
"""

# @app.get("/items")
# async def read_items(
#         cookie_id: str | None = Cookie(None),
#         accept_encoding: str | None = Header(None),
#         sec_ch_ua: str | None = Header(None),
#         user_agent: str | None = Header(None),
#         x_token: list[str] | None = Header(None),
# ):
#     return {
#       "cookie_id": cookie_id,
#       "accept_encoding": accept_encoding,
#       "sec_ch_ua": sec_ch_ua,
#       "user_agent": user_agent,
#       "X-Token Values": x_token,
#     }


"""
Part 13 -> Response Model
"""

# class Item(BaseModel):
#   name: str
#   description: Optional[str] = None
#   price: float
#   tax: Optional[float] = 10.5
#   tags: list[str] = []
#
# items = {
#   "foo": {"name": "Foo", "price": 50.2},
#   "bar": {
#     "name": "Bar",
#     "description": "The bartenders",
#     "price": 62,
#     "tax": 20.2},
#   "baz": {
#     "name": "Baz",
#     "description": None,
#     "price": 50.2,
#     "tax": 10.5,
#     "tags": []}
# }
#
# @app.get(
#   "/items/{item_id}",
#   response_model = Item,
#   response_model_exclude_unset = True
# )
# async def read_item(item_id: Literal["foo", "bar", "baz"]):
#   return items[item_id]
#
# @app.post(
#   "/items",
#   response_model = Item,
# )
# async def create_item(item: Item):
#   return item
#
# @app.get(
#   "/items/{item_id}/name",
#   response_model = Item,
#   response_model_include = {"name", "description"},
#   response_model_exclude = {"tax"},
# )
# async def read_item_name(item_id: Literal['foo', 'bar', 'baz']):
#   return items[item_id]
#
# @app.get(
#   "/items/{item_id}/public",
#   response_model = Item,
#   response_model_exclude = {"tax"},
# )
# async def read_items_public_data(item_id: Literal['foo', 'bar', 'baz']):
#   return items[item_id]
#
#
# class UserBase(BaseModel):
#   username: str
#   email: EmailStr
#   full_name: Optional[str] = None
#
# class UserIn(UserBase):
#   password: str
#
# class UserOut(UserBase):
#   pass
#
# @app.post("/users", response_model = UserOut)
# async def create_user(user: UserIn):
#   return user


# class UserBase(BaseModel):
#   username: str
#   email: EmailStr
#   full_name: Optional[str] = None
#
# class UserIn(UserBase):
#   password: str
#
# class UserOut(UserBase):
#   pass
#
# class UserInDB(UserBase):
#   hashed_password: str
#
#
# def fake_password_hash(raw_password: str):
#   return f"supersecret{raw_password}"
#
# def fake_save_user(user_in: UserIn):
#   hashed_password = fake_password_hash(user_in.password)
#   user_in_db = UserInDB(**user_in.dict(), hashed_password = hashed_password)
#   print("userin.dict", user_in.dict)
#   print("User 'saved'.")
#   return user_in_db
#
# @app.post("/user/", response_model = UserOut)
# async def create_user(user_in: UserIn):
#   user_saved = fake_save_user(user_in)
#   return user_saved
#
#
# class BaseItem(BaseModel):
#     description: str
#     type: str
#
# class CarItem(BaseItem):
#   type: Literal["car"] = "car"
#
# class PlaneItem(BaseItem):
#   type: Literal["plane"] = "plane"
#   size: int
# items = {
#   "item1": {"description": "All my friend drive a low rider", "type": "car"},
#   "item2": {"description": "Music is my areoplane", "type": "plane", "size": 5},
# }
#
# @app.get(
#   "/items/{item_id}",
#   response_model = Union[PlaneItem, CarItem]
# )
# async def read_item(item_id: Literal["item1", "item2"]):
#   return items[item_id]
#
# class ListItem(BaseModel):
#   name: str
#   description: str
#
# list_items = [
#   {"name": "Foo", "description": "Foo", "type": "car"},
#   {"name": "Bar", "description": "Bar", "type": "plane"},
# ]
#
# @app.get("/list_items/", response_model = list[ListItem])
# async def read_items():
#   return list_items
#
# @app.get("/arbitrary/", response_model = dict[str, float])
# async def get_arbitrary():
#   return {"foo": 1, "bar": "2"}

# @app.post("/items/", status_code = status.HTTP_201_CREATED)
# async def create_item(name: str):
#   return {"name": name}



#Part 16 -> Form Fields


# class User(BaseModel):
#   username: str
#   password: str
#
#
# @app.post("/login/")
# async def login(
#         username: str = Form(...),
#         password: str = Form(...),
# ):
#   print("password", password)
#   return {"username": username}
#
#
# class User(BaseModel):
#   username: str
#   password: str
#
#
# @app.post("/login-json/")
# async def login_json(
#         username: str = Body(...),
#         password: str = Body(...)
# ):
#   return {"username": username}

# Part 17 -> Request Files


# @app.post("/files/")
# async def create_file(
#         files: list[bytes] | None = File(
#           None,
#           description = "A file read as bytes"
#         )
# ):
#   if not files:
#     return {"message": "No file send"}
#   return {"file": [len(files)]}
#
#
# @app.post("/upload-file/")
# async def upload_file(
#         files: list[UploadFile] = File(
#           ...,
#           description = "A file read as bytes"
#         )
# ):
#   if not files:
#     return {"message": "No upload file sent"}
#   print("file:", files)
#   contents = await files[0].read()
#   return {"filename": [file.filename for file in files]}


# @app.post("/files/")
# async def create_file(
#         file: bytes = File(...),
#         fileb: UploadFile = File(...),
#         token: str = Form(...)
# ):
#   return {
#     "file_size": len(file),
#     "token": token,
#     "fileb_content_type": fileb.content_type
#   }


# Part 19 - Handling Errors
# items = {"foo": "The Foo Wrestlers"}
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: Literal['foo', 'bar', 'baz']):
#   if item_id not in items:
#     raise HTTPException(
#       status_code = status.HTTP_404_NOT_FOUND,
#       detail = "Item not found",
#       headers = {"X-Error": "There goes my error"})
#   return {"item": items[item_id]}
#
#
# class UnicornException(Exception):
#   def __init__(self, name: str):
#     self.name = name
#
#
# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#   return JSONResponse(
#     status_code = status.HTTP_418_IM_A_TEAPOT,
#     content = {"message": f"Opps! {exc.name} did something. There goes a rainbow..."},
#   )
#
#
# @app.get("/unicorns/{name}")
# async def read_unicorns(name: str):
#   if name == "yolo":
#     raise UnicornException(name = name)
#   return {"unicorn_name": name}


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#   print("request", request)
#   print("exc", exc)
#   return PlainTextResponse(
#     str(exc),
#     status_code = status.HTTP_400_BAD_REQUEST
#   )
#
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc: StarletteHTTPException):
#   return PlainTextResponse(
#     str(exc.detail),
#     status_code = exc.status_code
#   )
#
# @app.get("/validation_items/{items_id}")
# async def read_validation_items(item_id: int):
#   if item_id == 3:
#     raise HTTPException(status_code = status.HTTP_418_IM_A_TEAPOT, detail = "Nope! I don't like 3.")
#   return {"item_id": item_id}

######
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#   print("request", request)
#   print("exc", exc)
#   return JSONResponse(
#     status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
#     content = jsonable_encoder({
#       "detail": exc.errors(),
#       "body": exc.body,
#     }),
#   )
#
# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
#   # loglama yapılabilir
#   print(f"OMG! An Http Error: {repr(exc)}")
#   return await http_exception_handler(request, exc=exc)
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#   # loglama yapılabilir
#   print(f"OMG! The client sent invalid data!: {repr(exc)}")
#   return await request_validation_exception_handler(request, exc=exc)
#
# class Item(BaseModel):
#   title: str
#   size: int
#
# @app.post("/items/")
# async def create_item(item: Item):
#
#   return item
#
# @app.get("/blah_items/{item_id}")
# async def read_item(item_id: int):
#   if item_id == 3:
#     raise HTTPException(status_code = status.HTTP_418_IM_A_TEAPOT, detail = "Nope! I don't like 3.")
#   return {"item_id": item_id}