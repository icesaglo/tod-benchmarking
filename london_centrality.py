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

    # The formula assumes finite distances between all nodes.
    # If the network has disconnected segments, use the largest connected component.
    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()

    n = G.number_of_nodes()
    if n <= 1:
        return 0.0

    closeness_values = []
    for u in G.nodes():
        # Calculate topological hops to all other nodes
        distances = nx.single_source_shortest_path_length(G, u)
        distance_sum = sum(distances.values())
        
        if distance_sum == 0:
            closeness_values.append(0.0)
            continue
            
        c_u = (n - 1) / distance_sum
        closeness_values.append(c_u)

    # Return the normalised average across all stations
    return sum(closeness_values) / n


def calculate_london_closeness(stations_csv_path, links_csv_path):
    print("==================================================")
    print("Analysing Closeness Centrality for London Underground")
    
    # 1. Load the structural data
    stations_df = pd.read_csv(stations_csv_path)
    links_df = pd.read_csv(links_csv_path)

    # 2. Build the Graph Model
    G = nx.Graph()

    # Add nodes (using 'id' as the key and 'name' as a label)
    for idx, row in stations_df.iterrows():
        G.add_node(row['id'], name=row['name'])

    # Add edges representing topological connections
    for idx, row in links_df.iterrows():
        G.add_edge(row['station1'], row['station2'])

    # Remove any isolated stops not connected to the main network
    G.remove_nodes_from(list(nx.isolates(G)))

    # 3. Calculate City-Wide Average via the thesis formula
    avg_close = average_closeness_from_formula(G)

    print(f"Total Active Stations Analysed: {len(G.nodes)}")
    print(f"Average Closeness Centrality (C_c): {avg_close:.4f}\n")
    
    # 4. Identify the Top 5 most central stations for context
    # We use the built-in networkx function here just to rank them quickly
    closeness_dict = nx.closeness_centrality(G)
    top_5 = sorted(closeness_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    
    print("Top 5 Most Central Stations (Node Value):")
    for station_id, score in top_5:
        name = G.nodes[station_id]['name']
        print(f"  {name}: {score:.4f}")
        
    return avg_close


if __name__ == "__main__":
    calculate_london_closeness('london_station_nodes.csv', 'london_network_links.csv')