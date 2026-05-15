import pandas as pd
import networkx as nx


def average_closeness_from_formula(G: nx.Graph) -> float:
    """
    Compute average closeness centrality exactly as:
      C_c(u) = (n - 1) / sum_{v!=u} d(v, u)
      C̄_c   = (1 / n) * sum_u C_c(u)
    using unweighted topological hop distances.
    """
    if G.number_of_nodes() == 0:
        return 0.0

    # Formula assumes finite distances between all nodes.
    # If disconnected, use the largest connected component as the analysis network.
    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()

    n = G.number_of_nodes()
    if n <= 1:
        return 0.0

    closeness_values = []
    for u in G.nodes():
        distances = nx.single_source_shortest_path_length(G, u)
        distance_sum = sum(distances.values())  # includes d(u,u)=0
        if distance_sum == 0:
            closeness_values.append(0.0)
            continue
        c_u = (n - 1) / distance_sum
        closeness_values.append(c_u)

    return sum(closeness_values) / n


def calculate_hk_closeness(csv_path):
    print("Analysing Closeness Centrality for Hong Kong")
    
    # 1. Load the clean MTR CSV
    df = pd.read_csv(csv_path)

    # Optional safety check: if GTFS-style route_type exists, explicitly exclude 0 (LRT/tram).
    if 'route_type' in df.columns:
        df['route_type'] = pd.to_numeric(df['route_type'], errors='coerce')
        df = df[df['route_type'].isin([1, 2])].copy()
        if (df['route_type'] == 0).any():
            raise ValueError("route_type 0 (LRT/tram) was found in the filtered HK dataset.")
    
    # 2. Sort to ensure sequence logic works
    df = df.sort_values(by=['Line Code', 'Direction', 'Sequence'])
    
    # 3. Create edges based on station sequences
    # Pair each station with the next station strictly within the same line+direction group.
    df['Next Station ID'] = df.groupby(['Line Code', 'Direction'])['Station ID'].shift(-1)
    edges_df = df.dropna(subset=['Next Station ID'])
    unique_edges = edges_df[['Station ID', 'Next Station ID']].drop_duplicates()
    
    # 4. Build the Graph Model
    G = nx.Graph()
    
    # Add nodes (using Station ID ensures interchanges are linked if they share IDs)
    for idx, row in unique_edges.iterrows():
        G.add_edge(row['Station ID'], row['Next Station ID'])
        
    # 5. Calculate City-Wide Average via your exact formula
    avg_closeness = average_closeness_from_formula(G)
    
    print("SUCCESS!")
    print(f"Total Active MTR Stations: {len(G.nodes)}")
    print(f"Average Closeness Centrality: {avg_closeness:.4f}\n")
    
    return avg_closeness

calculate_hk_closeness("hk_mtr_lines_and_stations.csv")