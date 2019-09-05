class Graph:
	def __init__(self, default_weight):
		self.graph = dict()
		self.default_weight = default_weight
		self.N = 0

	def insert_edge(self, parent, child):
		if parent in self.graph:
			_, outlinks, adj_list = self.graph[parent]
			adj_list += child
			self.graph[parent] = (_, outlinks + 1, adj_list)
		else:
			self.graph[parent] = (self.default_weight, 1, [child])
			self.N += 1

		if child not in self.graph:
			self.graph[child] = (self.default_weight, 1, [])
			self.N += 1

	def insert_node(self, node):
		if node not in self.graph:
			self.graph[node] = (self.default_weight, 0, [])
			self.N += 1

	def remove_edge(self, parent, child):
		if parent in self.graph:
			try:
				_, outlinks, adj_list = self.graph[parent]
				self.graph[parent] = (_, outlinks - 1, adj_list.remove(child))
				return True

			except ValueError:
				return False

		else:
			return False

	def remove_node(self, node):
		if node in self.graph:

			del self.graph[node]

			for k in self.graph.keys():
				_, outlinks, adj_list = self.graph[k]

				if node in adj_list:
					adj_list.remove(node)
					self.graph[k] = (_, outlinks - 1, adj_list)

			self.N -= 1

			return True

		else:
			return False

	def size(self):
		return self.N

	def get_info(self, node):
		if node in self.graph:
			weight, outlinks, _ = self.graph[node]
			return (weight, outlinks)

		else:
			return None

