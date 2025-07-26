import pandas as pd
import networkx as nx
import os
from visualizations.plot_2d import plot_2d_network
from analysis.centrality import calculate_centrality
from analysis.clustering import calculate_clustering
from utils.data_loader import load_data

# Load the Data into DataFrames
airport_files = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'airports.dat'))
route_files = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'routes.dat'))
airports, routes = load_data(airport_files, route_files)

# Creating Graph 
G = nx.DiGraph()

# Adding airports as nodes
for _, row in airports.iterrows():
    G.add_node(row['IATA'], name=row['Name'], city=row['City'],
               country=row['Country'], pos=(row['Longitude'], row['Latitude']))

# Adding routes as edges
for _, row in routes.iterrows():
    src = row['SourceAirport']
    dst = row['DestAirport']
    if src in G.nodes and dst in G.nodes:
        G.add_edge(src, dst)

print(f"Total Airports (Nodes): {G.number_of_nodes()}")
print(f"Total Routes (Edges): {G.number_of_edges()}")

# Analysis for the Flight Network
degree_centrality, pagerank = calculate_centrality(G)
clustering_coeff = calculate_clustering(G)

print("\nTop 5 Airports by PageRank:")
top_5_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:5]
for iata, score in top_5_pagerank:
    name = G.nodes[iata]['name']
    print(f"{iata}: {name} ({score:.4f})")

# Print Top 5 Airports by Clustering Coefficient 
print("\nTop 5 Airports by Clustering Coefficient:")
node_clustering = clustering_coeff["node_clustering"]
top_5_clustering = sorted(node_clustering.items(), key=lambda x: x[1], reverse=True)[:5]
for iata, coeff in top_5_clustering:
    name = G.nodes[iata]['name']
    print(f"{iata}: {name} ({coeff:.4f})")

# Visualizations the top airports on a map
plot_2d_network(G, pagerank, top_n=20)




