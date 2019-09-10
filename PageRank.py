from Graph import Graph

class PageRank:

	def __init__(self, graph=Graph(), damping_factor=0.12):
		self.graph = graph
		self.damping_factor = damping_factor
		self.has_seen = None

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
		weight, _, adj_list = self.get(root)
		if self.has_seen:
			self.has_seen.add(root)
		else:
			self.has_seen = set([root])
		for v in adj_list:
			if v not in self.has_seen:
				curr = self.calculate_rank(v) 
			else:
				curr = self.get(v)[0]
			if self.get(v)[1] != 0:
				curr /= self.get(v)[1]
				score += curr

		self.graph.graph[root] = (E + self.damping_factor*score, _, adj_list)

		return score

	def get(self, node):
		return self.graph.get(node)

	def iterate(self, root, num_iter=4):

		for i in range(4):
			# Reset has_seen set
			self.has_seen = set()
			print("Iteration {}: ".format(i + 1))
			self.calculate_rank(root)
			self.print_info()

		return


p = PageRank()
p.insert_edge('A', 'B')
p.insert_edge('A', 'E')
p.insert_edge('B', 'D')
p.insert_edge('B', 'C')
p.insert_edge('C', 'A')
p.insert_edge('D', 'C')

p.iterate('A')
p.iterate('E')

