import json

from fastapi import FastAPI

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
@app.get('/carrot_field_sample/{field_id}')
def view_observations(field_id: str):
    # load all the fields 
    data = load_data()

    for observations in data["observations"]:
        if observations["field_id"] == field_id:
            return observations

    return {'error' : 'no observation for given carrot field. TRY AGAIN'}    

