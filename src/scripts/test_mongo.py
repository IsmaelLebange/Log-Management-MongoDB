from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client.test_db
col = db.test_col
col.insert_one({"test": "ok"})
print("✅ Insertion réussie")