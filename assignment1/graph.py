# Graph Implementation

import math
from queue import PriorityQueue

"""
Vertex class represents a vertex in a graph
"""
class Vertex:

    def __init__(self, id, coords):
        """
        Vertex class constructor to create new instances of Vertex class/object

        :param id           the integer id of the vertex
        :param coords       the 2D integer coordinates of the vertex
        :param cost         the cost to goal, typically euclidean
        :param edges        list of neighbor vertices with a connection/edge
        :param parent       parent vertex as part of a path
        :param parent       path to goal
        """
        self.id = id
        self.coords = coords
        self.cost = 0
        self.edges = []
        self.parent = None
        self.path = []

    def __eq__(self, coords):
        """
        Check equality of vertex based on coordinates, override default comparison

        :param coords       the 2D integer coordinates of a vertex to compare

        :return boolean     true if the coordinates are the same, false otherwise
        """
        return self.coords == coords

    def __lt__(self, vertex):
        """
        Check equality of vertex based on cost, override default comparison

        :param vertex       the vertex to compare costs

        :return boolean     true if the costs are the same, false otherwise
        """
        return (self.cost < vertex.cost)

    def __hash__(self):
        return hash((self.coords[0], self.coords[1]))


"""
Graph class represents a graph with vertices and edges
"""
class Graph:

    def __init__(self):
        """
        Graph class constructor to create new instances of Graph class/object
        """
        self.vertices = {}

    def add_edge(self, vertexA, vertexB):
        """
        Add an edge between two vertices

        :param vertexA        a vertex to add an edge
        :param vertexB        the other vertex to add an edge
        """
        vertexA.edges.append(vertexB)
        vertexB.edges.append(vertexA)

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph

        :param vertex     the vertex being added to the graph
        """
        self.vertices[vertex.id] = vertex

    def has_edge(self, vertexA, vertexB):
        """
        Check if an edge exists between two vertices

        :param vertexA        a vertex to compare
        :param vertexB        the other vertex to compare

        :return boolean     true if each vertex has an edge to the other vertex, false otherwise
        """
        return vertexA in vertexB.edges and vertexB in vertexA.edges

    def aStar(self, start, goal):
        """
        Obtain the path from start vertex to goal vertex using A* search algorithm

        :param start          the starting vertex
        :param goal           the goal vertex

        :return list    list of vertex ids representing path from start to goal
        """
        frontier = PriorityQueue()
        explored = set()
        start.path = [start.id] 
        frontier.put((0, start))
        while not frontier.empty():
            vertex = frontier.get()[1]
            if vertex.id == goal.id:
                return vertex.path
            if vertex.id not in explored:
                explored.add(vertex.id)
                for neighbor in vertex.edges:
                    neighbor.path = vertex.path + [neighbor.id]
                    cost = 0
                    nodes = len(neighbor.path) - 1
                    for i in range(nodes):
                        cost += math.dist(self.vertices[neighbor.path[i]].coords,
                                          self.vertices[neighbor.path[i+1]].coords)
                    priority = cost + math.dist(neighbor.coords, goal.coords)
                    if neighbor.id not in explored:
                        frontier.put((priority, neighbor))
        return None

    def dijkstra(self, start, goal):
        dist = {}
        for id,vertex in self.vertices.items():
            dist[vertex] = 1000000
            vertex.parent = None
        dist[start] = 0

        while not dist == False:
            vertex = min(dist, key=dist.get)
            if vertex == goal:
                break
            for neighbor in vertex.edges:
                alt = dist[vertex] + math.dist(vertex.coords, neighbor.coords)
                if dist.get(neighbor) != None and alt < dist[neighbor]:
                    dist[neighbor] = alt
                    neighbor.parent = vertex
            del dist[vertex]

        path_stack = []
        while vertex != start and vertex != None:
            path_stack.append(vertex.id)
            vertex = vertex.parent
        path_stack.append(start.id)
        path_stack.reverse()
        if not self.has_edge(start, self.vertices[path_stack[1]]):
            return None

        return path_stack

    def remove_edge(self, vertexA, vertexB):
        """
        Remove an edge between two vertices

        :param vertexA        a vertex to remove an edge
        :param vertexB        the other vertex to remove an edge
        """
        vertexA.edges.remove(vertexB)
        vertexB.edges.remove(vertexA)

    def remove_vertex(self, vertex):
        """
        Remove an vertex from the graph

        :param id           the ID of a vertex to remove
        """
        for id, v in self.vertices.items():
            if v != vertex and vertex in v.edges:
                self.remove_edge(v, vertex)

        # remove vertex from graph
        self.vertices.pop(vertex.id, None)

