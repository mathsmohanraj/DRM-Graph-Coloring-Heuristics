# Dynamic Graph Coloring Heuristics for Real-Time DRM Conflict Resolution

## Overview
This repository contains the Python implementation (using `NetworkX`) of a dynamic graph coloring heuristic model designed for real-time Digital Rights Management (DRM) conflict resolution in large-scale digital media platforms.

By modeling media assets as vertices and detected copyright claims as dynamically weighted edges, this algorithm assigns discrete chromatic values (Green, Yellow, Red) to instantly execute specific DRM policies such as monetization, revenue sharing, and global takedowns using the **Maximal Penalty Principle**.

## Experimental Results
The heuristic algorithm was tested against varying network sizes to evaluate its real-time performance and scalability. The localized recoloring approach ensures that processing time scales linearly O(Δ(v)).

| Test Case | Nodes ($\|V\|$) | Conflicts ($\|E\|$) | Nodes Recolored | Execution Time (ms) |
| :--- | :--- | :--- | :--- | :--- |
| 1. Small Network | 1,000 | 150 | 89 | 1.04 ms |
| 2. Shorts Mashup | 10,000 | 2,400 | 1,372 | 21.03 ms |
| 3. Live Broadcast | 50,000 | 8,500 | 4,982 | 94.01 ms |
| 4. Global Scale | 100,000 | 15,000 | 8,750 | 174.82 ms |

*(Note: Execution times may vary slightly based on hardware specifications, but the computational complexity remains strictly bounded by the node degree).*

## How to Run the Simulation

Ensure you have Python installed (3.8+ recommended).

1. Install the required dependencies:
   ```bash
   pip install networkx

 python drm_simulation.py
 
Author:
   M.Mohanraj

Department of Mathematics, Periyar Maniammai Institute of Science & Technology

Research Focus: Graph Theory, Algorithmic Complexity, and Graph Coloring Heuristics.
