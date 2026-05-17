#!/usr/bin/env python3
from pymongo import MongoClient
import time
from datetime import datetime, timedelta

client = MongoClient("mongodb://localhost:27017")
db = client.logs_db
col = db.logs_agreg

# R1 : actions d'un utilisateur (tous temps) : on somme event_count
user = col.find_one({}, {"user_id": 1})["user_id"]
start = time.time()
pipeline_r1 = [
    {"$match": {"user_id": user}},
    {"$group": {"_id": None, "total": {"$sum": "$event_count"}}}
]
res = list(col.aggregate(pipeline_r1))
total_actions = res[0]["total"] if res else 0
print(f"R1 - Utilisateur {user} : {total_actions} actions, temps {time.time()-start:.4f}s")

# R2 : actions par cours (tous temps) - il faut déconstruire les events
start = time.time()
pipeline_r2 = [
    {"$unwind": "$events"},
    {"$match": {"events.course_id": {"$exists": True}}},
    {"$group": {"_id": "$events.course_id", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 20}
]
res2 = list(col.aggregate(pipeline_r2))
print(f"R2 - {len(res2)} cours, temps {time.time()-start:.4f}s")

# R3 : utilisateurs inactifs depuis plus de 5 jours (basé sur 'hour')
latest = col.find_one({}, sort=[("hour", -1)])["hour"]
seuil = latest - timedelta(days=5)
start = time.time()
pipeline_r3 = [
    {"$group": {"_id": "$user_id", "last_hour": {"$max": "$hour"}}},
    {"$match": {"last_hour": {"$lt": seuil}}},
    {"$count": "inactive"}
]
res3 = list(col.aggregate(pipeline_r3))
count = res3[0]["inactive"] if res3 else 0
print(f"R3 - Inactifs >5j : {count}, temps {time.time()-start:.4f}s")