#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Création des index sur la collection logs_plat
Usage: python3 create_indexes.py
"""

from pymongo import MongoClient

def create_indexes():
    client = MongoClient("mongodb://localhost:27017")
    db = client.logs_db
    col = db.logs_plat

    print("Création des index sur logs_plat...")

    # Index 1 : timestamp descendant + user_id ascendant
    result1 = col.create_index([("ts", -1), ("user_id", 1)])
    print(f"Index {result1} créé : {('ts', -1), ('user_id', 1)}")

    # Index 2 : course_id ascendant + timestamp descendant
    result2 = col.create_index([("course_id", 1), ("ts", -1)])
    print(f"Index {result2} créé : {('course_id', 1), ('ts', -1)}")

    # Optionnel : index simple sur user_id (pour les requêtes sans filtre temporel)
    result3 = col.create_index([("user_id", 1)])
    print(f"Index {result3} créé : user_id")

    # Lister les index
    print("\nIndex existants sur logs_plat :")
    for idx in col.list_indexes():
        print(idx["name"], "->", idx["key"])

if __name__ == "__main__":
    create_indexes()