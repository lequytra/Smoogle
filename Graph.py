class Graph:
	def __init__(self, default_weight=0.2):
		self.graph = dict()
		self.default_weight = default_weight
		self.N = 0

	def insert_edge(self, parent, child):
		if child in self.graph:
			_, outlinks, adj_list = self.graph[child]
			adj_list += [parent]
			self.graph[child] = (_, outlinks, adj_list)
		else:
			self.graph[child] = (self.default_weight, 1, [parent])
			self.N += 1

		if parent in self.graph:
			_, outlinks, ls = self.graph[parent]
			self.graph[parent] = (_, outlinks + 1, ls)
		else: 
			self.graph[parent] = (self.default_weight, 1, [])
			self.N += 1

	def insert_node(self, node):
		if node not in self.graph:
			self.graph[node] = (self.default_weight, 0, [])
			self.N += 1

	def remove_edge(self, parent, child):
		if child in self.graph:

			_, n, adj_list = self.graph[child]
			if parent in adj_list:
				self.graph[child][2] = (_, n, self.graph[child].remove(parent))
				weight, n_parent, ls = self.get(parent)
				self.graph[parent] =  (weight, n_parent - 1, ls)
				return True
			else:
				return False

		else:
			return False

	def remove_node(self, node):
		if node in self.graph:
			_, _, adj_list = self.graph[node]
			del self.graph[node]

			for k in adj_list:
				weight, n, ls = self.get(k)
				self.graph[k] = (weight, n - 1, ls)

			self.N -= 1

			return True

		else:
			return False

	def size(self):
		return self.N

	def get(self, node):
		return self.graph[node]

	def reset_weight(self):
		self.default_weight = 1/self.N
		for item in self.graph.keys():
			self.graph[item][0] = self.default_weight

	def get_info(self, node):
		if node in self.graph:
			weight, outlinks, _ = self.graph[node]
			return (weight, outlinks)

		else:
			return None

