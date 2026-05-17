#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import time
from datetime import datetime, timedelta
import csv
import os

def get_user_id():
    client = MongoClient("mongodb://localhost:27017")
    db = client.logs_db
    col = db.logs_plat
    doc = col.find_one({}, {"user_id": 1})
    return doc["user_id"] if doc else "u00001"

def get_course_id():
    client = MongoClient("mongodb://localhost:27017")
    db = client.logs_db
    col = db.logs_plat
    doc = col.find_one({"course_id": {"$exists": True}}, {"course_id": 1})
    return doc["course_id"] if doc else "CS001"

def run_queries():
    client = MongoClient("mongodb://localhost:27017")
    db = client.logs_db
    col = db.logs_plat

    user_id = get_user_id()
    course_id = get_course_id()

    print(f"Requêtes avec user_id={user_id}, course_id={course_id}\n")

    # R1 : Toutes les actions de cet utilisateur (sans limite de temps)
    start = time.time()
    count_r1 = col.count_documents({"user_id": user_id})
    elapsed_r1 = time.time() - start
    print(f"R1 - Actions de l'utilisateur {user_id} (tous temps) : {count_r1} actions")
    print(f"    Temps : {elapsed_r1:.4f} secondes\n")

    # R2 : Nombre d'actions par cours (tous temps) (au lieu de par jour)
    start = time.time()
    pipeline_r2 = [
        {"$match": {"course_id": {"$exists": True}}},
        {"$group": {"_id": "$course_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ]
    results_r2 = list(col.aggregate(pipeline_r2))
    elapsed_r2 = time.time() - start
    print(f"R2 - Actions par cours (tous temps) : {len(results_r2)} lignes")
    print(f"    Temps : {elapsed_r2:.4f} secondes\n")

    # R3 : Utilisateurs inactifs depuis plus de 5 jours (si logs récents)
    # On prend la date du log le plus récent dans la collection
    latest_doc = col.find_one({}, sort=[("ts", -1)])
    if latest_doc and "ts" in latest_doc:
        latest_ts = latest_doc["ts"]
        seuil = latest_ts - timedelta(days=5)
    else:
        seuil = datetime.now() - timedelta(days=5)

    start = time.time()
    pipeline_r3 = [
        {"$group": {"_id": "$user_id", "last_ts": {"$max": "$ts"}}},
        {"$match": {"last_ts": {"$lt": seuil}}},
        {"$count": "inactive_count"}
    ]
    result_r3 = list(col.aggregate(pipeline_r3))
    count_r3 = result_r3[0]["inactive_count"] if result_r3 else 0
    elapsed_r3 = time.time() - start
    print(f"R3 - Utilisateurs inactifs depuis plus de 5 jours : {count_r3}")
    print(f"    Temps : {elapsed_r3:.4f} secondes\n")

    os.makedirs("results", exist_ok=True)
    with open("results/query_times.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["requete", "temps_secondes", "nb_resultats"])
        writer.writerow(["R1", round(elapsed_r1, 4), count_r1])
        writer.writerow(["R2", round(elapsed_r2, 4), len(results_r2)])
        writer.writerow(["R3", round(elapsed_r3, 4), count_r3])
    print("Résultats sauvegardés dans results/query_times.csv")

if __name__ == "__main__":
    run_queries()