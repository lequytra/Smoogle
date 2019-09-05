from Graph import Graph

class PageRank:

	def __init__(self, graph, damping_factor=0.31):
		self.graph = graph
		self.damping_factor = damping_factor

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
			for node in self.graph.keys():
				weight, _ = self.graph.get_info(node)
				print("Page {} has the weight {}\n".format(node, weight))

	def calculate_rank(self, root):
		E = float((1 - self.damping_factor))/float(self.graph.size()) 
		score = 0
		weight, _, adj_list = self.graph[root]
		has_seen = set([root])
		for v in adj_list:
			curr = self.calculate_rank(v) if v not in has_seen else self.graph[v][0]
			if self.graph[v][1] != 0:
				curr /= self.graph[v][1]
				score += curr

		self.graph[root] = (score, _, adj_list)


		return score

	def iterate(self, root, num_iter=4):

		for i in range(4):
			self.calculate_rank(root)
			self.print_info()

		return
		



