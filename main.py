from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field

costs = [
    {
        'id': 1,
        'amount': 120.5,
        'description':'buying a book',
    },
    {
        'id': 2,
        'amount': 50.6,
        'description':'buying an ice cream',
    },
    {
        'id': 3,
        'amount': 12.5,
        'description':'paying for a taxi',
    }
]


app = FastAPI(debug=True)

class CostCreate(BaseModel):   # for validation 
    amount: float = Field(
        gt = 0,  # greater than
        le = 1_000_000  # less than or equal 
        )
    description: str = Field(
        min_length=3,
        max_length=100,
        pattern= r"^[a-zA-Z0-9 ]+$"
    )

class costResponse(BaseModel):
    id: int
    amount: float
    description: str

@app.post('/costs',status_code= status.HTTP_201_CREATED)
def add_cost(cost: CostCreate):
    max_id = 0
    for item in costs:
        if item["id"] > max_id:
            max_id = item["id"]
    
    new_cost = {
        'id': max_id + 1,
        'amount': cost.amount,
        'description': cost.description
    }
    costs.append(new_cost)
    
    return new_cost


@app.get('/costs', response_model=list[costResponse], status_code= status.HTTP_200_OK)
def receive_costs():
    return costs


@app.get('/costs/{id}', response_model=costResponse, status_code= status.HTTP_200_OK)
def receive_costs_with_id(id:int):
    
    for cost in costs:
        if cost["id"] == id:
            return cost
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='object not found')


@app.put('/costs/{id}', response_model=costResponse ,status_code= status.HTTP_200_OK)
def edit_costs(id: int, cost: CostCreate):

    for item in costs:
        if item["id"] == id:
            costs[id] = {
                "id": id,
                item["amount"]: cost.amount,
                item["description"]: cost.description
            }
            return costs[id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='object not found')
    

@app.delete('/costs/{id}',status_code=status.HTTP_204_NO_CONTENT)
def remove_cost(id: int):
    for cost in costs:
        if cost['id'] == id:
            costs.remove(cost)
            return ""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='object not found')
