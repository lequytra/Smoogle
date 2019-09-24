import numpy as np
from Graph import Graph
import os


class PageRank:

    def __init__(self, graph, prev_path=None, damping_factor=0.32, epsilon=0.00001, default_weight=None):
        self.N = graph.size()
        if prev_path and default_weight:
            print("A previous weight path is provided, previous weights will be used instead of default weights.")

        elif not prev_path:
            if not default_weight:
                default_weight = 1 / self.N

            self.prev = np.full(shape=(self.N,), fill_value=default_weight)

        else:
            self.prev = np.load(file=prev_path)

        graph = sorted(graph.graph.items(), key=lambda item: int(item[0]))
        _, val = zip(*graph)

        self.M, self.neighbors = zip(*val)

        del graph, _, val

        self.prev = np.expand_dims(self.prev, axis=1)
        self.M = np.expand_dims(self.M, axis=1)
        # Replace all the dangling links to be connected
        # to all other pages in the graph
        self.M[self.M == 0] = self.N - 1
        self.d = damping_factor
        # At initialization, current weight is equal to the previous weights
        self.curr = np.copy(self.prev)
        self.epsilon = epsilon

    def calculate_score(self, A=None):

        if A.all() is None:
            A = self.build_A()

        self.prev = np.copy(self.curr)
        M = A / self.M

        curr = (1 - self.d) / self.N + np.sum(self.d * (M * self.prev), axis=0)
        self.curr = np.expand_dims(curr, axis=1)

        try:
            assert self.curr.shape == self.prev.shape
        except AssertionError:
            print("Curr shape: {}".format(self.curr.shape))
            print("Previous shape: {}".format(self.prev.shape))

        epsilon = np.sum(np.absolute(self.curr - self.prev))

        return epsilon

    def iterate(self, max_iter=None):
        A = self.build_A()

        diff = np.Inf
        i = 0
        if max_iter is None:
            max_iter = np.Inf
        print("Start iterating ... ")
        while diff >= self.epsilon and i < max_iter:
            diff = self.calculate_score(A=A)
            i += 1
            if i % 5 == 0:
                print("Iteration {}: \t\t Loss is {}".format(i, diff))
                print("Current Weights: ")
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
            A[[int(node) for node in self.neighbors[i]], i] = 1

        return A

    def save_score(self, filename: str = None, path=None):
        """
            A method to save the current scores to a npy file.
        :param filename: name of the score file.
        :param path: the path to save file
                    if None, it will store the file in the current
                    directory
        :return: None
        """

        if not filename:
            filename = "PageRank_score"

        filename += '.npy'

        if not path:
            path = os.getcwd()
        path = os.path.join(path, 'Data')

        if not os.path.exists(path):
            os.makedirs(path)

        path = os.path.join(path, filename)

        self.curr = np.squeeze(self.curr)

        assert self.curr.shape == (self.N,)

        with open(path, 'wb') as f:
            np.save(f, self.curr, allow_pickle=False)

        return
