import networkx as nx

def calculate_degree_centrality(G):
    return nx.degree_centrality(G)

def calculate_pagerank(G):
    return nx.pagerank(G)

def calculate_centrality(G):
   
    degree_centrality = calculate_degree_centrality(G)
    pagerank = calculate_pagerank(G)
    
    return degree_centrality, pagerank