from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title = "event-analytics")

# class Item(BaseModel):
#     text: str = None 
#     is_done: bool = False 
# items = [] 


@app.get("/health")
def root(): 
    return {"status": "ok"}


# @app.post("/items") #http post request
# def create_item(item: Item): #query paramater
#     items.append(item)
#     return items

# @app.get("/items") #http get request
# def list_items(limit: int = 10): #query parameter with default value
#     return items[0:limit]

# @app.get("/items/{item_id}") #http get request
# def get_item(item_id: int) -> Item: 
#     if item_id < len(items):
#         return items[item_id]
#     else:
#         raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")