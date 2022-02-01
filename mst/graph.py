import numpy as np
import heapq
from typing import Union

class Graph:
    def __init__(self, adjacency_mat: Union[np.ndarray, str]):
        """ Unlike project 2, this Graph class takes an adjacency matrix as input. `adjacency_mat` 
        can either be a 2D numpy array of floats or the path to a CSV file containing a 2D numpy array of floats.

        In this project, we will assume `adjacency_mat` corresponds to the adjacency matrix of an undirected graph
        """
        if type(adjacency_mat) == str:
            self.adj_mat = self._load_adjacency_matrix_from_csv(adjacency_mat)
        elif type(adjacency_mat) == np.ndarray:
            self.adj_mat = adjacency_mat
        else: 
            raise TypeError('Input must be a valid path or an adjacency matrix')
        self.mst = None

    def _load_adjacency_matrix_from_csv(self, path: str) -> np.ndarray:
        with open(path) as f:
            return np.loadtxt(f, delimiter=',')

    def construct_mst(self):
        """ Given `self.adj_mat`, the adjacency matrix of a connected undirected graph, implement Prim's 
        algorithm to construct an adjacency matrix encoding the minimum spanning tree of `self.adj_mat`. 
            
        `self.adj_mat` is a 2D numpy array of floats. 
        Note that because we assume our input graph is undirected, `self.adj_mat` is symmetric. 
        Row i and column j represents the edge weight between vertex i and vertex j. An edge weight of zero indicates that no edge exists. 
        
        TODO: 
            This function does not return anything. Instead, store the adjacency matrix 
        representation of the minimum spanning tree of `self.adj_mat` in `self.mst`.
        We highly encourage the use of priority queues in your implementation. See the heapq
        module, particularly the `heapify`, `heappop`, and `heappush` functions.
        """
        
        # determine number of nodes, initialize mst as numpy array of zeros connecting all nodes
        num_nodes = np.shape(self.adj_mat)[1]
        self.mst = np.zeros(self.adj_mat.shape)
        
        # initialize a tree with a vertex closen arbitrarily from the graph
        vertices = list(range(num_nodes)) # create list with range of vertex numbers 
        curr_vertex = vertices[0] 
        visited_vertices = {curr_vertex}
        
        # store outgoing edges from visited_vertices as tuples in a priority queue, remove zeros
        outgoing_edges_with_zeros = list(self.adj_mat[1:num_nodes,curr_vertex])
        curr_vertex_list = [curr_vertex] * len(outgoing_edges_with_zeros)
        outgoing_edges_zip = list(zip(outgoing_edges_with_zeros, curr_vertex_list, vertices[1:]))
        outgoing_edges = [i for i in outgoing_edges_zip if i[0]!=0] # keep non-zero edges
        heapq.heapify(outgoing_edges)   
        
        # grow the tree by adding the minimum weight edge to a vertex not in the tree
        while(outgoing_edges):
            # determine lowest weighted edge and corresponding neighbor node
            lowest_weight_edge = heapq.heappop(outgoing_edges) # removes lowest weight edge from queue
            
            # if destination vertex isn't in vistited_vertices
            if lowest_weight_edge[2] not in visited_vertices:
                # Add this edge to our MST and add vertex to visited
                self.mst[lowest_weight_edge[1], lowest_weight_edge[2]] = lowest_weight_edge[0]
                self.mst[lowest_weight_edge[2], lowest_weight_edge[1]] = lowest_weight_edge[0]
                visited_vertices.add(lowest_weight_edge[2]) # Add the destination to visited_vertices
                # Add all outgoing edges from visited_vertices to our priority queue
                curr_vertex = lowest_weight_edge[2]
                outgoing_edges_with_zeros = list(self.adj_mat[:,curr_vertex])
                outgoing_edges_with_zeros.pop(lowest_weight_edge[1]) # remove edge that led to this node from the other side ##### this one makes them not line up anymore 
                curr_vertex_list = [curr_vertex] * len(outgoing_edges_with_zeros)
                vertices_wo_recent = [x for x in vertices if x!=lowest_weight_edge[1]]
                outgoing_edges_zip = list(zip(outgoing_edges_with_zeros, curr_vertex_list, vertices_wo_recent))
                outgoing_edges_add = [i for i in outgoing_edges_zip if i[0]!=0] # keep non-zero edges
                for edge in outgoing_edges_add:
                    heapq.heappush(outgoing_edges, edge)