from typing import Optional
from graph_interfaces import IGraph, IVertex
from graph_impl import Graph, Vertex, Edge
from priority_queue import PriorityQueue
import copy
import math


def read_graph(file_path: str) -> IGraph:  
    """Read the graph from the file and return the graph object"""
    temp_graph = Graph()
    with open(file_path) as paths:
        for line in paths:
            origin, destination, highway, distance = line.split(",")
            if origin != "source":
                temp_graph.add_vertex(origin)
                temp_graph.add_vertex(destination)
                temp_graph.add_edge(highway, origin, destination, distance)
    return temp_graph

def read_vertices_coord(graph: IGraph, file_path: str):
    """Read the vertices from the file and add the coordinate information to the objects"""
    raise NotImplementedError

def haversine_distance(lat1, lon1, lat2, lon2) -> float:
   radius: int = 3959 # Earth's radius in miles
   lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
   delta_lat: float = lat2 - lat1
   delta_lon: float = lon2 - lon1
   # 'a' is the squared half-chord length between the points
   a: float = math.sin(delta_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon/2)**2
   # 'c' is the angular distance in radians (the central angle)
   c: float = 2 * math.asin(math.sqrt(a))
   return radius * c


def print_dfs(graph: IGraph, start_vertex: IVertex) -> None:
    """
        Print the DFS traversal of the graph starting from the start vertex (I used the iterative
        approach)
    """


    reset_visited(graph.get_vertices())
   
    stack = []
    visited = []
    visited_adj_list = Graph()


    stack.append(start_vertex)


    while len(stack) != 0:
        vertex = stack.pop()
        if vertex.is_visited() is False:
            visited_adj_list.add_vertex(vertex)
            visited.append(vertex.get_name())
            vertex.set_visited(True)
            for edge in vertex.get_edges():
                stack.append(edge.get_destination())


    print(visited)

def print_bfs(graph: IGraph, start_vertex: IVertex) -> None:
    """
        Print the BFS traversal of the graph starting from the start vertex (I used the
        iterative approach)
    """
    reset_visited (graph.get_vertices())


    queue = []
    visited = []
    visited_adj_list = Graph()


    queue.append(start_vertex)
    visited.append (start_vertex.get_name())
    visited_adj_list.add_vertex(start_vertex)
    start_vertex.set_visited(True)

    while len(queue) != 0:
        vertex = queue.pop(0)
        for edge in vertex.get_edges():
            dest = edge.get_destination()
            if dest.is_visited() is False:
                queue.append(dest)
                visited_adj_list.add_vertex(dest)
                visited.append(dest.get_name())
                dest.set_visited(True)


    print(visited)

def print_greedyBFS(graph: IGraph, start_vertex:IVertex, destination:IVertex):
    reset_visited (graph.get_vertices())
    frontier = PriorityQueue() #swap to priority queue (a class ina new file)
    frontier.add_node (start_vertex, start_vertex.get_h()) #fix
    explored = []
    explored_adj_list = Graph()


    while frontier.get_length() != 0:
        current = frontier.pop_node()
        if current.get_name() == destination.get_name():
            return explored
        explored.append(current.get_name)
        explored_adj_list.add_vertex(current)

    raise NotImplementedError

def print_dijkstra(graph: IGraph, start_vertex:IVertex, destination:IVertex):
    reset_visited (graph.get_vertices())
    raise NotImplementedError


def print_astar(graph: IGraph, start_vertex: IVertex, destination: IVertex):
    reset_visited (graph.get_vertices())
    raise NotImplementedError

def priority_queue(arr, func): #FIX THIS
    new_array = arr
    for i in range(len(new_array)):
        minimum =i
        for m in range (i+1,len(new_array)):
            if new_array[m] < new_array [minimum]:
                minimum = m
        new_array [i], new_array [minimum] = new_array [minimum], new_array [i]
    return new_array

def reset_visited(graph) -> None:
    """
    Purpose:
        Resets all the visited statuses of the each vertex in a graph.
    """
    for vertex in graph:
        vertex.set_visited(False)




def main() -> None:
    graph: IGraph = read_graph("graph.txt")
    for i in graph.get_vertices():
        print(i.get_name())
    start_vertex_name: str  = input("Enter the start vertex name: ")


    # Find the start vertex object
    start_vertex: Optional[IVertex]= next((v for v in graph.get_vertices() if v.get_name() == start_vertex_name), None)


    if start_vertex is None:
        print("Start vertex not found")
        return
   
    print_bfs(graph, start_vertex)
    print_dfs(graph, start_vertex)




if __name__ == "__main__":
    main()

