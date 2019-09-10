import numpy as np 
from Graph import Graph

class PageRank:

	def __init__(self, graph, damping_factor=0.32, epsilon=0.00001):
		self.N = graph.size()

		graph = sorted(graph.graph.items(), key= lambda item: item[0])
		_, val = zip(*graph)
		self.prev, self.M, self.neighbors = zip(*val)
		self.prev = np.expand_dims(self.prev, axis=1)
		self.M = np.expand_dims(self.M, axis=1)
		# Replace all the danling links to be connected
		# to all other pages in the graph
		self.M[self.M == 0] = self.N - 1
		self.d = damping_factor
		self.curr = self.prev
		self.epsilon = epsilon

	def calculate_score(self, A=None):

		if A.all() == None:
			A = self.build_A()

		self.prev = self.curr
		M = A/self.M
		# print(M)
		# print("Curr weights")
		# print(M*self.prev)
		# print("Curr matrix")
		# print((1 - self.d)/self.N + self.d*(M*self.prev))
		curr = (1 - self.d)/self.N + np.sum(self.d*(M*self.prev), axis=0)
		self.curr = np.expand_dims(curr, axis=0)

		epsilon = np.sum(np.absolute(self.curr - self.prev))

		return epsilon

	def iterate(self, max_iter=None):
		A = self.build_A()

		diff = np.Inf
		i = 0
		if max_iter == None:
			max_iter = np.Inf

		while diff >= self.epsilon and i < max_iter:
			diff = self.calculate_score(A=A)
			i += 1
			print(self.curr)
		return self.curr

	def build_A(self):
		A = np.zeros((self.N, self.N))

		for i in range(self.N):
			# if the current node has no outlinks
			if self.M[i] == self.N - 1:
				# it is assumed that it is connected to
				# all other pages
				A[i, :] = 1
				A[i, i] = 0
			# Set adjacency
			A[[node for node in self.neighbors[i]], i] = 1

		return A

g = Graph()
g.insert_edge(0, 1)
g.insert_edge(0, 4)
g.insert_edge(1, 2)
g.insert_edge(1, 3)
g.insert_edge(2, 0)
g.insert_edge(3, 2)
p = PageRank(g)
p.iterate(max_iter=None)