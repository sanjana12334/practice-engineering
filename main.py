# from fastapi import FastAPI

# app = FastAPI(title="WorkTrack API")


# @app.get("/")
# def home():
#     return {"message": "WorkTrack API is running"}


# @app.get("/about")
# def about():
#     return {
#         "project": "WorkTrack",
#         "technology": "Python and FastAPI"
#     }
from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

k
