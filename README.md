# rideshare-path-planning

### Introduction

This project explores the solution to a simplified version of a ride-sharing problem that is faced by ride service apps such as Uber and Lyft. The goal is to design an optimal path planning strategy based on parameters such as ride time and user experience.

This is implemented in three phases:

1. **Phase 1:** Static path planning on a 2D grid 
2. **Phase 2:** Implementing route and user quality cost functions for a single taxi 
3. **Phase 3:** Dynamic path planning, with changing user requests as the taxi moves

### Phase 1: Static Path Planning

Phase 1 assumes the simplest case, where a single taxi exists for multiple users. The pickup and drop off locations for each user is known in advance. 

The map is represented by a 2D grid, where each node is represented by an ordered pair of coordinates $(x,y)$ and each edge represents a valid path between adjacent nodes. All edges have a uniform cost, allowing for the shortest path to be computed using Manhattan distances. 

The taxi must visit each pickup location before its corresponding drop off location, with the goal of determining the order of locations that minimizes total travel distance.

**Key Assumptions for Phase 1:**

- Number of taxis: $m$ = 1,
- Number of users: $n$ = 3
- Customer $A$ is always picked up first (Without Loss of Generality)
- all edges of the graph have an equal weight


