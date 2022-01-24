
from grid import Grid

import random
class Input_Manager():

    def randomize_for_grids(grids: list[Grid]):
        for grid in grids:
            dir_x = random.randint(-1,1)
            dir_y = random.choice((-1,1)) if dir_x == 0 else 0
            Input_Manager.send_input(grid, (dir_x, dir_y))

    def send_input(grid: Grid, dir: tuple):
        grid.move_manager(dir)
