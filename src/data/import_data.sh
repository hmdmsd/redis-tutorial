#!/bin/bash

# Attendre que Redis soit prêt
until redis-cli -h redis ping; do
  echo "Waiting for Redis to be ready..."
  sleep 1
done

echo "Redis is ready. Importing data..."

# Importer les données
redis-cli -h redis < /home/jovyan/work/data/import_actors.redis
redis-cli -h redis < /home/jovyan/work/data/import_movies.redis
redis-cli -h redis < /home/jovyan/work/data/import_users.redis
redis-cli -h redis < /home/jovyan/work/data/import_theaters.redis
redis-cli -h redis < /home/jovyan/work/data/import_create_index.redis

echo "Data import completed!"