from util import Stack, Queue

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {
            # 0: {
            #     "room_id": 0,
            #     "title": "A Dark Room",
            #     "description": "You cannot see anything.",
            #     "coordinates": "(60,60)",
            #     "exits": ["n", "s", "e", "w"],
            #     "cooldown": 1.0,
            #     "errors": [],
            #     "messages": []
            #     }
            }

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set ()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise ValueError('vertex does not exist')

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            raise ValueError('vertex does not exist')

    def bft(self, starting_vertex):
            """
            Print each vertex in breadth-first order
            beginning from starting_vertex.
            """
            # Create a queue
            q = Queue()
            # Enqueue the starting vertex
            q.enqueue(starting_vertex)
            # Create a set to store visited vertices
            visited = set()
            # While the queue is not empty...
            while q.size() > 0:
                # Dequeue the first vertex
                v = q.dequeue()
                # Check if it's been visited
                # If it hasn't been visited...
                if v not in visited:
                    # Mark it as visited
                    print(v)
                    visited.add(v)
                    # Enqueue all it's neighbors
                    for neighbor in self.get_neighbors(v):
                        q.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # create a stack 
        s = Stack()
        # push the starting vertex
        s.push(starting_vertex)
        # create set to store visited 
        visited = set()
        # while stack is not empty:
        while s.size() > 0:
            # pop first vertex
            v = s.pop()
            # check if visiteed
            if not v in visited:
                print(v)
                #if not,
                # mark as visited
                visited.add(v)
                    # push all of its neighbors
                for neighbor in self.get_neighbors(v):
                    s.push(neighbor)
        # loop

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # create a queue
        q = Queue()
        # enqueue A PATH to the starting vertex
        q.enqueue([starting_vertex])
        # create set to store visited vertices
        v = set()
        # while queue is not empty,
        while q.size() > 0:
            # dequeue the first PATH
            path = q.dequeue()
            # grab vertex from the end of the path
            last_vertex = path[-1]
            # check if it's been visited, if not
            if not last_vertex in v:
                # mark it as visited
                v.add(last_vertex)
                # check if it's the target
                if last_vertex == destination_vertex:
                    return path
                    # if so, return the path
                    # enequeue a path to all its neighbors
                    # make a copy of the path
                    # enqeue the copy
                for n in self.get_neighbors(last_vertex): 
                    copy = path.copy()            
                    if not n in copy:
                        copy.append(n)
                    q.enqueue(copy)
                

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        # enqueue A PATH to the starting vertex
        s.push([starting_vertex])
        # create set to store visited vertices
        v = set()
        # while queue is not empty,
        while s.size() > 0:
            # dequeue the first PATH
            path = s.pop()
            # grab vertex from the end of the path
            last_vertex = path[-1]
            # check if it's been visited, if not
            if not last_vertex in v:
                # mark it as visited
                v.add(last_vertex)
                # check if it's the target
                if last_vertex == destination_vertex:
                    return path
                    # if so, return the path
                    # enequeue a path to all its neighbors
                    # make a copy of the path
                    # enqeue the copy
                for n in self.get_neighbors(last_vertex): 
                    copy = path.copy()            
                    if not n in copy:
                        copy.append(n)
                    s.push(copy)

    def dfs_recursive(self, starting_vertex, destination_vertex, path=None, visited=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if visited is None:
            visited = set()

        if path is None:
            path = []
        
        visited.add(starting_vertex)
        path = path + [starting_vertex]
        if starting_vertex == destination_vertex:
            return path
        
        for n in self.get_neighbors(starting_vertex):
            if n not in visited:
                x = self.dfs_recursive(n, destination_vertex, path, visited)
                if x:
                    return x
        

room_graph = Graph()