""" 
Author: Elias Schweighuber
Date: 16.11.2026
Exercise:
"""
import json
import os
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output

class Point:
    def __init__(self, point_id, x, y):
        self.id = point_id
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.id}, {self.x}, {self.y})"

    def to_dict(self):
        return {"id": self.id, "x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["x"], data["y"])

class Tour:
    def __init__(self, points):
        self.points = points.copy()

    def generate_random(self):
        random.shuffle(self.points)

    def total_distance(self):
        # sqrt(x^2 + y^2)
        # modulo is for last point to first
        return sum(
            ((self.points[i].x - self.points[(i + 1) % len(self.points)].x)**2 +
             (self.points[i].y - self.points[(i + 1) % len(self.points)].y)**2)**0.5
            for i in range(len(self.points))
        )

    def plot(self, title="Tour"):
        fig, ax = plt.subplots(figsize=(10, 8))

        xs = [p.x for p in self.points] + [self.points[0].x]
        ys = [p.y for p in self.points] + [self.points[0].y]

        ax.plot(xs, ys, marker='o', linestyle='-', color='dodgerblue', markersize=6)
        ax.plot([xs[0]], [ys[0]], marker='s', color='green', markersize=9, label='Start Point')
        ax.legend()
        ax.set_title(title)
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_xlim(-50, 1050)
        ax.set_ylim(-50, 1050)
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.show()

HW1_DIR = "../hw1"

def load_instances(filename=os.path.join(HW1_DIR, "instances.json")):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [[Point.from_dict(p) for p in pts] for pts in data.values()]

def save_tour_to_file(tour, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{tour.total_distance():.2f}\n\n")
        for p in tour.points:
            f.write(f"{p.id} {float(p.x):.1f} {float(p.y):.1f}\n")

def read_tour_result(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    dist = float(lines[0])
    points = [Point(int(p[0]), float(p[1]), float(p[2])) for p in (line.split() for line in lines[1:])]
    return dist, points

def read_all_tour_results(folder_path):
    files = sorted(
        [f for f in os.listdir(folder_path) if f.startswith("tour_instance_")],
        key=lambda f: int(f.split("_")[-1].split(".")[0])
    )
    results = []
    for fn in files:
        iid = int(fn.split("_")[-1].split(".")[0])
        dist, pts = read_tour_result(os.path.join(folder_path, fn))
        results.append({
            "instance_id": iid,
            "filename": fn,
            "distance": dist,
            "points": pts,
            "tour": Tour(pts)
        })
    return results

def tournament_selection(population, distances, k=3):
    selected_indices = random.sample(range(len(population)), k)
    best_idx = min(selected_indices, key=lambda i: distances[i])
    return population[best_idx]

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]

    copied_ids = {p.id for p in child[start:end + 1]}
    remaining = [p for p in parent2 if p.id not in copied_ids]

    rem_idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = remaining[rem_idx]
            rem_idx += 1
    return child

def swap_mutation(individual, mutation_chance=0.05):
    mutated = individual.copy()
    if random.random() < mutation_chance:
        i, j = random.sample(range(len(mutated)), 2)
        mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated

def genetic_algorithm(points, pop_size=100, generations=1000, mutation_chance=0.05, elite_size=1, tournament_k=3):
    population = [random.sample(points, len(points)) for _ in range(pop_size)]

    for _ in range(generations):
        distances = [Tour(ind).total_distance() for ind in population]
        sorted_indices = sorted(range(pop_size), key=lambda i: distances[i])

        new_population = [population[i].copy() for i in sorted_indices[:elite_size]]

        while len(new_population) < pop_size:
            p1 = tournament_selection(population, distances, k=tournament_k)
            p2 = tournament_selection(population, distances, k=tournament_k)
            child = ordered_crossover(p1, p2)
            child = swap_mutation(child, mutation_chance)
            new_population.append(child)

        population = new_population

    distances = [Tour(ind).total_distance() for ind in population]
    best_idx = min(range(pop_size), key=lambda i: distances[i])
    return Tour(population[best_idx])

random.seed(42)
instances = load_instances()
ga_folder = os.path.join(HW1_DIR, "results", "genetic_algorithm")
os.makedirs(ga_folder, exist_ok=True)


nn_results = read_all_tour_results(os.path.join(HW1_DIR, "results", "nearest_neighbour"))
rnd_results = read_all_tour_results(os.path.join(HW1_DIR, "results", "random_tour"))
ga_results = read_all_tour_results(os.path.join(HW1_DIR, "results", "genetic_algorithm"))

nn_dists = [r["distance"] for r in nn_results]
rnd_dists = [r["distance"] for r in rnd_results]
ga_dists = [r["distance"] for r in ga_results]


def run_ga_live_plot(points, pop_size=100, generations=1000, mutation_chance=0.05, elite_size=1, tournament_k=3,
                     live=True, plot_every=50):
    random.seed(42)
    population = [random.sample(points, len(points)) for _ in range(pop_size)]
    best_history, avg_history, worst_history = [], [], []

    for gen in range(generations):
        distances = [Tour(ind).total_distance() for ind in population]
        best_history.append(min(distances))
        avg_history.append(sum(distances) / len(distances))
        worst_history.append(max(distances))

        if live and (gen % plot_every == 0 or gen == generations - 1):
            clear_output(wait=True)
            plt.figure(figsize=(8, 4))
            plt.plot(best_history, label="Best", color="green")
            plt.plot(avg_history, label="Average", color="dodgerblue")
            plt.plot(worst_history, label="Worst", color="crimson", alpha=0.6)
            plt.title(f"GA Progress (k={tournament_k}) - Generation {gen + 1}/{generations}")
            plt.xlabel("Generation")
            plt.ylabel("Tour Distance")
            plt.legend()
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.show()

        sorted_indices = sorted(range(pop_size), key=lambda i: distances[i])
        new_population = [population[i].copy() for i in sorted_indices[:elite_size]]

        while len(new_population) < pop_size:
            p1 = tournament_selection(population, distances, k=tournament_k)
            p2 = tournament_selection(population, distances, k=tournament_k)
            child = ordered_crossover(p1, p2)
            child = swap_mutation(child, mutation_chance)
            new_population.append(child)

        population = new_population

    return best_history, avg_history, worst_history


# Set plot_every=1 to redraw on every single generation
best_k3, avg_k3, worst_k3 = run_ga_live_plot(instances[0], tournament_k=3, live=True, plot_every=50)
