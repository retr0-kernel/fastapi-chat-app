from fastapi import FastAPI #Import FastAPI because that's the server framework we are using 
from fastapi.middleware.cors import CORSMiddleware #Importing CORSMiddleware because we will be making API calls from other websites 
from pydantic import BaseModel #Interface for request bodies for logging in and signing up
from typing import Union
import requests #making API calls to chatengine.io 

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # The middleware is configured to allow any origin
    allow_credentials=True, # Allows the use of cookies, HTTP authentication, and TLS client   certificates for cross-origin requests.
    allow_methods=["*"], # The middleware is configured to allow any HTTP method
    allow_headers=["*"], #The middleware is configured to allow any headers
)

PROJECT_ID = "11b05d69-1f2a-4f98-8e14-03e50f099ec2"
PRIVATE_KEY = "8c881691-9113-423f-9197-5099d6fa1813"

class User(BaseModel):
    username: str #declaring a username which is a string
    secret: str #declaring a secret which is string 
    email: Union[str, None] = None    # optionally add these which can be a string or none and by default its None
    first_name: Union[str, None] = None  # optionally add these which can be a string or none and by default its None
    last_name: Union[str, None] = None  # optionally add these which can be a string or none and by default its None

#Adding first route
@app.post('/login/')
async def root(user: User):
    response = requests.get('https://api.chatengine.io/users/me/', 
        headers={ 
            "Project-ID": PROJECT_ID,
            "User-Name": user.username,
            "User-Secret": user.secret
        }
    )
    return response.json()

# Instead of fetching a user with a GET request we are creating a user using POST request
@app.post('/signup/')
async def root(user: User):
    response = requests.post('https://api.chatengine.io/users/', 
        data={
            "username": user.username,
            "secret": user.secret,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        headers={ "Private-Key": PRIVATE_KEY }
    )
    return response.json()

# python3 -m venv venv
# source venv/bin/activate
# pip install --upgrade pip
# pip install -r requirements.txt
# uvicorn main:app --reload --port 3001