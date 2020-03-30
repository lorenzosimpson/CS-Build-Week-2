import axios from 'axios';

class Graph {
    constructor(vertices) {
        this.vertices = vertices
    }
    add_vertex(this, vertex_id){
        this.vertices[vertex_id] = set ()
    }

    add_edge(this, v1, v2){
        if (v1 in this.vertices && v2 in this.vertices) {
            this.vertices[v1].add(v2)
        }
        else {
            throw new Error('vertex does not exist')
        }
    }

    get_neighbors(this, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in this.vertices:
            return this.vertices[vertex_id]
        else:
            raise ValueError('vertex does not exist')
}