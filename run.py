import get_graph
import capacity_functions
import road_load_functions
import fix_functions

import argparse

import networkx as nx


parser = argparse.ArgumentParser(description="Скрипт принимает на вход путь к osm файлу")
parser.add_argument("file_path", help="Путь к файлу")
parser.add_argument("dir_path", help="Путь к исполняемой папке")
args = parser.parse_args()
file_path = args.file_path
dir_path = args.dir_path
graph = get_graph.get_graph_xml(file_path)
fix_functions.fix_lanes_and_maxspeed(graph)
new_graph= get_graph.simplify(graph)
new_graph = capacity_functions.assign_capacity()
new_graph = road_load_functions.assign_random_road_load()
nx.write_graphml(graph,f'{dir_path}/graph.graphml')
nx.write_graphml(new_graph,f'{dir_path}/graph_simplified.graphml')


