def construct_mst(self):   
        mst = np.zeros(self.adj_mat.shape)
        visited = {0}

        pq = [(self.adj_mat[0, node], (0, node)) for node in range(self.adj_mat.shape[0]) if self.adj_mat[0, node] > 0]
        heapq.heapify(pq)
        while len(visited) < self.adj_mat.shape[0]:
            weight, (v1, v2) = heapq.heappop(pq)
            if v2 not in visited:
                mst[v1, v2] = weight
                mst[v2, v1] = weight
                visited.add(v2)
                for node in range(self.adj_mat.shape[0]):
                    if node not in visited and self.adj_mat[v2, node] > 0:
                        heapq.heappush(pq, (self.adj_mat[v2, node], (v2, node)))
        self.mst = mst
