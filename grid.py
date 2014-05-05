# coding=utf-8
__author__ = 'steman'
from random import randint
from cell import Cell


class Grid(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[Cell(x, y) for x in range(cols)] for y in range(rows)]
        self.starting_embryos_location = dict()

    def print_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print self.board[i][j].id, '\t',
            print

    def full(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j].id == -1:
                    return False
        return True

    def alive(self, row, col):
        """
        Check cell status in grid
        """
        return self.board[row][col].alive

    def set_alive(self, row, col):
        """
        Set cell to alive in grid
        """
        self.board[row][col].alive = True

    def moore(self):
        """
        Moore neighbourhood
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j].id != -1 and self.board[i][j].alive:
                    cell_id = self.board[i][j].id
                    # Cell on the right
                    if j + 1 < self.cols and self.board[i][j + 1].id == -1:
                        self.board[i][j + 1].id = cell_id
                        self.board[i][j + 1].alive = True
                        # Cell on the left
                    if j - 1 >= 0 and self.board[i][j - 1].id == -1:
                        self.board[i][j - 1].id = cell_id
                        self.board[i][j - 1].alive = True
                        # Cell on the top
                    if i + 1 < self.rows and self.board[i + 1][j].id == -1:
                        self.board[i + 1][j].id = cell_id
                        self.board[i + 1][j].alive = True
                        # Cell on the bottom
                    if i - 1 >= 0 and self.board[i - 1][j].id == -1:
                        self.board[i - 1][j].id = cell_id
                        self.board[i - 1][j].alive = True
                        # Cell on the top right
                    if j + 1 < self.cols and i + 1 < self.rows and self.board[i][j + 1].id == -1:
                        self.board[i + 1][j + 1].id = cell_id
                        self.board[i + 1][j + 1].alive = True
                        # Cell on the top left
                    if j - 1 >= 0 and i + 1 < self.rows and self.board[i][j - 1].id == -1:
                        self.board[i + 1][j - 1].id = cell_id
                        self.board[i + 1][j - 1].alive = True
                        # Cell on the bottom right
                    if i - 1 >= 0 and j + 1 < self.cols and self.board[i - 1][j].id == -1:
                        self.board[i - 1][j + 1].id = cell_id
                        self.board[i - 1][j + 1].alive = True
                        # Cell on the bottom left
                    if i - 1 >= 0 and j - 1 >= 0 and self.board[i - 1][j].id == -1:
                        self.board[i - 1][j - 1].id = cell_id
                        self.board[i - 1][j - 1].alive = True

    def von_neuman(self):
        """
        Von Neuman neighbourhood
        """
        while(not self.full()):
            for nr, id in enumerate(self.starting_embryos_location.keys()):
                new_embryos = list()
                for cell in self.starting_embryos_location[id]:
                    # Cell on the right
                    if cell.x + 1 < self.cols and self.board[cell.y][cell.x + 1].id == -1:
                        # Add new embryo
                        new_embryos.append(Cell(cell.x+1, cell.y, True, cell.id))
                    # Cell on the left
                    if cell.x - 1 >= 0 and self.board[cell.y][cell.x - 1].id == -1:
                        # Add new embryo
                        new_embryos.append(Cell(cell.x-1, cell.y, True, cell.id))
                    # Cell on the bottom
                    if cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x].id == -1:
                        # Add new embryo
                        new_embryos.append(Cell(cell.x, cell.y+1, True, cell.id))
                    # Cell on the top
                    if cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x].id == -1:
                        # Add new embryo
                        new_embryos.append(Cell(cell.x, cell.y-1, True, cell.id))
                del self.starting_embryos_location[id]
                self.starting_embryos_location[id] = list()
                self.starting_embryos_location[id].extend(new_embryos)
                # Add new seeds
                for cell in new_embryos:
                    self.board[cell.y][cell.x] = cell


    def hexagonal_left(self):
        """
        Left hexagonal neighbourood
        """
        pass

    def hexagonal_right(self):
        """
        Right hexagonal neighbourood
        """
        pass

    def hexagonal_random(self):
        """
        Random hexagonal neighbourood
        """
        pass

    def pentagonal_random(self):
        """
        Random pentagonal neighbourood
        """
        pass

    def random_embryo_loc(self, quantity):
        """
        Set random location of @quantity embryons
        """
        print "Random embyos:"
        for i in range(quantity):
            random_row = randint(0, self.rows - 1)
            random_col = randint(0, self.cols - 1)
            self.board[random_row][random_col].alive = True
            self.board[random_row][random_col].id = i
            self.board[random_row][random_col].x = random_col
            self.board[random_row][random_col].y = random_row
            self.starting_embryos_location[i] = list()
            self.starting_embryos_location[i].append(self.board[random_row][random_col])
            print "row[{}] col[{}] x={}, y={}".format(random_row, random_col, self.board[random_row][random_col].x,
                                                      self.board[random_row][random_col].y)

    def linear_embryo_loc(self, quantity, offset):
        """
        Set location of @quantity embryons with given offset
        """
        pass

    def radius_embryo_loc(self, quantity, radius):
        """
        Set location of @quantity embryons with given radius
        """
        pass

    def mouse_embyro_loc(self):
        """
        Set location of @quantity embryons with mouse clicks
        """
        pass

    def periodic_bc(self):
        """
        Set periodic border conditions
        """
        pass

    def nonperiodic_bc(self):
        """
        Set nonperiodic border conditions
        """
        pass


if __name__ == '__main__':
    grid = Grid(30, 20)

    grid.random_embryo_loc(3)
    print "Von Neuman"
    grid.von_neuman()
    grid.print_board()
