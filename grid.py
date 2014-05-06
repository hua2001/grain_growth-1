# coding=utf-8
import Tkinter

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
        while(not self.full()):
            for id in self.starting_embryos_location.keys():
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
                    # Cell on the top left
                    if cell.x - 1 >= 0 and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x - 1] == -1:
                        new_embryos.append(Cell(cell.x-1, cell.y-1, True, cell.id))
                    # Cell on the top right
                    if cell.x + 1 < self.cols and cell.y -1 >= 0 and self.board[cell.y - 1][cell.x + 1] == -1:
                        new_embryos.append(Cell(cell.x+1, cell.y-1, True, cell.id))
                    # Cell on the bottom left
                    if cell.x - 1 >= 0 and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x - 1] == -1:
                        new_embryos.append(Cell(cell.x-1, cell.y-1, True, cell.id))
                    # Cell on the bottom right
                    if cell.x + 1 < self.cols and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x - 1] == -1:
                        new_embryos.append(Cell(cell.x-1, cell.y-1, True, cell.id))
                del self.starting_embryos_location[id]
                self.starting_embryos_location[id] = list()
                self.starting_embryos_location[id].extend(new_embryos)
                # Add new seeds
                for cell in new_embryos:
                    self.board[cell.y][cell.x] = cell

    def von_neuman(self):
        """
        Von Neuman neighbourhood
        """
        # while(not self.full()):
        for id in self.starting_embryos_location.keys():
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

root = Tkinter.Tk()
r, c = 20, 20
cells = [[0 for x in range(c)] for y in range(r)]


def update(grid):
    grid.von_neuman()
    for i in range(grid.rows):
        for j in range(grid.cols):
            color = 'white'
            if grid.board[i][j].id == 0:
                color = 'red'
            elif grid.board[i][j].id == 1:
                color = 'blue'
            elif grid.board[i][j].id == 2:
                color = "green"
            cells[i][j].configure(background=color)
    root.after(125, update, grid)

if __name__ == '__main__':
    grid = Grid(r, c)
    # grid2 = Grid(15, 15)
    grid.random_embryo_loc(3)
    # grid2.random_embryo_loc(3)
    # print "Von Neuman"
    # grid.von_neuman()
    for i in range(grid.rows):
        for j in range(grid.cols):
            color = 'white'
            if grid.board[i][j].id == 0:
                color = 'red'
            elif grid.board[i][j].id == 1:
                color = 'blue'
            elif grid.board[i][j].id == 2:
                color = "green"
            cells[i][j] = Tkinter.Canvas(root, background=color, width=10, height=10, borderwidth=0)
            cells[i][j].grid(row=i, column=j)
    update(grid)
    root.mainloop()

    # grid.print_board()
    # print "Moore"
    # grid2.moore()
    # grid2.print_board()
