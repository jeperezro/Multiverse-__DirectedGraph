
from multiverse_project.data_structures.directedGraph import Directed_Graph
from multiverse_project.data_structures.dynamicArray import Dynamic_Array
from multiverse_project.multiverse.zn_verse import Zn_verse


class Multiverse:
    def __init__(self):
        self.graph = Directed_Graph()
        self.initialize_multiverse()

    def initialize_multiverse(self):
        sets = Dynamic_Array()  # Use My_List instead of a standard list
        for n in [2,3,4,6,8,9,12]:  
            sets.append(n)  # Add elements to My_List
        
        for i in range(len(sets)):  # Iterate through My_List using indexing
            n = sets[i]
            for a in range(n):  
                universe = Zn_verse(a, n)
                self.graph.add_vertex(universe)
                
                # 🔹 Fix: Establish connections immediately

        self._create_connections()

    
    def _create_connections(self):
        """Update all valid connections between universes, preventing duplicates."""
        vertices = self.graph.get_vertices()
        
        for universe1 in vertices:
            # Create a new list to track unique connections
            unique_connections = Dynamic_Array()
            
            for universe2 in vertices:
                if universe1 != universe2:
                    # Check if universe1 can transition into universe2
                    connection_condition = (
                        universe2.a % universe1.n == universe1.a % universe1.n and
                        universe2.n % universe1.n == 0
                    )
                    
                    # Additional check to prevent excessive connections
                    is_duplicate = False
                    for existing_connection in unique_connections:
                        if existing_connection == universe2:
                            is_duplicate = True
                            break
                    
                    if connection_condition and not is_duplicate and len(unique_connections) < 6:
                        unique_connections.append(universe2)
            
            # Clear existing edges and add only unique connections
            self.graph.graph[universe1] = unique_connections


    
    def add_universe(self, a, n):
        universe = Zn_verse(a, n)
        if universe not in self.graph.get_vertices():
            self.graph.add_vertex(universe)
            
    
    def remove_universe(self, a, n):
        universe = Zn_verse(a, n)
        if universe in self.graph.get_vertices():
            self.graph.remove_vertex(universe)

    def get_related_universes(self, universe):
        """Returns all universes related to the given universe."""
        related = self.graph.graph[universe]    
        return related
    
    def display_multiverse(self):
        self.graph.display()
