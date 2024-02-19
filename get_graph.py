import osmnx as ox
import networkx as nx
import os
from shapely import MultiPolygon, Polygon


def get_graph_xml(xml:str,simplify: bool =False,network_type: str = "drive") -> nx.MultiDiGraph:
    graph = ox.graph_from_xml(xml, simplify=simplify,bidirectional=False)
    for node_id, node_data in graph.nodes(data=True):
        if ("lat" not in node_data) or ("lon" not in node_data):
            node_data["lat"] = node_data["y"]
            node_data["lon"] = node_data["x"]
    return graph




def simplify(graph: nx.MultiDiGraph):
    new_graph: nx.MultiDiGraph = graph.copy()
    for n in graph.nodes(data=True):
        edges_out = list(new_graph.out_edges(n[0],data=True,keys=True))
        edges_in = list(new_graph.in_edges(n[0],data=True,keys=True))
        if(len(edges_in)==2 and len(edges_out)==2):
            if({edges_in[0][0],edges_in[1][0]} == {edges_out[0][1],edges_out[1][1]}):                    
                if(edges_in[0][0] == edges_in[1][0] or edges_out[0][1] == edges_out[1][1]):
                    continue
                if(edges_out[0][1] == edges_in[0][0]):
                    index = 1
                else:
                    index = 0
                way1 = (edges_in[0],edges_out[index])
                way2 = (edges_in[1],edges_out[abs(index-1)])
                if(way1[0][3]['lanes'] == way1[1][3]['lanes'] and way1[0][3]['maxspeed'] == way1[1][3]['maxspeed'] and way2[0][3]['lanes'] == way2[1][3]['lanes'] and way2[0][3]['maxspeed'] == way2[1][3]['maxspeed']):
                    data1 = way1[0][3]
                    data2 = way2[0][3]
                    data1['length'] = way1[0][3]['length'] + way1[1][3]['length']
                    data2['length'] = way2[0][3]['length'] + way2[1][3]['length']
                    new_graph.remove_node(n[0])
                    new_graph.add_edge(way1[0][0],way1[1][1])
                    k1 = new_graph.number_of_edges(way1[0][0],way1[1][1])
                    new_graph.add_edge(way2[0][0],way2[1][1])
                    k2 = new_graph.number_of_edges(way2[0][0],way2[1][1])
                    for key in data1.keys():
                        new_graph.edges[way1[0][0],way1[1][1],k1-1][key] = data1[key]
                    for key in data2.keys():
                        new_graph.edges[way2[0][0],way2[1][1],k2-1][key] = data2[key]
        else:
            if(len(edges_in)==1 and len(edges_out) == 1):
                if(edges_in[0][0] == edges_out[0][1]):
                    continue
                way = (edges_in[0],edges_out[0])
                if(way[0][3]['lanes'] == way[1][3]['lanes'] and way[0][3]['maxspeed'] == way[1][3]['maxspeed']):
                    data = way[0][3]
                    data['length'] = way[0][3]['length'] + way[1][3]['length']
                    new_graph.remove_node(n[0])
                    new_graph.add_edge(way[0][0],way[1][1])
                    k=new_graph.number_of_edges(way[0][0],way[1][1])
                    for key in data.keys():
                        new_graph.edges[way[0][0],way[1][1],k-1][key] = data[key]
    return new_graph









