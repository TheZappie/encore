import string

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
import networkx as nx


used_colors = ['w', '#154a8b', '#980f11', '#fdc086', '#ffff99', '#386cb0', '#f0027f', '#bf5b17', '#666666']
cmap = colors.ListedColormap(used_colors)


allowed_segment_sizes = range(6, 0, -1)

width = 15
height = 7
number_of_colours = 5
shape = (height, width)

class OptionBoard:
    def __init__(self):
        self.board = np.ones((height, width, number_of_colours), dtype=bool)
        # color_list = list(range(1, number_of_colours+1))
        # self.left_over_matrix = [[color_list] * height] * width

        def update(self, graph, n):
            pass

        def get_options(self):
            pass


class Board:
    '''
    self.graphs contains the connected components of each key
    '''
    def __init__(self):
        self.raster_graph = nx.generators.lattice.grid_2d_graph(height, width)
        self.graphs = {i:nx.Graph() for i in range(1, number_of_colours+1)}
        self.board = np.zeros(shape, dtype=int)

    def fill_randomly(self):
        self.board = np.random.randint(1, number_of_colours + 1, shape)

    def plot(self):
        x_axis = string.ascii_uppercase
        return plt.imshow(self.board, cmap=cmap, vmin=0, vmax=number_of_colours)

    def find_spaces(self): # finds the first empty space in the board; where there is not a number
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return (row, col)
        return False

    def add_space(self, location, integer):
        graph = self.graphs.get(integer)
        # if not graph is None:
        #     raise ValueError('Integer has no graph associated with it')
        if location in graph:
            raise ValueError(f'Node {location} already in graph {integer}')
        self.board[location] = integer
        graph.add_node(location)
        for node in self.raster_graph.neighbors(location):
            if node in graph:
                graph.add_edge(node, location)

        # self.left_over_matrix[location[0], ]

    def remove_space(self, location, integer):
        graph = self.graphs.get(integer)
        graph.remove_node(location)
        self.board[location] = 0

    def check_space(self, location, integer):
        '''Checks to see if a integer can be fitted into a specific location; row, col'''
        graph = self.graphs.get(integer)
        # if not graph is None:
        #     raise ValueError(f'Given value {integer} has no graph associated with it')
        # for node in self.raster_graph.neighbors(location):
        #     if node in graph:
        #         len(nx.node_connected_component(graph, node))
        if location in graph:
            raise ValueError(f'Node {location} already in graph {integer}')
        neighbors = self.raster_graph.neighbors(location)
        graph.add_node(location)
        for node in neighbors:
            if node in graph:
                graph.add_edge(node, location)
        # future_segment_size = 1+sum(len(nx.node_connected_component(graph, node)) for node in neighbors if node in graph)

        segment_sizes = [len(nodes) for nodes in nx.connected_components(graph)]
        if len(segment_sizes) > len(allowed_segment_sizes):
            graph.remove_node(location)
            return False
        for i, j in zip(allowed_segment_sizes, sorted(segment_sizes, reverse=True)):
            # print(i,j)
            if j > i:
                graph.remove_node(location)
                return False
        # self.graphs[integer] = graph
        graph.remove_node(location)
        return True

    def generate(self):
        '''Generate a playing board'''        
        spacesAvailable = self.find_spaces()
        if not spacesAvailable:
            return True

        counter += 1
        if counter % 1000 == 0:
            print(self.board)
            print()
            return self.board

        for n in range(1, number_of_colours + 1):
            if self.check_space(spacesAvailable, n):
                # self.board[spacesAvailable] = n
                self.add_space(spacesAvailable, n)

                if not self.generate() is None:
                    return self.board

                self.remove_space(spacesAvailable, n)
                # self.board[spacesAvailable] = 0

        return

counter = 0

a = Board()
# a.add_space((1,2), 1)
# a.add_space((2,2), 1)
# a.add_space((3,3), 1)
# nx.draw(a.graphs.get(1))
# a.plot()

b = a.generate()
