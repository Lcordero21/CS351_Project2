from graph_impl import Graph, Vertex, Edge
from graph_interfaces import IGraph, IVertex, IEdge

class PriorityQueue():
    def __init__(self) -> None:
        """ Initialize the Priority Queue as an empty list that takes in vertices"""
        self._queue: list[Node] = []

    def add_node(self, node: IVertex, weight: float) -> None:
        """ Add a new node in order based on the weight"""
        if len(self._queue) > 0:
            for i in range (len(self._queue)-1):
                if self._queue[i].get_weight() <= weight:
                    self._queue.insert(i,Node(node,weight))
                    return None
        self._queue.append(Node(node, weight))

    def pop_node(self) -> IVertex:
        """Pop a node off the queue"""
        pop = self._queue[len(self._queue)-1].get_node()
        self._queue.pop()
        return pop
    
    def get_queue(self) -> list:
        """Get the queue list"""
        return self._queue
    
    def get_length(self) -> int:
        """Get the lenght of the queue"""
        return len(self._queue)
    
    def reset_all_weight(self)->None:
        """Resets all the node's weights to None"""
        for node in self._queue:
            node.set_weight(None)
    
class Node():
    def __init__(self, node:IVertex, weight:float) -> None:
        """Initializes the node with the node Vertex address and the weight of the node"""
        self._node: IVertex = node
        self._weight:float = weight
        self._f_weight = None

    def set_weight(self, new_weight:float) -> None:
        """Can be set as any weight (to be used for sorting purposes in queue)"""
        self._weight:float = new_weight

    def get_weight(self) -> float:
        """To retireve the set weight of the Node"""
        return self._weight
    
    def get_node(self) -> IVertex:
        """To get the actual IVertex node"""
        return self._node
