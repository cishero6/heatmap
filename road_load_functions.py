import networkx as nx
import random
import numpy as np
import json


def assign_random_road_load(graph: nx.MultiDiGraph):
    for edge in graph.edges(data=True):
        edge[2]['road_load'] = json.dumps(list(np.round(np.random.rand(24)*2000+edge[2]['capacity']-1000)))