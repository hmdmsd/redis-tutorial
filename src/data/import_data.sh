#!/bin/bash
sleep 15  # Attendre que Redis soit prêt
redis-cli -h redis < /data/import_actors.redis
redis-cli -h redis < /data/import_movies.redis
redis-cli -h redis < /data/import_users.redis
redis-cli -h redis < /data/import_theaters.redis
redis-cli -h redis < /data/import_create_index.redis