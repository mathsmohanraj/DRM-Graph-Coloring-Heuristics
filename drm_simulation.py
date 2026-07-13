import networkx as nx
import time
import random

def run_drm_simulation(num_total_nodes, num_conflicts):
    """
    Simulates the YouTube DRM Network using Graph Coloring Heuristics.
    Returns the number of recolored nodes and execution time in milliseconds.
    """
    G = nx.Graph()
    
    # 1. Nodes Generation
    # 20% Original Nodes (Rights Holders), 80% Derivative Nodes (Users)
    num_vo = int(num_total_nodes * 0.2)
    num_vd = num_total_nodes - num_vo
    
    vo_nodes = [f"O_{i}" for i in range(num_vo)]
    vd_nodes = [f"D_{i}" for i in range(num_vd)]
    
    # Assign policies to original rights holders (Whitelist, Revenue Share, Takedown)
    policies = ["Whitelist", "Revenue Share", "Takedown"]
    for u in vo_nodes:
        # Takedown (30%), Revenue Share (50%), Whitelist (20%)
        assigned_policy = random.choices(policies, weights=[0.2, 0.5, 0.3])[0]
        G.add_node(u, type='Original', policy=assigned_policy)
        
    # Assign default 'Green' color to user derivative nodes
    for v in vd_nodes:
        G.add_node(v, type='Derivative', color='Green')
        
    # 2. Generate fuzzy conflict edges representing copyright overlaps
    edges_added = 0
    while edges_added < num_conflicts:
        u = random.choice(vo_nodes)
        v = random.choice(vd_nodes)
        if not G.has_edge(u, v):
            weight = random.uniform(0.1, 1.0) # overlap weight (w)
            G.add_edge(u, v, weight=weight)
            edges_added += 1

    # =======================================================
    # ALGORITHM 1: Dynamic Chromatic Assignment
    # =======================================================
    start_time = time.time()
    
    threshold = 0.3 # tau (Fuzzy/Temporal Threshold)
    recolored_count = 0
    
    for v in vd_nodes:
        neighbors = list(G.neighbors(v))
        if not neighbors:
            continue # No conflict detected, remains Green.
            
        final_color = 'Green'
        for u in neighbors:
            w = G[u][v]['weight']
            if w >= threshold: # Conflict confirmed
                policy = G.nodes[u]['policy']
                
                if policy == "Whitelist":
                    continue # Licensed content, remains Green
                elif policy == "Revenue Share":
                    final_color = 'Yellow' # Revenue sharing
                elif policy == "Takedown":
                    final_color = 'Red' # Immediate takedown
                    break # Stop scanning further once a Red policy is hit (Heuristic optimization)
        
        # Update node color if changed
        if final_color != 'Green':
            G.nodes[v]['color'] = final_color
            recolored_count += 1
            
    end_time = time.time()
    # =======================================================
    
    execution_time_ms = (end_time - start_time) * 1000
    return recolored_count, execution_time_ms

# 3. Running Test Cases to generate performance table
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
