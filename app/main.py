from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI(title="Base CI Project")
class Item(BaseModel):
    name: str
    price: float
items: dict[str, Item] = {}
@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello, World!"}
@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/items/{item_id}", status_code=201)
def create_item(item_id: int, item: Item) -> Item:
    if item_id in items:
        raise HTTPException(status_code=409, detail="Item already exists")
    items[item_id] = item
    return item


@app.get("/items/{item_id}")
def read_item(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
