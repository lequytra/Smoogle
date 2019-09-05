from Graph import Graph

class PageRank:

	def __init__(self, graph, damping_factor=0.31):
		self.graph = graph
		self.damping_factor = damping_factor
		self.has_seen = set([])

	def insert_node(self, node):
		self.graph.insert_node(node)

	def insert_edge(self, parent, child):
		self.graph.insert_edge(parent, child)

	def remove_node(self, node):
		self.graph.remove_node(node)

	def remove_edge(self, parent, child):
		self.graph.remove_edge(parent, child)

	def print_info(self, node=None):
		if node != None:
			weight, _ = self.graph.get_info(node)
			print("Page {} has the weight {}\n".format(node, weight))

		else:
			for node in self.graph.graph.keys():
				weight, _ = self.graph.get_info(node)
				print("Page {} has the weight {}\n".format(node, weight))

	def calculate_rank(self, root):
		E = float((1 - self.damping_factor))/float(self.graph.size()) 
		score = 0
		weight, _, adj_list = self.graph.graph[root]
		self.has_seen = self.has_seen.add(root)
		for v in adj_list:

			curr = self.calculate_rank(v) if v not in self.has_seen else self.graph.graph[v][0]
			if self.graph.graph[v][1] != 0:
				curr /= self.graph.graph[v][1]
				score += curr

		self.graph.graph[root] = (E + score, _, adj_list)
		print("Updated {}".format(root))

		return score

	def iterate(self, root, num_iter=4):

		for i in range(4):
			self.has_seen = set([])
			print("Iteration {}:".format(i + 1))
			self.calculate_rank(root)
			self.print_info()

		return

graph = Graph(default_weight=0.2)
graph.insert_edge('A', 'B')
graph.insert_edge('A', 'E')
graph.insert_edge('B', 'D')
graph.insert_edge('B', 'C')
graph.insert_edge('D', 'C')
graph.insert_edge('C', 'A')
p = PageRank(graph)
p.iterate('A')


