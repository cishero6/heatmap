import networkx as nx

def fix_lanes_and_maxspeed(graph: nx.MultiDiGraph):
    for edge in graph.edges(data=True):
        if('lanes' not in edge[2]):
            edge[2]['lanes'] = '1'
        if('maxspeed' not in edge[2]):
            edge[2]['maxspeed'] = 'RU:urban'