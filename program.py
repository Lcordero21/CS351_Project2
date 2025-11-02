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
   lat1, lon1,lat2,lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
   """Will calculate the haversine distance in radians"""
   radius: int = 3959 # Earth's radius in miles
   lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
   delta_lat: float = lat2 - lat1
   delta_lon: float = lon2 - lon1
   # 'a' is the squared half-chord length between the points
   a: float = math.sin(delta_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon/2)**2
   # 'c' is the angular distance in radians (the central angle)
   c: float = 2 * math.asin(math.sqrt(a))
   return radius * c

def set_coords (file_path: str, graph: IGraph, destination: str) -> None: #FINISH
    """Will read in the file with all the city coordinates to later be used by the 
    haversine_distance function
    Complexity: O(n^2)...not the most efficient, sorry"""
    vertices = graph.get_vertices()
    dest_name, dest_lat, dest_lon = destination, None, None
    with open(file_path) as paths:
        for line in paths:
            name, latitude, longitude = line.split(",")
            if name != "vertex":
                for i in range (len(vertices)-1):
                    if vertices[i].get_name() == name:
                        vertices[i].set_coordinates(latitude, longitude)

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

    reset_visited (graph.get_vertices()) #Resets visited of all vertices

    #This is in a seperate python file I created for this 
    frontier = PriorityQueue() 

    #The coordinates that will be used to get the haversine distance
    start_coords = start_vertex.get_coordinates()
    dest_coords = destination.get_coordinates()

    frontier.add_node (start_vertex, haversine_distance(start_coords[0], start_coords[1],dest_coords[0], dest_coords[1])) 
    explored = []
    parent = {}

    parent[start_vertex] = None


    while frontier.get_length() != 0:
        current = frontier.pop_node()
        if current.get_name() == destination.get_name():
            print (reconstructPath(parent, current))
        explored.append(current)
        current.set_visited(True)
        for edge in current.get_edges():
            neighbour = edge.get_destination()
            if (neighbour.is_visited() == False) and (neighbour not in frontier.get_queue()):
                parent[neighbour] = current
                neighbour_coords = neighbour.get_coordinates()
                frontier.add_node(neighbour_coords[0],neighbour_coords[1],dest_coords[0], dest_coords[1]) 
    print("Path Not Found For Greedy Best First Search")

def print_dijkstra(graph: IGraph, start_vertex:IVertex, destination:IVertex):
    reset_visited (graph.get_vertices())

    frontier = PriorityQueue()
    frontier.add_node(start_vertex, 0)

    explored = []
    total_dist = 0
    parent = {}

    parent[start_vertex] = None

    while frontier.get_length() != 0:
        current = frontier.pop_node()
        if current.get_name() == destination.get_name():
            print (reconstructPath(parent, current))
        explored.append(current)
        current.set_visited(True)
        for edge in current.get_edges():
            tentative_g = current.get_weight() + total_dist
            neighbour = edge.get_destination()
            if neighbour.get_visited() == False:
                if (neighbour not in frontier.get_queue()) or (tentative_g < neighbour.get_weight()):
                    neighbour.set_weight(tentative_g)
                    parent[neighbour] = current
                    frontier.add_node(neighbour, tentative_g)
    print("Path Not Found for Dijkstra")


def print_astar(graph: IGraph, start_vertex: IVertex, destination: IVertex):
    reset_visited (graph.get_vertices())

    #To get f(start)
    start_coords = start_vertex.get_coordinates()
    dest_coords = destination.get_coordinates()
    g_score_start = 0
    f_score_start = g_score_start + haversine_distance (start_coords[0], start_coords[1], dest_coords[0], dest_coords[1])

    frontier = PriorityQueue()
    frontier.add_node(start_vertex, f_score_start)

    explored = []
    parent = {}

    parent[start_vertex] = None

    


    print("Path Not Found for A-Star")

##########################################################################################
def priority_queue(arr, func): #FIX THIS OR DELETE ____________________________________
    new_array = arr
    for i in range(len(new_array)):
        minimum =i
        for m in range (i+1,len(new_array)):
            if new_array[m] < new_array [minimum]:
                minimum = m
        new_array [i], new_array [minimum] = new_array [minimum], new_array [i]
    return new_array

def reconstructPath(parent_path: dict[IVertex,IVertex], end:IVertex) -> list[str]:
    current = end
    the_path = []
    while current != None:
        the_path.append(parent_path[current].get_name())
        current = parent_path[current]
    return the_path

def reset_visited(graph) -> None:
    """
    Purpose:
        Resets all the visited statuses of the each vertex in a graph.
    """
    for vertex in graph:
        vertex.set_visited(False)




def main() -> None:
    #Read the files
    graph: IGraph = read_graph("graph_v2.txt")

    # Get starting name
    for i in graph.get_vertices():
        print(i.get_name())
    start_vertex_name: str  = input("Enter the start vertex name: ")


    # Find the start vertex object
    start_vertex: Optional[IVertex]= next((v for v in graph.get_vertices() if v.get_name() == start_vertex_name), None)


    if start_vertex is None:
        print("Start vertex not found")
        return
   
   # Get the destination vertex name
    for i in graph.get_vertices():
        print(i.get_name())
    dest_vertex_name: str = input("Enter the destination vertex name:")

    # Get the destination vertex object
    dest_vertex:Optional[IVertex] = next((v for v in graph.get_vertices() if v.get_name() == dest_vertex_name), None)

    if dest_vertex is None: 
        print("Destination vertex not found")
        return
    
    set_coords("vertices_v1.txt", graph, dest_vertex_name) 
    
    print("[Greedy Best First Search Algorithm]")
    print_greedyBFS(graph, start_vertex, dest_vertex)

    """print("[Dijkstra Algorithm]")
    print_dijkstra(graph, start_vertex, dest_vertex)

    print("[A* Algorithm]")
    print_astar(graph, start_vertex, dest_vertex)

    print_bfs(graph, start_vertex)
    print_dfs(graph, start_vertex)"""





if __name__ == "__main__":
    main()

