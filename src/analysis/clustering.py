import networkx as nx

def calculate_clustering(G):
    
    clustering_coeff = nx.clustering(G.to_undirected())
    avg_clustering = nx.average_clustering(G.to_undirected())
    return {"node_clustering": clustering_coeff, "average_clustering": avg_clustering}