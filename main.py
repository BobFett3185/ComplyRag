from distro import name
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()
# to run the server cd into your fastapi folder then use the command fastapi dev main.py 

# 1. Enable CORS (Critical for the frontend to talk to the backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/") # default route to test if the server is working
async def root():
    return {"message": "Hello World"}


#@something is a decorator in python which takes the function below and does something with it

@app.get("/hello") # this is a path operation decorator which tells that the function below uses this method and route
async def hello():
    return {"message": "Hello from the /hello route!"}



# path parameters
'''You have to put the variable in the path so the server knows to expect a variable there, 
then you can use it in the function as an argument and its used when the function is called

basically you can have dynamic routes with path parameters
'''

@app.get("/hello/{name}") # this route will take a name as a path parameter and return a personalized greeting
async def hello_name(name:str):
    return {"message": f"Hello {name}"}

# if you do type cast python automatically will convert to the required type if possible if not will throw e 
# with python type declaration, Fast api automatically validates the input and will return an error if the input is bad 

'''
Order matters in path definition, if you have a path parameter that can match multiple routes, it will match the first one it finds.
Don't put a variable path parameter before a static path, because it will match the variable path first and never reach the static 
path. for example if you have /hello/{name} and /hello/world, if you put /hello/{name} first, then /hello/world will never be
reached because it will match /hello/{name} with name=world and return "Hello world" instead of the intended message 
for /hello/world.

'''


'''
if you have a path parameter but you want possible valid paths to be predefined you use an enum, this 
way you can have a path parameter that only accepts certain values and will return an error if the value is not in the enum.
this is more efficient when an error occurs because it will return a 422 error instead of a 404 error, 
which is more accurate and faster to process.

ex:
'''

from enum import Enum
class Food(str, Enum):
    pizza = "pizza"
    burger = "burger"
    sushi = "sushi"

@app.get("/food/{foodName}") # route with foodName variable in path
async def get_food(foodName: Food): # declare that the variable is of the type Food(enum)
    if foodName == Food.pizza:
        return {"message": "You ordered pizza"}

    return {"message": f"You are getting {foodName.value}"} # .value gets the actual food not Food.foodname which is enum version

# in this case we use the enum to compare with the variable, not the variable compared to a string 

'''
# error handling with parameters in paths is pretty simple with fast api 
# data parsing and validation is also handled automatically by fast api when you 
# declare the type of the variable in the function arguments
# using enums to restrict/list the possible values of a path parameter is a good way to handle errors
'''

# QUERY PARAMETERS

'''
When you declare other function parameters that are not in the path these are called query parameters
These are parameters that are passed in the URL after the ?
for ex:
'''

fake_db = [{"item_id": 1, "name": "item1"}, {"item_id": 2, "name": "item2"}, {"item_id": 3, "name": "item3"}]

@app.get("/items/") # route to get items with optional query parameter
async def read_items(start: int = 0, limit: int = 10): # skip and limit are query parameters with default values
    return fake_db[start : start + limit] # return a slice of the fake_db based on the skip and limit values

'''
the query is the part of the url after ? and seperated by &

if you type cast the parameter will automatically convert to the required type if possible, if not it will throw an error

same processes/benefits that path parameters have 

If you dont give any specificed parameters the default is assumed

'''


# you can mix path parameters and query parameters in the same route 
@app.get("/search/{query}") # route to search items with a query parameter
async def search_items(query: str, q: str| None = None): # query is a required query parameter but q is optional
    if q:
        return {"message": f"Searching for {query} with additional query {q}"}
    
    return {"message": f"Searching for {query}"}

# set the q parameter to optional

# when you specify in url : http://127.0.0.1:8000/search/hello?q=cheese

#boolean query parameters are automatically converted to boolean values if you declare the type as bool

'''
you can declare multiple path parameters and query parameters in the same route 

Also 

when you want a query parameter to be optional you can just give it a default value, 
then the parameter is optional and will use the default value if not provided by user

if you want to make a query parameter optional but also dont want a default value just set default to None 


'''

#REQUEST BODY
'''
A request body is the way to send data from from client to API
A response body is the data your api send back to the client 

You almost always have to send a response body but you dont alwasy have a request body, for example in a GET request you usually dont have a request body (get)


'''
from pydantic import BaseModel 

# this guarantees data is correct before it reaches the function. If data is incorrect it returns error 
class Item(BaseModel): # make some class 
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/") # route to create an item with a request body
async def create_item(item: Item): # declare that the request body should be of type Item
    item_dict = item.model_dump() # convert the item to a dictionary
    if item.tax is not None:
        total_price = item.price + item.tax
        item_dict.update({"total_price": total_price}) # add the total price to the dictionary
    
    return item_dict

'''
With this, fast api will automatically parse the request body as json and convert it to an instance of the Item class
it will convert types and validate data as needed 

inside of the function you can access all the attributes of of the model object directly

You can pass a request body and path and query parameter in the same route and fast api will handle it all for you, just declare the parameters in the function arguments 

if the parameter is in the path then its obviouslt a path parameter
if the parameter is of a single type then it will be a query parameter
if the parameter is a pydantic model then its a request body


Summary
Path parameter is the broader route that we should go to and a general direction/topic. 
The query parameter is the more specific endpoint and tells you some more details. 
The request body for a post request is usally long and contains lots of information which you can then extract and use
'''



from chatbot import getResponse # this is the function we created in chatbot.py to get the response from the chatbot

class Query (BaseModel):
    message: str

# endpoint for chat feature
@app.post("/chat")
async def chat(query: Query): # whatever query is passed has to follow the query class
    response = getResponse(query.message)
    #response = f"Bot received: {query.message}"

    return {"response": response}




