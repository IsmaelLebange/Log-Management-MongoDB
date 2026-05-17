#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
import time
from datetime import datetime
from collections import defaultdict
from pymongo import MongoClient, errors

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017")
    return client.logs_db

def import_logs_aggregated(file_path, collection_name, batch_size=1000):
    db = connect_mongo()
    col = db[collection_name]
    
    print(f"Importation groupée (modèle aggloméré) depuis {file_path} vers {collection_name}...")
    
    # Dictionnaire pour agréger : clé = (user_id, heure_trunc)
    aggregated = defaultdict(lambda: {"events": []})
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line.strip())
            ts_str = doc.get("ts")
            if not ts_str:
                continue
            # Convertir la date
            dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            # Tronquer à l'heure
            hour_trunc = dt.replace(minute=0, second=0, microsecond=0)
            key = (doc["user_id"], hour_trunc)
            # Conserver les événements sans le champ ts (car on a l'heure)
            event = {k: v for k, v in doc.items() if k != "ts"}
            aggregated[key]["events"].append(event)
            aggregated[key]["user_id"] = doc["user_id"]
            aggregated[key]["hour"] = hour_trunc
    
    # Insérer par lots
    total = 0
    batch = []
    start_time = time.time()
    
    for (user_id, hour), data in aggregated.items():
        doc_aggregated = {
            "user_id": user_id,
            "hour": hour,
            "events": data["events"],
            "event_count": len(data["events"])
        }
        batch.append(doc_aggregated)
        if len(batch) >= batch_size:
            col.insert_many(batch, ordered=False)
            total += len(batch)
            elapsed = time.time() - start_time
            rate = total / elapsed if elapsed > 0 else 0
            print(f"Inséré {total} documents groupés en {elapsed:.2f} sec ({rate:.0f} docs/s)")
            batch = []
    
    if batch:
        col.insert_many(batch, ordered=False)
        total += len(batch)
        elapsed = time.time() - start_time
        rate = total / elapsed if elapsed > 0 else 0
        print(f"Inséré {total} documents groupés en {elapsed:.2f} sec ({rate:.0f} docs/s)")
    
    print(f"Terminé. {total} documents groupés (au lieu de {len(aggregated)} logs bruts).")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--collection", default="logs_agreg")
    parser.add_argument("--batch", type=int, default=1000)
    args = parser.parse_args()
    import_logs_aggregated(args.input, args.collection, args.batch)

if __name__ == "__main__":
    main()