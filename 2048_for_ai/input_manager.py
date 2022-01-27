
from grid import Grid

import random
import numpy as np

class Input_Manager():

    def get_neuron_input(grids: list[Grid]):
        for grid in grids:
            flatt = np.matrix(grid.tile_data)
            input = np.ndarray.flatten(flatt)

    def test():
        grid = Grid(2,2)
        grid2 = Grid(2,4)
        grids = [grid, grid2]
        Input_Manager.get_neuron_input(grids)

    def randomize_for_grids(grids: list[Grid]):
        for grid in grids:
            dir_x = random.randint(-1,1)
            dir_y = random.choice((-1,1)) if dir_x == 0 else 0
            Input_Manager.send_input(grid, (dir_x, dir_y))

    def send_input(grid: Grid, dir: tuple):
        grid.move_manager(dir)
Input_Manager.test()