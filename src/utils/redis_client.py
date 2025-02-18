import redis

class RedisClient:
    def __init__(self, host='redis', port=6379, db=0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
    
    def ping(self):
        return self.client.ping()

    def get_movie(self, movie_id):
        """Get movie by ID"""
        return self.client.hgetall(f"movie:{movie_id}")

    def search_movies(self, query):
        """Search movies using RediSearch"""
        return self.client.execute_command('FT.SEARCH', 'idx:movie', query)

    def get_actor(self, actor_id):
        """Get actor by ID"""
        return self.client.hgetall(f"actor:{actor_id}")

    def get_user(self, user_id):
        """Get user by ID"""
        return self.client.hgetall(f"user:{user_id}")