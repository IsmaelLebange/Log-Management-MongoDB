#!/bin/bash

# Nettoyer les anciens dossiers de données (optionnel : pour repartir de zéro)
rm -rf ~/data/shard1 ~/data/shard2 ~/data/config
mkdir -p ~/data/shard1 ~/data/shard2 ~/data/config

echo "=== Lancement du config server (port 27020) ==="
mongod --configsvr --replSet configReplSet --port 27020 --dbpath ~/data/config --fork --logpath ~/data/config.log --bind_ip localhost

sleep 2

echo "=== Lancement du shard1 (port 27018) ==="
mongod --shardsvr --replSet shard1ReplSet --port 27018 --dbpath ~/data/shard1 --fork --logpath ~/data/shard1.log --bind_ip localhost

sleep 2

echo "=== Lancement du shard2 (port 27019) ==="
mongod --shardsvr --replSet shard2ReplSet --port 27019 --dbpath ~/data/shard2 --fork --logpath ~/data/shard2.log --bind_ip localhost

sleep 2

echo "=== Initialisation des replica sets ==="
mongosh --port 27020 --eval "rs.initiate({_id: 'configReplSet', configsvr: true, members: [{_id: 0, host: 'localhost:27020'}]})"
mongosh --port 27018 --eval "rs.initiate({_id: 'shard1ReplSet', members: [{_id: 0, host: 'localhost:27018'}]})"
mongosh --port 27019 --eval "rs.initiate({_id: 'shard2ReplSet', members: [{_id: 0, host: 'localhost:27019'}]})"

sleep 5

echo "=== Lancement du routeur mongos (port 27017) ==="
mongos --configdb configReplSet/localhost:27020 --port 27017 --fork --logpath ~/data/mongos.log --bind_ip localhost

sleep 3

echo "=== Ajout des shards et activation du sharding ==="
mongosh --port 27017 --eval "
sh.addShard('shard1ReplSet/localhost:27018');
sh.addShard('shard2ReplSet/localhost:27019');
sh.enableSharding('logs_db');
sh.shardCollection('logs_db.logs_plat', { user_id: 'hashed' });
"

echo "=== Vérification du statut ==="
mongosh --port 27017 --eval "sh.status()"

echo "Sharding terminé. Utilisez 'mongosh --port 27017' pour te connecter."