from fastapi import FastAPI

app = FastAPI()


@app.get("/", description="This is our first route.", deprecated=True)
async def base_get_route():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
