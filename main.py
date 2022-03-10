#run with: uvicorn main:app --reload
#https://pydantic-docs.helpmanual.io/usage/types/#pydantic-types
#Python
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel
from pydantic import Field
#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models
class HairColor(Enum):
    BLACK = 'black'
    BLOND = 'blond'
    RED = 'red'

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    
    class Config:
        schema_extra = {
            "example": {#is mandatory use example at the biginning - just for swagger
                "first_name": "Jeersson",
                "last_name": "Maradiaga Carballo",
                "age": 25,
                "hair_color": HairColor.BLOND,
                "is_married": False
            }
        }

@app.get("/")
def home():
    return {"Hello": "Hello World"}

# Request and Response body
@app.post("/person/new")
def create_person(person: Person = Body(..., embed=True)):
    return person

# Validation: Query Parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person's name",
        description="The name of the person you are looking for",
        example="Jeersson"
        ),
    age: str = Query(
        ...,
        title="Person's age",
        description="The age of the person you are looking for",
        example="25"
        )
):
    return {name: age}

# Validation: Path Parameters
@app.get("/person/details/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person's ID",
        description="The ID of the person you are looking for",
        example=123
        )
):
    return {person_id: "It exists!"}

# Validation: Body Parameters
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person's ID",
        description="The ID of the person you are looking for",
        example=123
        ),
    person: Person = Body(
        ...,
        title="Person's details",
        description="The details of the person you are looking for",
        ),
    #location: Location = Body(...)
):
    #results = person.dict()
    #results.update(location.dict())
    return person