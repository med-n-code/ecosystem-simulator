# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 20:13:20 2020

@author: med-n-code
"""


class Grid_cell():

    def __init__(self, position):
        """
        Constructor method

        Parameters
        ----------
        position : tuple of int
            The position (row,col) of the cell.

        Returns
        -------
        None.

        """

        self.position = position  # cell's position (row,col)

        # List of lists of neighbours, where list n is the neighbours that are on
        # the 'ring' n + 1 units away
        self.neighbours = [[], [], []]

    def get_neighbours(self, up_to_distance):
        return [self.neighbours[i] for i in range(up_to_distance)]

    def get_position(self):
        return self.position

    def get_row(self):
        return self.position[0]

    def get_column(self):
        return self.position[1]

    def define_neighbours(self, grid):
        """
        Creates a list of all the neighbours of self in grid

        Parameters
        ----------
        grid : list of lists of Grid_cells (2D array of Grid_cells)
            All the cells in the simulation's grid with their indices
            correlating to their position.

        Returns
        -------
        None.
        """

        my_row = self.position[0]  # row of self
        my_col = self.position[1]  # col of self

        # Max dist is len of array (e.g. 4) but we only go to len - 1 (e.g. 3)
        max_dist = len(self.neighbours)

        grid_size = len(grid)  # size of the grid

        # Start and end row to generate neighbours, can't be lower than 0 or higher
        # than  grid_size respectively
        start_row = max(0, my_row - max_dist)
        end_row = min(grid_size, my_row + max_dist + 1)

        # Start and end column to generate neighbours, can't be lower than 0 or higher
        # than  grid_size respectively
        start_col = max(0, my_col - max_dist)
        end_col = min(grid_size, my_col + max_dist + 1)

        # if row is 5 and radius max is 3, cycle from 2 (incl.) to 9 (excl.)
        for i in range(start_row, end_row):

            # if col is 5 and radius max is 3, cycle from 2 (incl.) to 9 (excl.)
            for j in range(start_col, end_col):

                # calculate the max grid distance (either vert or horiz) from position
                # 2 2 2 2 2 2 2
                # 2 1 1 1 1 1 2
                # 2 1 0 0 0 1 2
                # 2 1 0 P 0 1 2
                # 2 1 0 0 0 1 2
                # 2 1 1 1 1 1 2
                # 2 2 2 2 2 2 2 
                ring_distance_from_position = max(abs(my_row - i), abs(my_col - j))

                if (ring_distance_from_position > 0):
                    self.neighbours[ring_distance_from_position - 1].append(grid[i][j])

    def get_available_neighbours(self, avoid_positions=[], up_to_distance=1):
        """
        ...

        Parameters
        ----------
        avoid_positions : list of tuples of ints, optional
            DESCRIPTION. The default is [].
        selected_distance : int, optional
            DESCRIPTION. The default is 1.

        Returns
        -------
        available_neighbours : list of Grid_cells
            DESCRIPTION.

        """

        available_neighbours = [[] * up_to_distance]

        # If is_empty is False, then available_neighbours is self.neighbours.
        # If is_empty is True, then available_neighbours is elements of
        # self.neighbours that are also devoid of an animal.
        for d in range(up_to_distance):
            available_neighbours[d].extend([self.neighbours[d][i]
                                            for i in range(len(self.neighbours[d]))
                                            if (not (self.neighbours[d][i].position in avoid_positions))])

        return available_neighbours
