import networkx as nx

G=nx.path_graph(5)

print(nx.dijkstra_path(G,0,4))