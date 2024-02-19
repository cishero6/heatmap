import networkx as nx
from shapely import MultiPolygon, Polygon

def get_beta_coefficient():
    return 1

def get_P_max(lanes: int) -> int:
    if (lanes == '2'):
        return 3600
    if (lanes == '3'):
        return 4000
    if (lanes == '4'):
        return 4*2150
    if (lanes == '5'):
        return 5*2250
    if (lanes == '6'):
        return 2300*6
    return int(lanes)*1900
    


def assign_capacity(graph:nx.MultiDiGraph):
    for edge in graph.edges(data=True):
        value = 0
        if('lanes' in edge[2]):
            value = edge[2]['lanes']
        else:
            value = 1
        edge[2]['capacity'] = get_beta_coefficient() * get_P_max(value)

