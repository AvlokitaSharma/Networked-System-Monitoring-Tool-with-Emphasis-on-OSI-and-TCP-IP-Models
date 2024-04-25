from scapy.all import sniff, IP, TCP, Ether, UDP
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from collections import deque

# Initialize data structures
max_length = 20  # maximum length of deque to store data
data = {
    "Timestamp": deque(maxlen=max_length),
    "Ethernet": deque(maxlen=max_length),
    "IP": deque(maxlen=max_length),
    "TCP": deque(maxlen=max_length),
    "UDP": deque(maxlen=max_length)
}

# Define the Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1*1000  # update every second
    ),
])

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    graph = go.Figure(
        data=[
            go.Scatter(
                x=list(data['Timestamp']),
                y=list(data['Ethernet']),
                name='Ethernet',
                mode='lines+markers'
            ),
            go.Scatter(
                x=list(data['Timestamp']),
                y=list(data['IP']),
                name='IP',
                mode='lines+markers'
            ),
            go.Scatter(
                x=list(data['Timestamp']),
                y=list(data['TCP']),
                name='TCP',
                mode='lines+markers'
            ),
            go.Scatter(
                x=list(data['Timestamp']),
                y=list(data['UDP']),
                name='UDP',
                mode='lines+markers'
            )
        ],
        layout=go.Layout(
            title='Network Packet Data Over Time',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Packet Count')
        )
    )
    return graph

def capture_packets():
    sniff(count=10, store=0, prn=process_packet)

def process_packet(packet):
    current_time = pd.datetime.now()
    data['Timestamp'].append(current_time)
    for layer, count in [('Ethernet', Ether), ('IP', IP), ('TCP', TCP), ('UDP', UDP)]:
        if packet.haslayer(count):
            data[layer].append(1)
        else:
            data[layer].append(0)

if __name__ == '__main__':
    from threading import Thread
    t = Thread(target=capture_packets)
    t.start()
    app.run_server(debug=True)
