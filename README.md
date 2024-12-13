# ALLIN
ALLIN

docker run --name mongodb -d -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=adminpass \
    mongo


export MONGODB_USERNAME="admin"
export MONGODB_PASSWORD="adminpass"
export MONGODB_HOST="localhost"
export MONOGODB_DBNAME="mydatabase"
export MONOGODB_COLLECTION="mycollection"
export REDIS_HOST="localhost"
export REDIS_PASSWORD=""


python3 -m uvicorn main:app --reload