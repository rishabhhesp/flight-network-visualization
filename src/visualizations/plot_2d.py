import networkx as nx
import plotly.graph_objects as go
import plotly.io as pio

def plot_2d_network(G, pagerank, top_n=5):
    pio.renderers.default = "browser"

    # Get top airports
    top_airports = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_nodes = [node for node, _ in top_airports]
    pos = {node: G.nodes[node]['pos'] for node in top_nodes if 'pos' in G.nodes[node]}

    # Color scheme for nodes
    colors = ['#FF00FF', '#00FFFF', '#FFD700', '#FF4500', '#00FF00']
    node_colors = [colors[i % len(colors)] for i in range(len(top_nodes))]

    # Node trace for airports
    node_trace = go.Scattergeo(
        lon=[pos[node][0] for node in top_nodes],
        lat=[pos[node][1] for node in top_nodes],
        text=top_nodes,
        mode='markers+text',
        marker=dict(size=16, color=node_colors, line=dict(width=2, color='black')),
        textposition="top center"
    )

    # Edge trace (only between top airports)
    edge_traces = []
    for src, dst in G.edges():
        if src in top_nodes and dst in top_nodes:
            edge_traces.append(
                go.Scattergeo(
                    lon=[pos[src][0], pos[dst][0]],
                    lat=[pos[src][1], pos[dst][1]],
                    mode='lines',
                    line=dict(width=2, color='#8A2BE2'),
                    opacity=0.5,
                    hoverinfo='none'
                )
            )

    fig = go.Figure(data=[node_trace] + edge_traces)
    fig.update_layout(
        title="Top 5 Airports on Country Map",
        showlegend=False,
        geo=dict(
            scope='world', 
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(230, 230, 230)',
            showcountries=True,
            countrycolor='rgb(200, 200, 200)',
            showlakes=True,
            lakecolor='rgb(180, 220, 250)',
            showocean=True,
            oceancolor='rgb(180, 220, 250)',
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        font=dict(color='#222222')
    )
    fig.show()