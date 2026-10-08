import json

from fastapi import FastAPI, Path , HTTPException, Query

app = FastAPI()

# this function loads the data from the json file
def load_data():
    with open('carrot_field_sample.json', 'r') as f:
        data = json.load(f)

    return data
    
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
    
    sorted_data = sorted(data.values(), key=lambda x:x.ge(sort_by, 0), reverse=False)

    return sorted_data