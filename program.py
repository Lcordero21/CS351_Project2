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


def print_greedyBFS(graph: IGraph, start_vertex:IVertex, destination:IVertex):
    """Uses the heuristic value to determine the best path to the goal"""
    reset_visited (graph.get_vertices()) #Resets visited of all vertices
    vertices_explored=0
    edges_explored=0
    total_distance=

    #This is in a seperate python file I created for this 
    frontier = PriorityQueue() 

    #The coordinates that will be used to get the haversine distance
    start_coords = start_vertex.get_coordinates()
    dest_coords = destination.get_coordinates()

    start_vertex.set_h(haversine_distance(start_coords[0], start_coords[1],dest_coords[0], dest_coords[1]))
    frontier.add_node(start_vertex, start_vertex.get_h()) 

    #Keeps track of parents
    parent = {}

    parent[start_vertex] = None

    while frontier.get_length() != 0:
        current = frontier.pop_node()
        total_distance += float(current.get_h())
        if current.get_name() == destination.get_name():
            return(reconstructPath(parent, current),edges_explored, vertices_explored, total_distance)
        current.set_visited(True)
        for edge in current.get_edges():
            neighbour = edge.get_destination()
            edges_explored += 1
            if (neighbour.is_visited() == False) and (neighbour not in frontier.get_queue()):
                vertices_explored += 1
                parent[neighbour] = current
                neighbour_coords = neighbour.get_coordinates()
                neighbour.set_h(haversine_distance(neighbour_coords[0],neighbour_coords[1],dest_coords[0], dest_coords[1]))
                frontier.add_node(neighbour,neighbour.get_h()) 
    print("Path Not Found For Greedy Best First Search")

def print_dijkstra(graph: IGraph, start_vertex:IVertex, destination:IVertex):
    """Uses the actual distance to determine the best possible path"""
    reset_visited (graph.get_vertices())
    edges_explored = 0
    vertices_explored= 0
    total_distance = 0

    frontier = PriorityQueue()
    frontier.add_node(start_vertex, 0)

    start_vertex.set_g(0)
    parent = {}

    parent[start_vertex] = None

    while frontier.get_length() != 0:
        current = frontier.pop_node()
        total_distance += float(current.get_g())
        if current.get_name() == destination.get_name():
            return (reconstructPath(parent, current),edges_explored, vertices_explored, total_distance)
        current.set_visited(True)
        for edge in current.get_edges():
            tentative_g = float(edge.get_weight()) + current.get_g()
            neighbour = edge.get_destination()
            edges_explored += 1
            if neighbour.is_visited() == False:
                if (neighbour not in frontier.get_queue()) or (tentative_g < neighbour.get_g()):
                    vertices_explored += 1
                    parent[neighbour] = current
                    frontier.add_node(neighbour, tentative_g)
                    neighbour.set_g(tentative_g)
    print("Path Not Found for Dijkstra")


def print_astar(graph: IGraph, start_vertex: IVertex, destination: IVertex):
    """Uses the sum of the heuristic value and actual distance value to determine best possible path"""
    reset_visited (graph.get_vertices())
    edges_explored = 0
    vertices_explored = 0
    total_distance = 0

    # To get f(start)
    start_coords = start_vertex.get_coordinates()
    dest_coords = destination.get_coordinates()

    #Setting the start_vertex up
    start_vertex.set_g (0)
    start_vertex.set_h(haversine_distance (start_coords[0], start_coords[1], dest_coords[0], dest_coords[1]))
    start_vertex.set_f(start_vertex.get_g() + start_vertex.get_h())

    # Set Up The Priority Queue
    frontier = PriorityQueue()
    frontier.add_node(start_vertex, float(start_vertex.get_f()))

    #Parent node stuff
    parent = {}

    parent[start_vertex] = None 

    while frontier.get_length() != 0:
        current = frontier.pop_node()
        total_distance += float(current.get_f())
        if current.get_name() == destination.get_name():
            return (reconstructPath(parent, current),edges_explored, vertices_explored, total_distance)
        current.set_visited(True)
        for edge in current.get_edges():
            edges_explored += 1
            tentative_g = current.get_g() + float(edge.get_weight())
            neighbour = edge.get_destination()
            if neighbour.is_visited() == False:
                vertices_explored += 1
                if (neighbour not in frontier.get_queue()) or (tentative_g < neighbour.get_g()):
                    #(There's a lot going on, so I'm going to add comments here):

                    # Set the g-value
                    neighbour.set_g(tentative_g)

                    # Set the h-value
                    neighbour_coords = neighbour.get_coordinates()
                    neighbour.set_h(haversine_distance(neighbour_coords[0],neighbour_coords[1],dest_coords[0], dest_coords[1]))

                    # Set the f-value
                    neighbour.set_f(neighbour.get_g()+neighbour.get_h())

                    #Set the parent and add it to the frontier
                    parent[neighbour] = current
                    frontier.add_node(neighbour, float(neighbour.get_f()))

    print("Path Not Found for A-Star")


def reconstructPath(parent_path: dict[IVertex,IVertex], end:IVertex) -> list[str]:
    """
    Purpose:
        To reconstruct the path taken to get to the result.
    """
    current = end
    the_path = []
    the_path.append(end.get_name())
    while parent_path[current] != None:
        the_path.insert(0,parent_path[current].get_name())
        current = parent_path[current]
    
    return the_path

def reset_visited(graph) -> None:
    """
    Purpose:
        Resets all the visited statuses, the g-value, and h-value of the each vertex in a graph.
    """
    for vertex in graph:
        vertex.set_visited(False)
        vertex.set_g(None)
        vertex.set_h(None)




def main() -> None:
    status = True
    while status:
        #Read the files
        graph: IGraph = read_graph("graph_v2.txt")

        print("Select Pathfinding Algorithm \n 1.Greedy Best First Search\n 2.Dijkstra's Algorithm\n 3.A* Algorithm")
        choice = input("Your Choice (1-3):")

        if choice not in range (1,4):
            print("Not a valid option")
            return

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

        #There's lots of print statements because I tried to make it look nice...
        if choice == 1:
            print("-"*25)
            print("[Greedy Best First Search Algorithm]")
            print("Path taken:", print_greedyBFS(graph, start_vertex, dest_vertex))
            print("-"*25)
        if choice == 2:
            print("[Dijkstra Algorithm]")
            print("Path taken:", print_dijkstra(graph, start_vertex, dest_vertex))
            print("-"*25)
        if choice == 3:
            print("[A* Algorithm]")
            print("Path taken:", print_astar(graph, start_vertex, dest_vertex))
            print("-"*25)

        

        """print_bfs(graph, start_vertex)
        print_dfs(graph, start_vertex)"""





if __name__ == "__main__":
    main()

