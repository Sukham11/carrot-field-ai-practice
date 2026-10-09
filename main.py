import json

from fastapi import FastAPI, Path , HTTPException, Query # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from pydantic import BaseModel, Field # type: ignore
from typing import Annotated, Literal

app = FastAPI()

class Carrots(BaseModel):

    observation_id: Annotated[str, Field(..., description='id of observed carrots', example= 'OBS-001')]
    carrots_inspected: Annotated[int, Field(..., ge=0, description='number of carrots inspected')]
    row_id: Annotated[str, Field(..., description='Number of the row the carrot is from in the field', example= 'ROW-02')]
    field_id: Annotated[str, Field(..., description='field number for carrots', example= 'FIELD-001')]
    condition: Annotated[str, Field(..., description='tells the conditions of carrot roots or leaves')]
    description: Annotated[str, Field(..., description='decsibes the condiiton in lttle more detail')]
    severity: Annotated[Literal['none', 'low', "Moderate", "high"], Field(..., description="tells how sever carrt condition is")]
    
# this function loads the data from the json file
def load_data():
    with open('carrot_field_sample.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('carrot_field_sample.json', 'w') as f:
        json.dump(data, f, indent=4)

# this is endpoint using get method
@app.get("/")
def hello():
    return {'message' : 'Carrot field management system API'}

# this is endpoint using get method
@app.get('/about')
def about():
    return {'message' : 'Fully functional API to management carrot field and its related activities'}

# this endpoint gives all the data of carrot field
@app.get('/view')
def view():
    data = load_data()

    return data

# this endpount gives spcific data of carrot filed instead of all data 
@app.get('/carrot_field_sample/{field_id}')
def view_fields(field_id: str):
    # load all the carrots 
    data = load_data()

    for field in data["fields"]:
     if field["field_id"] == field_id:
        return field
     
    return {'error' : 'Carrot field not found'}

# this endpoint gives data of fields under observation 
@app.get('/observations/{field_id}')
def view_observations(field_id: str = Path(..., description="Field id of the carrots in the db", example='Field001')):
    # load all the fields 
    data = load_data()
    result = []  # create list to store all the observations
    for observations in data["observations"]:
        if observations["field_id"] == field_id:
            result.append(observations)  # add to list if field id matches

    if not result : # if no field id matches and nothing in the list
       #return {"error: no observation found. TRY AGAIN!"}
       raise HTTPException(status_code=404, detail='No oberservation found.TRY AGIAN!') # raise stauts code for error message 
    return (result) 

# use query function to sort data based on some columns     
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='sort on the basis of carrots_inspected, discoloration_estimate, observation_date'), order: str= Query('asc', description='sort in asc or desc order') ):
    valid_fields = ['carrots_inspected', 'observation_date', 'discolored_carrots_estimate']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")

    if order not in ['asc' , 'desc']:
        raise HTTPException(status_code=400, detail ='Invalid order select between asc or desc')

    data = load_data()

    sort_order = True if order=='desc' else  False
    
    sorted_data = sorted(data["observations"], key=lambda x:x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_observation(observation: Carrots):

    #load existing data
    data = load_data()

    #check if the field exist 
    field_found = False

    for field in data["fields"]:
        if field["field_id"] == observation.field_id:
            field_found = True
            break

        if not field_found:
            raise HTTPException(status_code=404, detail="Field does not exist")
        
    #check if the carrot observation exist already
    for existing in data["observations"]:
        if existing["observation_id"] == observation.observation_id:
            raise HTTPException(status_code=400, detail="Carrot observation already exists")
    
    #new observation add to database
    data["observations"].append(observation.model_dump())

    #save into json file 
    save_data(data)

    return JSONResponse(status_code=201, content={'message':"observation created successfully"})
