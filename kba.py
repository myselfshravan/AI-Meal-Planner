import networkx as nx
from queue import PriorityQueue
import time

class Hotel:
    def __init__(self, name, location, price, rating):
        self.name = name
        self.location = location
        self.price = price
        self.rating = rating

class HotelKnowledgeBase:
    def __init__(self):
        self.hotels = []
        self.graph = nx.Graph()

    def tell(self, hotel):
        self.hotels.append(hotel)
        self.graph.add_node(hotel.name, data=hotel)

    def ask(self, query):
        return self.graph.nodes[query]['data'] if query in self.graph.nodes else None

    def add_relation(self, hotel1, hotel2):
        self.graph.add_edge(hotel1.name, hotel2.name)

    def get_recommendations(self, start_hotel, algorithm='dfs'):
        if algorithm == 'dfs':
            start_time = time.time()
            recommendations = self.dfs(start_hotel)
            end_time = time.time()
        elif algorithm == 'bfs':
            start_time = time.time()
            recommendations = self.bfs(start_hotel)
            end_time = time.time()
        elif algorithm == 'best_first':
            start_time = time.time()
            recommendations = self.best_first(start_hotel)
            end_time = time.time()

        execution_time = end_time - start_time
        return recommendations, execution_time

    def dfs(self, start_hotel):
        visited = set()
        stack = [(start_hotel, [start_hotel])]
        recommendations = []

        while stack:
            current_hotel, path = stack.pop()

            if current_hotel not in visited:
                visited.add(current_hotel)

                if current_hotel != start_hotel:
                    recommendations.append(current_hotel)

                neighbors = self.graph.neighbors(current_hotel)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))

        return recommendations

    def bfs(self, start_hotel):
        visited = set()
        queue = PriorityQueue()
        queue.put((start_hotel, [start_hotel]))
        recommendations = []

        while not queue.empty():
            current_hotel, path = queue.get()

            if current_hotel not in visited:
                visited.add(current_hotel)

                if current_hotel != start_hotel:
                    recommendations.append(current_hotel)

                neighbors = self.graph.neighbors(current_hotel)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.put((neighbor, path + [neighbor]))

        return recommendations

    def best_first(self, start_hotel):
        visited = set()
        priority_queue = PriorityQueue()
        priority_queue.put((start_hotel, [start_hotel]))
        recommendations = []

        while not priority_queue.empty():
            current_hotel, path = priority_queue.get()

            if current_hotel not in visited:
                visited.add(current_hotel)

                if current_hotel != start_hotel:
                    recommendations.append(current_hotel)

                neighbors = self.graph.neighbors(current_hotel)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        priority_queue.put((neighbor, path + [neighbor]))

        return recommendations

# Example usage:
kb = HotelKnowledgeBase()

hotel1 = Hotel("Hotel A", "City X", 100, 4.5)
hotel2 = Hotel("Hotel B", "City X", 150, 6.0)
hotel2 = Hotel("Hotel B", "City X", 150, 4.2)
hotel3 = Hotel("Hotel C", "City Y", 200, 4.7)
hotel4 = Hotel("Hotel D", "City Y", 120, 4.1)
hotel5 = Hotel("Hotel E", "City Z", 180, 4.9)

kb.tell(hotel1)
kb.tell(hotel2)
kb.tell(hotel3)
kb.tell(hotel4)
kb.tell(hotel5)

kb.add_relation(hotel1, hotel2)
kb.add_relation(hotel1, hotel3)
kb.add_relation(hotel2, hotel4)
kb.add_relation(hotel3, hotel5)

start_hotel = "Hotel A"

# Get first available hotels
available_hotels = [hotel.name for hotel in kb.hotels]
print("Available Hotels:")
if available_hotels:
    print(available_hotels[0])
else:
    print("No hotels available.")

# Get recommendations using DFS
recommendations_dfs, time_dfs = kb.get_recommendations(start_hotel, algorithm='dfs')

print("\nDFS Recommendations:")
if recommendations_dfs:
    print(recommendations_dfs[0])
else:
    print("No recommendations found.")

print("DFS Time:", time_dfs)

# Get recommendations using BFS
recommendations_bfs, time_bfs = kb.get_recommendations(start_hotel, algorithm='bfs')

print("\nBFS Recommendations:")
if recommendations_bfs:
    print(recommendations_bfs[0])
else:
    print("No recommendations found.")

print("BFS Time:", time_bfs)

# Get recommendations using Best-First Search
recommendations_best_first, time_best_first = kb.get_recommendations(start_hotel, algorithm='best_first')

print("\nBest-First Recommendations:")
if recommendations_best_first:
    print(recommendations_best_first[0])
else:
    print("No recommendations found.")

print("Best-First Time:", time_best_first)
