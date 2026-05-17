#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
import time
from datetime import datetime
from pymongo import MongoClient, errors

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017")
    db = client.logs_db
    return db

def import_logs(file_path, collection_name, batch_size=10000):
    db = connect_mongo()
    col = db[collection_name]
    
    print(f"Importation des logs depuis {file_path} vers {collection_name}...")
    start_time = time.time()
    batch = []
    total = 0
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                doc = json.loads(line.strip())
                # Convertir le champ 'ts' en datetime (car il est au format ISO string)
                if "ts" in doc:
                    doc["ts"] = datetime.fromisoformat(doc["ts"].replace("Z", "+00:00"))
                batch.append(doc)
                total += 1
                
                if len(batch) >= batch_size:
                    col.insert_many(batch, ordered=False)
                    elapsed = time.time() - start_time
                    rate = total / elapsed if elapsed > 0 else 0
                    print(f"Importé {total} documents en {elapsed:.2f} sec ({rate:.0f} docs/s)")
                    batch = []
            except json.JSONDecodeError as e:
                print(f"Erreur JSON: {e}")
            except errors.BulkWriteError as e:
                print(f"Erreur insertion: {e.details}")
                batch = []
    
    if batch:
        col.insert_many(batch, ordered=False)
        elapsed = time.time() - start_time
        rate = total / elapsed if elapsed > 0 else 0
        print(f"Importé {total} documents en {elapsed:.2f} sec ({rate:.0f} docs/s)")
    
    print(f"Terminé. Total: {total} documents.")
    return total

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--collection", default="logs_plat")
    parser.add_argument("--batch", type=int, default=10000)
    args = parser.parse_args()
    import_logs(args.input, args.collection, args.batch)

if __name__ == "__main__":
    main()