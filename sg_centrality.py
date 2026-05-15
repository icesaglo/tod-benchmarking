import pandas as pd
import networkx as nx
import zipfile


def average_closeness_from_formula(G: nx.Graph) -> float:
    """
    Compute average closeness centrality exactly as:
      C_c(u) = (n - 1) / sum_{v!=u} d(v, u)
      C̄_c   = (1 / n) * sum_u C_c(u)
    using unweighted topological hop distances.
    """
    if G.number_of_nodes() == 0:
        return 0.0

    # Formula requires finite d(v, u) to all nodes.
    # If disconnected, use the largest connected component as the network.
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


def calculate_mrt_closeness(gtfs_zip_path, city_name):
    print(f"========================================")
    print(f"Analysing Closeness Centrality for {city_name}")

    with zipfile.ZipFile(gtfs_zip_path, 'r') as z:
        stops = pd.read_csv(z.open('stops.txt'))
        routes = pd.read_csv(z.open('routes.txt'))
        trips = pd.read_csv(z.open('trips.txt'))
        stop_times = pd.read_csv(z.open('stop_times.txt'))
        
    # Filter for MRT/Train only (GTFS route_type 1=subway/metro, 2=rail).
    routes['route_type'] = pd.to_numeric(routes['route_type'], errors='coerce')
    mrt_route_types = [1, 2]
    mrt_routes_df = routes[routes['route_type'].isin(mrt_route_types)].copy()
    if (mrt_routes_df['route_type'] == 0).any():
        raise ValueError("route_type 0 (LRT/tram) was found in MRT-filtered routes.")
    mrt_routes = mrt_routes_df['route_id']
    mrt_trips = trips[trips['route_id'].isin(mrt_routes)]['trip_id']
    mrt_stop_times = stop_times[stop_times['trip_id'].isin(mrt_trips)]
    
    # Build connections
    mrt_stop_times = mrt_stop_times.sort_values(by=['trip_id', 'stop_sequence'])
    # Pair each stop with the next stop within the same trip
    mrt_stop_times['next_stop_id'] = mrt_stop_times.groupby('trip_id')['stop_id'].shift(-1)
    edges_df = mrt_stop_times.dropna(subset=['next_stop_id'])
    unique_edges = edges_df[['stop_id', 'next_stop_id']].drop_duplicates()
    
    # 6. Build the Graph Model (Merging platforms by name)
    G = nx.Graph()
    
    # Create a mapping dictionary: stop_id -> stop_name
    id_to_name = pd.Series(stops.stop_name.values, index=stops.stop_id).to_dict()
    
    # Add the tracks as edges, but use the Names instead of IDs
    for idx, row in unique_edges.iterrows():
        u_name = id_to_name.get(row['stop_id'])
        v_name = id_to_name.get(row['next_stop_id'])
        if u_name and v_name:
            G.add_edge(u_name, v_name)
            
    # Remove any lone stations that aren't connected
    G.remove_nodes_from(list(nx.isolates(G)))

    #G = nx.Graph()
    #for idx, row in unique_edges.iterrows():
    #    G.add_edge(row['stop_id'], row['next_stop_id'])
        
    # Calculate average closeness centrality with your exact formula
    avg_closeness = average_closeness_from_formula(G)
    
    print(f"Total Stations (graph): {len(G.nodes)}")
    print(f"Average Closeness Centrality: {avg_closeness:.4f}\n")
    
    return avg_closeness

calculate_mrt_closeness("singapore-gtfs.zip", "Singapore")