from pymongo import MongoClient

from llm_cw.settings import settings

client = MongoClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=5000,
)

try:
    client.admin.command("ping")
    print("Mongo connected")
except Exception as e:
    print(f"Mongo connection failed: {e}")
    raise