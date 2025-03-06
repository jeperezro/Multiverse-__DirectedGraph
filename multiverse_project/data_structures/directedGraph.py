from multiverse_project.data_structures.dictionary import Dictionary
from multiverse_project.data_structures.dynamicArray import Dynamic_Array


class Directed_Graph:
    def __init__(self):
        """Initialize an empty adjacency list using My_Dict."""
        self.graph = Dictionary()

    def add_vertex(self, vertex):
        """Add a vertex to the graph if it doesn't already exist."""
        if vertex not in self.graph:
            self.graph[vertex] = Dynamic_Array()

    def add_edge(self, from_vertex, to_vertex):
        """Add a directed edge from one vertex to another."""
        if from_vertex not in self.graph:
            self.add_vertex(from_vertex)
        if to_vertex not in self.graph:
            self.add_vertex(to_vertex)
        self.graph[from_vertex].append(to_vertex)

    def remove_edge(self, from_vertex, to_vertex):
        """Remove a specific directed edge from the graph."""
        if from_vertex in self.graph:
            new_adj_list = Dynamic_Array()
            for neighbor in self.graph[from_vertex]:
                if neighbor != to_vertex:
                    new_adj_list.append(neighbor)
            self.graph[from_vertex] = new_adj_list  # Replace with filtered list

    def remove_vertex(self, vertex):
        if vertex in self.graph:
            del self.graph[vertex]  # Remove the vertex itself

            for v in self.graph:
                new_list = Dynamic_Array()  # Create an empty My_List instance
                for neighbor in self.graph[v]:
                    if neighbor != vertex:
                        new_list.append(neighbor)  # Add elements one by one

                self.graph[v] = new_list  # Assign the updated list back

    def has_edge(self, from_vertex, to_vertex):
        """Check if an edge exists between two vertices."""
        return from_vertex in self.graph and to_vertex in self.graph[from_vertex]

    def get_vertices(self):
        """Return a My_List of all vertices in the graph."""
        return self.graph.keys

    def get_edges(self):
        """Return a My_List of all directed edges in the graph."""
        edges = Dynamic_Array()
        for vertex in self.graph:
            for neighbor in self.graph[vertex]:
                edges.append((vertex, neighbor))
        return edges  # Now returns a My_List


    # def get_neighbors(self, vertex):
    #     """Returns a My_List of neighbors for a given vertex."""
    #     neighbors = Dynamic_Array()
    #     if vertex in self.graph:
    #         for i in range(len(self.graph[vertex])):
    #             neighbors.append(self.graph[vertex][i])
    #     return neighbors

    def display(self):
        """Display the adjacency list of the graph."""
        print("Graph Representation (Adjacency List):")
        for vertex in self.graph:
            print(f"{vertex} --> {(self.graph[vertex])}")  # Convert to list for better readability

    def display_vertex_connections(self, vertex):
        """Return a string with the adjacency list of one vertex in the graph"""
        str = f"{vertex} --> {self.graph[vertex]}"
        return str
