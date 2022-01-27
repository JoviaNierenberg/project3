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
        print(self.adj_mat) ################
        
        # determine number of nodes, initialize mst as numpy array of zeros connecting all nodes
        self.num_nodes = np.shape(self.adj_mat)[1]
        self.mst = numpy.zeros((self.num_nodes, self.num_nodes))
        
        # initialize a tree with a vertex closen arbitrarily from the graph
        self.vertices = [*range(self.num_nodes)] # create list with range of vertex numbers 
        self.curr_vertex = self.vertices.pop(0)
        self.visted_vertices = [self.curr_vertex]
        heapq.heapify(self.visted_vertices)
        print(self.visted_vertices)
        
        # store outgoing edges from visited_vertices as tuples in a priority queue, remove zeros
        self.outgoing_edges_with_zeros = list(self.adj_mat[:,self.curr_vertex])
        self.outgoing_edges_with_zeros.pop(0)
        self.curr_vertex_list = [self.curr_vertex] * len(self.outgoing_edges_with_zeros)
        self.outgoing_edges_zip = list(zip(self.outgoing_edges_with_zeros, self.curr_vertex_list, self.vertices))
        self.outgoing_edges = [i for i in self.outgoing_edges_zip if i[0]!=0] # keep non-zero edges
        print(self.outgoing_edges)
        heapq.heapify(self.outgoing_edges)   
        
        # grow the tree by adding the minimum weight edge to a vertex not in the tree
        while(self.outgoing_edges):
            print("starting while loop")
            # determine lowest weighted edge and corresponding neighbor node
            print(self.outgoing_edges)
            self.lowest_weight_edge = heapq.heappop(self.outgoing_edges) # removes lowest weight edge from queue
            print(self.lowest_weight_edge)
            
            # if destination vertex isn't in vistited_vertices
            if self.lowest_weight_edge[2] not in self.visted_vertices:
                print("meow")
                # Add this edge to our MST
                self.mst[self.lowest_weight_edge[1], self.lowest_weight_edge[2]] = self.lowest_weight_edge[0]
                self.mst[self.lowest_weight_edge[2], self.lowest_weight_edge[1]] = self.lowest_weight_edge[0]
                # Add the destination to visited_vertices
                heapq.heappush(self.visted_vertices, self.lowest_weight_edge[2])
                print(list(self.visted_vertices))
                # Add all outgoing edges from visited_vertices to our priority queue
                self.curr_vertex = self.lowest_weight_edge[2]
                print(self.curr_vertex)
                self.outgoing_edges_with_zeros = list(self.adj_mat[:,self.curr_vertex])
                print("woof")
                print(self.outgoing_edges_with_zeros)
                self.outgoing_edges_with_zeros.pop(self.lowest_weight_edge[1]) # remove edge that led to this node from the other side
                self.curr_vertex_list = [self.curr_vertex] * len(self.outgoing_edges_with_zeros)
                self.outgoing_edges_zip = list(zip(self.outgoing_edges_with_zeros, self.curr_vertex_list, self.vertices))
                self.outgoing_edges_add = [i for i in self.outgoing_edges_zip if i[0]!=0] # keep non-zero edges
                print("grrr")
                print(self.outgoing_edges_add)
                for edge in self.outgoing_edges_add:
                    heapq.heappush(self.outgoing_edges, edge)
                print(self.outgoing_edges)
                
                print(self.mst)