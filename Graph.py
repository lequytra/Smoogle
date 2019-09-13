class Graph:
	def __init__(self, default_weight=0.2):
		self.graph = dict()
		self.default_weight = default_weight
		self.N = 0

	def insert_edge(self, parent, child):
		# If the incoming page is already in the graph
		if child in self.graph:
			_, outlinks, adj_list = self.graph[child]
			# Add parent to be one of the incoming page
			adj_list.add(parent)
			self.graph[child] = (_, outlinks, adj_list)
		else:
			# else, insert the child in the graph
			self.graph[child] = (self.default_weight, 0, set([parent]))
			self.N += 1 # Increase the total number of nodes in the graph
		# If the parent page exists in the graph
		if parent in self.graph:
			_, outlinks, ls = self.graph[parent]
			# Increase the number of forwardlinks of the parent page
			self.graph[parent] = (_, outlinks + 1, ls)
		else: 
			# Else insert the parent page into the graph
			self.graph[parent] = (self.default_weight, 1, set([]))
			self.N += 1 # Increase the total number of nodes

		print(self.get())

	def insert_node(self, node):
		"""
			A method to insert a new node into the graph
		"""
		if node not in self.graph:
			self.graph[node] = (self.default_weight, 0, set())
			self.N += 1

	def remove_edge(self, parent, child):
		# If the child page exist in the graph
		if child in self.graph:
			_, n, adj_list = self.graph[child]
			# If the parent page is in the adjacency list
			if parent in adj_list:
				self.graph[child] = (_, n, self.graph[child].remove(parent))
				weight, n_parent, ls = self.get(parent)
				self.graph[parent] =  (weight, n_parent - 1, ls)

				return True

			else:
				return False

		else:
			return False

	def remove_node(self, node):
		# If the node to be deleted is in the graph
		if node in self.graph:
			# Get its adjacency list
			_, _, adj_list = self.graph[node]
			del self.graph[node]
			# For every parent page
			for k in adj_list:
				weight, n, ls = self.get(k)
				self.graph[k] = (weight, n - 1, ls)
			# Decrease the total number of nodes
			self.N -= 1

			return True

		else:
			return False

	def size(self):
		return self.N

	def get(self, node=None):
		if not node:
			return self.graph.values()

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

