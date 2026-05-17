#!/usr/bin/env python3
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client.logs_db
plat = db.logs_plat
agreg = db.logs_agreg

# Récupérer la dernière heure agrégée (optionnel)
last = agreg.find_one({}, sort=[("hour", -1)])
since = last["hour"] if last else datetime(1970, 1, 1)
print(f"Aggrégation depuis {since}")

pipeline = [
    {"$match": {"ts": {"$gte": since}}},
    {"$group": {
        "_id": {
            "user_id": "$user_id",
            "hour": {"$dateTrunc": {"date": "$ts", "unit": "hour"}}
        },
        "events": {"$push": {"event": "$event", "course_id": "$course_id"}},
        "event_count": {"$sum": 1}
    }},
    {"$project": {"_id": 0, "user_id": "$_id.user_id", "hour": "$_id.hour", "events": 1, "event_count": 1}}
]

cursor = plat.aggregate(pipeline, allowDiskUse=True)
batch = []
total = 0
for doc in cursor:
    batch.append(doc)
    if len(batch) >= 1000:
        agreg.insert_many(batch, ordered=False)
        total += len(batch)
        print(f"Inséré lot de {len(batch)} docs (total {total})")
        batch = []
if batch:
    agreg.insert_many(batch, ordered=False)
    total += len(batch)
    print(f"Inséré dernier lot, total {total}")

print("Terminé.")