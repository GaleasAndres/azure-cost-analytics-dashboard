from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


from api import router as api_router

app.include_router(api_router, prefix="/api")

