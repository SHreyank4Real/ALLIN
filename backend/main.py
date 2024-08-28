from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
import redis
import datetime

# datetime
current_datetime = datetime.datetime.now()
timestamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")


# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


KEYPREFIX="user:"
KEYSUFIX=":auth"

# Redis connection
redis_client = redis.StrictRedis(host="localhost", port="6380" ,password='', charset="utf-8", decode_responses=True)

# MongoDB connection
client = MongoClient('mongodb://<username>:<password>@localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']

# Pydantic model for the input data
class Item(BaseModel):
    key: str
    value: str

class User(BaseModel):
    username: str
    password: str

# Set data in MongoDB
@app.post("/data/set/")
async def set_data(item: Item):
    document = {item.key: item.value}
    result = collection.insert_one(document)
    if result.inserted_id:
        return {"message": "Data inserted successfully", "id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Failed to insert data")

# Get all data from MongoDB
@app.get("/data/get/")
async def get_data():
    data = list(collection.find())
    # Convert ObjectId to string for JSON serialization
    for item in data:
        item["_id"] = str(item["_id"])
    return {"data": data}

# Get password from Redis
@app.post("/get/auth/")
async def get_password(user: User):
    USERKEY = KEYPREFIX+str(user.username)+KEYSUFIX
    userpassword = redis_client.get(USERKEY)
    if userpassword == user.password:
        return {"access_token": "dummy_token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

# To run the app, use the following command:
# uvicorn script_name:app --reload



#TODO use variabels and make applicaion fault tolerant