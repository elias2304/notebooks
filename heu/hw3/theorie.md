# Particle Swarm Optimization 
- Explain the basic idea of particle swarm optimization (PSO).
  - 
- What are the mechanisms to steer the interplay between diversification and intensification
in PSO?
-  Discuss the advantages and disadvantages of PSO in comparison to other population and
trajectory-based optimization strategies

# Ant Colony Optimization
- Explain the basic idea of ant colony optimization (ACO).
  - An ant in itself is very limited, but as a swarm, they are very effective
  - Ants emit pheromones during search -> ants have a higher likelihood to follow a path with high pheromones
  - That is also the idea of the algorithm: a lot of agents (ants) are left on a field (graph) and they are moving and the pheromones (weights) are getting updated
- What are the mechanisms to steer the interplay between diversification and intensification in ACO?
  - diversification: exploration / try out new paths
  - intensification: exploitation / use whats is known to be working
  - What the ant does, is based on a probability, that is calculated by the number of remaining nodes, pheromones on the edges and distances of the edges
- Discuss the advantages and disadvantages of ACO in comparison to other population and trajectory-based optimization strategies
  - 
    

# Variable Neighbourhood Search
**Done in hw3.ipynb**


Use both instances provided on Moodle. The files are provided in the following format:
Line 1: Number of items (𝑛)
Line 2: Capacity of the bins (𝑐)
Rest of the file:
- For each item 𝑗(𝑗 = 1, . . . , 𝑛):
    - Weight (𝑤𝑗)

Read in the items (id, weight) from the file. Create a bin class with an (id, capacity, items).

Create an initial random solution for this problem.
- How to reach a neighbouring solution based on your chosen encoding?
- Implement 2 neighbourhood operators.

Implement a Variable Neighbourhood Search with 3 neighbourhood sizes (1, 2, 3 changes) and
evaluate 30 neighbourhood solutions per neighbourhood size. ➔ 30 x 1 change, 30 x 2 change,
30 x 3 changes. Use first improvement in your algorithm. When generating neighbouring
solutions, randomly use on of the two neighbourhood operators.
- How much improvement could be reached over the randomly generated instance for the small instances?
- How much improvement could be reached over the randomly generated instance for the large instances?
- Visualize the result

