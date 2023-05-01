from dataclasses import Field
from enum import Enum

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from fastapi import HTTPException

#run with uvicorn main:app --reload
app = FastAPI(
    title="FastAPI Tutorial",
    description="This is a very basic FastAPI tutorial",
    version="0.0.1",
    openapi_tags=[{
            "name": "items",
            "description": "Items related end-points"
            }]

)

class Category(Enum):
    '''
    This is a class for categories
    '''
    TOOLS = 'Tools'
    CONSUMABLES = 'comsumables'

class Item(BaseModel):
    '''
    This is a class for items
    '''
    # id: int = None
    # name: str = None
    # price: float = None
    # description: str = None
    # count: int = None
    # category: Category = None
    name: str = Field(description='Name of the item', max_length=12)
    price: float = Field(gt=0, description='Price of the item')
    description: str = Field(description='Description of the item', max_length=22)
    count:  int = Field(ge=0, description='Count of the item')
    id: int = Field(default=None, description='Id of the item')
    category: Category = Field(default=None, description='Category of the item')

items = {
    0: Item(id=0, name='Sword', price=20.0, description='A sturdy sword', count=5, category=Category.TOOLS),
    1: Item(id=1, name='Hammer', price=10.0, description='A sturdy hammer', count=10, category=Category.TOOLS),
    2: Item(id=2, name='Screwdriver', price=5.0, description='A screwdriver', count=20, category=Category.TOOLS),
    3: Item(id=3, name='Saw', price=15.0, description='A saw', count=15, category=Category.TOOLS),
    4: Item(id=4, name='Nails', price=10.0, description='A sturdy hammer', count=10, category=Category.CONSUMABLES),
}


@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {'data': items}

@app.get("/items/{item_id}")
def query_item_id(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item code({item_id=}) not found"
            )
    return {'data': items[item_id]}

selection = dict[
    str, str | float | int | Category | None
]
@app.get("/items/")
def query_item_parameters(
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
    id: int | None = None,
    category: Category | None = None
    ) -> dict[str, selection]:
    def check_item(item: Item) -> bool:
        return all((
            name is None or item.name == name,
            price is None or item.price == price,
            count is None or item.count != count,
            category is None or item.category is category,
        ))
    selection = [item for item in items.values() if check_item(item)]
    return {
        #'status': 'success',
        #'code': 200,
        #'query': f'id:{id}, name: {name}, price: {price}, count: {count}, category:{category}',
        'query message': f'Found {len(selection)} items','data': selection}


@app.post("/")
def add_items(item: Item) -> dict[str, Item]:
    if item.id in items:
        raise HTTPException(
            status_code=400, detail=f"Item code({item.id=}) already exists"
            )
    item.id = len(items)
    items[item.id] = item
    return {'data added -> ': item}


@app.put("/items/{item_id}",
         responses={
             404: {'description': 'Item not found'},
             400: {'description': 'nothing specified to update'},
         },)
def update_item(
    item_id: int = Path(title='Item ID', gt=0, le=len(items)),
    #item_id: int = Path(title='Item ID', gt=0, le=len(items), description='Item ID', alias='item-id'),
    #name: str | None = Query(default=None, min_length=3, max_length=12),
    #price: float | None = Query(default=None, gt=0.0),
    #description: str | None = Query(default=None, min_length=5, max_length=22),
    #count: int | None = Query(default=None, ge=0),
    #category: Category | None = None
    #item_id: int = Path(title='Item ID', gt=0, le=len(items), description='Item ID', alias='item-id'),
    #item_id: int = Path(title='Item ID', gt=0, le=len(items), description='Item ID', alias='item-id'),ge = 0), 
    name: str | None = Query(default=None, min_length=3, max_length=12),
    price: float | None = Query(default=None, gt=0.0),
    description: str | None = Query(default=None, min_length=5, max_length=22),
    count: int | None = Query(default=None, ge=0),
    category: Category | None = None
    ) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item code({item_id=}) not found"
            )
    if all(info is None for info in (name, price, description, count, category)):
        raise HTTPException(
            status_code=400, detail=f"No data to update"
            )
    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if description is not None:
        item.description = description
    if count is not None:
        item.count = count
    if category is not None:
        item.category = category
    return {'data updated -> ': item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:

    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item code({item_id=}) not found"
            )
    
    item = items.pop(item_id) 
    #del items[item_id]
    return {'data deleted -> ': item}