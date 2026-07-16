import networkx as nx
import time
import random

def run_drm_simulation(num_total_nodes, num_conflicts):
    """
    Simulates the YouTube DRM Network using Graph Coloring Heuristics 
    with Maximal Penalty Principle (Updated Algorithm 1).
    Returns the number of recolored nodes and execution time in milliseconds.
    """
    G = nx.Graph()

    # 1. Nodes Generation
    # 20% Original Nodes (Copyright Owners), 80% Derivative Nodes (Users/Uploaders)
    num_vo = int(num_total_nodes * 0.2)
    num_vd = num_total_nodes - num_vo

    vo_nodes = [f"O_{i}" for i in range(num_vo)]
    vd_nodes = [f"D_{i}" for i in range(num_vd)]

    # Assign policies to original owners (Whitelist, Revenue Share, Takedown)
    policies = ["Whitelist", "Revenue Share", "Takedown"]
    for u in vo_nodes:
        # Takedown (30%), Revenue Share (50%), Whitelist (20%)
        assigned_policy = random.choices(policies, weights=[0.2, 0.5, 0.3])[0]
        G.add_node(u, type='Original', policy=assigned_policy)

    # Assign initial color 'Green' to derivative videos (users' uploads)
    for v in vd_nodes:
        G.add_node(v, type='Derivative', color='Green')

    # 2. Create copyright infringement links (Fuzzy Conflict Edges)
    edges_added = 0
    while edges_added < num_conflicts:
        u = random.choice(vo_nodes)
        v = random.choice(vd_nodes)
        if not G.has_edge(u, v):
            weight = random.uniform(0.1, 1.0) # overlap weight (w)
            G.add_edge(u, v, weight=weight)
            edges_added += 1

    # =======================================================
    # ALGORITHM 1: Dynamic Chromatic Assignment (Updated)
    # =======================================================
    start_time = time.time()

    threshold = 0.3 # tau (Fuzzy Threshold)
    recolored_count = 0

    for v in vd_nodes:
        final_color = 'Green' # Default state is Green
        claimants = [] # Initialize Claimants
        
        # Step 1: Detect all overlaps and collect Claimants
        neighbors = list(G.neighbors(v))
        for u in neighbors:
            w = G[u][v]['weight']
            if w >= threshold: # Conflict Detected
                claimants.append(u)

        # If no conflicts, proceed to the next node
        if not claimants:
            continue

        # Step 2: Apply Maximal Penalty Principle
        for u in claimants:
            policy = G.nodes[u]['policy']

            if policy == "Takedown":
                final_color = 'Red' # Immediate Red
                break # Overrides all other policies (stop checking once Red is assigned)
            
            elif policy == "Revenue Share" and final_color != 'Red':
                final_color = 'Yellow' # Change to Yellow
                # (Fractional splitting logic can be added here mathematically)

        # Step 3: Update the node's color if it has changed
        if final_color != 'Green':
            G.nodes[v]['color'] = final_color
            recolored_count += 1

    end_time = time.time()
    # =======================================================

    execution_time_ms = (end_time - start_time) * 1000
    return recolored_count, execution_time_ms

# 3. Running Test Cases and formatting the output table
if __name__ == "__main__":
    test_cases = [
        ("Small Network", 1000, 150),
        ("Shorts Mashup", 10000, 2400),
        ("Live Broadcast", 50000, 8500),
        ("Global Scale", 100000, 15000)
    ]

    print(f"{'Test Case':<18} | {'Nodes (|V|)':<11} | {'Conflicts (|E|)':<15} | {'Recolored':<10} | {'Time (ms)':<10}")
    print("-" * 75)
    for name, nodes, conflicts in test_cases:
        recolored, exec_time = run_drm_simulation(nodes, conflicts)
        print(f"{name:<18} | {nodes:<11} | {conflicts:<15} | {recolored:<10} | {exec_time:.2f} ms")
