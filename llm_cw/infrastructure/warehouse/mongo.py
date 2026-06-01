from pymongo import MongoClient

from llm_cw.settings import settings

client = MongoClient(settings.mongo_uri)

database = client[settings.mongo_database]