from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import networkx as nx
import os

# For Loading data 
airports_file = os.path.join("data", "airports.dat")
routes_file = os.path.join("data", "routes.dat")

airport_cols = ['AirportID', 'Name', 'City', 'Country', 'IATA', 'ICAO',
                'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST',
                'Tz', 'Type', 'Source']
route_cols = ['Airline', 'AirlineID', 'SourceAirport', 'SourceAirportID',
              'DestAirport', 'DestAirportID', 'Codeshare', 'Stops', 'Equipment']

airports = pd.read_csv(airports_file, names=airport_cols, index_col=False, header=None)
routes = pd.read_csv(routes_file, names=route_cols, index_col=False, header=None)

# Filtering out the invalid routes
routes = routes[routes['SourceAirport'].notnull() & routes['DestAirport'].notnull()]
routes = routes[routes['SourceAirport'] != routes['DestAirport']]

# Creating the graph
G = nx.DiGraph()

# Adding airports as a nodes
for _, row in airports.iterrows():
    G.add_node(row['IATA'], pos=(row['Longitude'], row['Latitude']))

# Adding routes as a edges
for _, row in routes.iterrows():
    src = row['SourceAirport']
    dst = row['DestAirport']
    if src in G.nodes and dst in G.nodes:
        G.add_edge(src, dst)

# Initializing Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Flight Network Dashboard"),
    dcc.Dropdown(
        id='airport-dropdown',
        options=[{'label': airport, 'value': airport} for airport in G.nodes],
        value='JFK',
        multi=True
    ),
    dcc.Graph(id='flight-network-graph')
])

@app.callback(
    Output('flight-network-graph', 'figure'),
    Input('airport-dropdown', 'value')
)
def update_graph(selected_airports):
    pos = nx.get_node_attributes(G, 'pos')
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    node_x = []
    node_y = []
    for airport in selected_airports:
        x, y = pos[airport]
        node_x.append(x)
        node_y.append(y)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(width=0.5, color='gray'), hoverinfo='none'))
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=selected_airports, textposition="top center",
                             marker=dict(size=10, color='skyblue', line=dict(width=2, color='DarkSlateGrey'))))

    fig.update_layout(title='Flight Network', showlegend=False, hovermode='closest')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)