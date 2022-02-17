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
    def __init__(self, height, width, number_of_colours):
        self.board = np.ones((height, width, number_of_colours), dtype=bool)

    def update(self, graph, n):
        pass

    def get_option(self, location):
        for i, v in enumerate(self.board[location]):
            if v:
                return i + 1


class Board:
    '''
    self.graphs contains the connected components of each key
    '''
    def __init__(self):
        self.raster_graph = nx.generators.lattice.grid_2d_graph(height, width)
        self.graphs = {i:nx.Graph() for i in range(1, number_of_colours+1)}
        self.board = np.zeros(shape, dtype=int)
        self.option_board = OptionBoard(height, width, number_of_colours)
        self._counter = 0

    def fill_randomly(self):
        self.board = np.random.randint(1, number_of_colours + 1, shape)

    def plot(self):
        x_axis = string.ascii_uppercase
        return plt.imshow(self.board, cmap=cmap, vmin=0, vmax=number_of_colours)

    def find_spaces(self):
        '''Find the first non determined space in the board; denoted with a zero'''
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return (row, col)
        return False

    def add_space(self, location, integer):
        '''Add a value at location, updating underlying data structures'''
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

        option_board = self.option_board.board[:,:,integer-1]
        connected_components = list(nx.connected_components(graph))
        if len(connected_components) == len(allowed_segment_sizes):
            option_board[:,:] = False
        elif len(connected_components) > len(allowed_segment_sizes):
            raise RuntimeError(f'More segments present than allowed ({len(allowed_segment_sizes)})')

        # loop the connected components from large to small
        for allowed_size, nodes in zip(allowed_segment_sizes, sorted(connected_components, key=len, reverse=True)):
            size = len(nodes)
            if size == allowed_size:
                neighbours = {leave for node in nodes for leave in self.raster_graph.neighbors(node)} - set(nodes)
                # neighbours = {nodes for nodes in self.raster_graph.neighbors(node)} - set(nodes)
                for neighbour in neighbours:
                    # option_board[neighbour] = False
                    self.option_board.board[neighbour[0], neighbour[1], integer-1] = False
            if size > allowed_size:
                raise RuntimeError(f'Segment larger than allowed: '
                                   f'found: {segment_sizes}, allowed: {allowed_segment_sizes}')


    def remove_space(self, location, integer):
        graph = self.graphs.get(integer)
        graph.remove_node(location)
        self.board[location] = 0

    def generate(self):
        '''Generate a playing board'''
        if not (available_location := self.find_spaces()):
            return True

        self._counter += 1
        if self._counter % 1000 == 0:
            print(self.board)
            print()
            return self.board

        if option := self.option_board.get_option(available_location):
            self.add_space(available_location, option)

            if not self.generate() is None:
                return self.board

            self.remove_space(available_location, option)
                # self.board[available_location] = 0

        return

counter = 0

a = Board()
# a.add_space((1,2), 1)
# a.add_space((2,2), 1)
# a.add_space((3,3), 1)
# nx.draw(a.graphs.get(1))
# a.plot()

b = a.generate()
