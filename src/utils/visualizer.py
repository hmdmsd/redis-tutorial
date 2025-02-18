import matplotlib.pyplot as plt
import seaborn as sns

class RedisVisualizer:
    def __init__(self, redis_client):
        self.redis = redis_client

    def plot_ratings_distribution(self):
        """Plot movie ratings distribution"""
        ratings = []
        for key in self.redis.client.keys('movie:*'):
            movie = self.redis.client.hgetall(key)
            if 'rating' in movie:
                ratings.append(float(movie['rating']))
        
        plt.figure(figsize=(10, 6))
        sns.histplot(ratings, bins=20)
        plt.title('Distribution des notes de films')
        plt.xlabel('Note')
        plt.ylabel('Nombre de films')
        plt.show()