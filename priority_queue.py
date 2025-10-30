from graph_impl import Graph, Vertex, Edge
from graph_interfaces import IGraph, IVertex, IEdge

class PriorityQueue():
    def __init__(self) -> None:
        """ Initialize the Priority Queue as an empty list that takes in vertices"""
        self._queue: list[IVertex] = []

    def add_node(self, node: IVertex, weight: float) -> None:
        """ Add a new node in order based on the weight"""
        for i in range (len(self._queue)-1):
            if self._queue[i].get_h() <= weight:
                self._queue.insert(node)
                return None
            self._queue.append(node)

    def pop_node(self) -> IVertex:
        return self._queue.pop()
    
    def get_length(self) -> int:
        return len(self._queue)
