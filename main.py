from fastapi import FastAPI, status, HTTPException


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

@app.post('/costs',status_code= status.HTTP_201_CREATED)
def add_cost(amount: float, description: str):
    max_id = 0
    for cost in costs:
        if cost["id"] > max_id:
            max_id = cost["id"]
    
    new_cost = {
        'id': max_id + 1,
        'amount': amount,
        'description': description
    }
    costs.append(new_cost)
    
    # return costs


@app.get('/costs',status_code= status.HTTP_200_OK)
def receive_costs():
    return costs


@app.get('/costs/{id}',status_code= status.HTTP_200_OK)
def receive_costs(id:int):
    
    for cost in costs:
        if cost["id"] == id:
            return cost
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='object not found')


@app.put('/costs/{id}',status_code= status.HTTP_200_OK)
def edit_costs(id: int, amount: float, description: str):

    for cost in costs:
        if cost["id"] == id:
            costs[id] = {
                "id": id,
                "amount": amount,
                "description": description
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
