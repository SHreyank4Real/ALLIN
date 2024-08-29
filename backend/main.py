from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
import redis
import datetime
import os

current_datetime = datetime.datetime.now()
timestamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

REDIS_HOST = os.environ.get('REDIS_HOST', 'dummy')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', 'dummy')
MONGODB_HOST = os.environ.get('MONGODB_HOST', 'dummy')
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', 'dummy')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', 'dummy')
MONOGODB_DBNAME = os.environ.get('MONOGODB_DBNAME', 'dummy')
MONOGODB_COLLECTION = os.environ.get('MONOGODB_COLLECTION', 'dummy')


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

redis_client = redis.StrictRedis(host=REDIS_HOST, port="6380" ,password=REDIS_PASSWORD, charset="utf-8", decode_responses=True)

client = MongoClient('mongodb://'+MONGODB_USERNAME+':'+MONGODB_PASSWORD+'@'+MONGODB_HOST+':27017/')
db = client[MONOGODB_DBNAME]
collection = db[MONOGODB_COLLECTION]

class Item(BaseModel):
    key: str
    value: str

class User(BaseModel):
    username: str
    password: str

@app.post("/data/set/")
async def set_data(item: Item):
    document = {item.key: item.value}
    result = collection.insert_one(document)
    if result.inserted_id:
        return {"message": "Data inserted successfully", "id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Failed to insert data")

@app.get("/data/get/")
async def get_data():
    data = list(collection.find())
    for item in data:
        item["_id"] = str(item["_id"])
    return {"data": data}

@app.post("/get/auth/")
async def get_password(user: User):
    USERKEY = KEYPREFIX+str(user.username)+KEYSUFIX
    userpassword = redis_client.get(USERKEY)
    if userpassword == user.password:
        return {"access_token": "dummy_token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")

#TODO use variabels and make applicaion fault tolerant