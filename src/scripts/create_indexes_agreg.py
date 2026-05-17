#!/usr/bin/env python3
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.logs_db
col = db.logs_agreg

print("Création index sur logs_agreg...")
col.create_index([("user_id", 1)])
col.create_index([("hour", -1)])
print("Index créés.")