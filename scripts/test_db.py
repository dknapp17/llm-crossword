from llm_cw.infrastructure.warehouse.mongo import database

print(database.name)
print(database.list_collection_names())