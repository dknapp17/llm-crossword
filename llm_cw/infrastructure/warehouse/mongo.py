import uuid
from abc import ABC
from typing import Generic, Type, TypeVar

from loguru import logger
from pydantic import UUID4, BaseModel, Field
from pymongo import MongoClient, errors

from llm_cw.settings import settings

client = MongoClient(settings.MONGO_URI)

database = client[settings.MONGO_DATABASE]


# -------------------------
# Mongo connection
# -------------------------
_client = MongoClient(settings.MONGO_URI)
_database = _client[settings.MONGO_DATABASE]


# -------------------------
# Generic document type
# -------------------------
T = TypeVar("T", bound="NoSQLBaseDocument")


class NoSQLBaseDocument(BaseModel, ABC, Generic[T]):
    """
    Base class for all Mongo-backed domain documents.
    """

    id: UUID4 = Field(default_factory=uuid.uuid4)

    # -------------------------
    # equality
    # -------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    # -------------------------
    # Mongo serialization
    # -------------------------
    def to_mongo(self) -> dict:
        data = self.model_dump()

        # convert id -> _id
        data["_id"] = str(data.pop("id"))

        # ensure UUIDs are strings
        for k, v in data.items():
            if isinstance(v, uuid.UUID):
                data[k] = str(v)

        return data

    @classmethod
    def from_mongo(cls: Type[T], data: dict) -> T:
        if not data:
            raise ValueError("Empty Mongo document")

        data = dict(data)
        data["id"] = data.pop("_id")

        return cls(**data)

    # -------------------------
    # persistence ops
    # -------------------------
    def save(self: T) -> T | None:
        collection = _database[self.get_collection_name()]

        try:
            collection.insert_one(self.to_mongo())
            return self
        except errors.PyMongoError:
            logger.exception("Failed to insert document")
            return None

    @classmethod
    def find(cls: Type[T], **filters) -> list[T]:
        collection = _database[cls.get_collection_name()]
        try:
            return [
                cls.from_mongo(doc)
                for doc in collection.find(filters)
            ]
        except errors.PyMongoError:
            logger.exception("Failed to query documents")
            return []
        
    @classmethod
    def get_by_id(cls: Type[T], doc_id: str) -> T | None:
        collection = _database[cls.get_collection_name()]

        doc = collection.find_one({"_id": doc_id})

        if doc:
            return cls.from_mongo(doc)

        return None

    @classmethod
    def get_or_create(cls: Type[T], **filters) -> T:
        collection = _database[cls.get_collection_name()]

        try:
            doc = collection.find_one(filters)
            if doc:
                return cls.from_mongo(doc)

            instance = cls(**filters)
            instance.save()
            return instance

        except errors.PyMongoError:
            logger.exception("get_or_create failed")
            raise

    @classmethod
    def bulk_insert(cls: Type[T], items: list[T]) -> bool:
        collection = _database[cls.get_collection_name()]

        try:
            collection.insert_many([i.to_mongo() for i in items])
            return True
        except errors.PyMongoError:
            logger.exception("bulk insert failed")
            return False

    @classmethod
    def vector_search(
        cls,
        embedding: list[float],
        limit: int = 5,
    ) -> list:

        collection = _database[cls.get_collection_name()]

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "clue_embedding_index",
                    "path": "clue_embedding",
                    "queryVector": embedding,
                    "numCandidates": 100,
                    "limit": limit,
                }
            },
            {
                "$addFields": {
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        return list(collection.aggregate(pipeline))

    # -------------------------
    # required by subclasses
    # -------------------------
    @classmethod
    def get_collection_name(cls) -> str:
        if not hasattr(cls, "Settings"):
            raise ValueError("Missing Settings class")

        return cls.Settings.name