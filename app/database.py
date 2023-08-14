from pymongo import mongo_client
import pymongo
from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)

db = client[settings.MONGO_INITDB_DATABASE]
ApiRequest = db.api_requests
ApiRequest.create_index([("route", pymongo.ASCENDING)], unique=False)

Credentials = db.credentials
Credentials.create_index(
    [
        ("store_department_key", pymongo.ASCENDING),
        ("store_department_id", pymongo.ASCENDING),
    ],
    unique=True,
)

User = db.mock_users
