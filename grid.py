# coding=utf-8
__author__ = 'steman'
import Tkinter
from random import randint
from cell import Cell


class Grid(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[Cell(x, y) for x in range(cols)] for y in range(rows)]
        self.starting_embryos_location = dict()
        self.new_grains = list()

    def is_full(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j].id == -1:
                    return False
        return True

    def add_new_grains(self, id):
        del self.starting_embryos_location[id]
        self.starting_embryos_location[id] = list()
        self.starting_embryos_location[id].extend(self.new_grains)
        for cell in self.new_grains:
            self.board[cell.y][cell.x] = cell
        self.new_grains = list()

    def moore(self, border_cond=False):
        """
		Moore neighbourhood
		"""
        for id in self.starting_embryos_location.keys():
            for cell in self.starting_embryos_location[id]:
                if border_cond:
                    self.periodic_bc(cell)
                # Cell on the top left
                if cell.x - 1 >= 0 and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x - 1].id == -1 \
                    and not self.board[cell.y - 1][cell.x - 1].alive:
                    self.new_grains.append(Cell(cell.x - 1, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x - 1].alive = True
                # Cell on the top right
                if cell.x + 1 < self.cols and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x + 1].id == -1 \
                    and not self.board[cell.y - 1][cell.x + 1].alive:
                    self.new_grains.append(Cell(cell.x + 1, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x + 1].alive = True
                # Cell on the bottom left
                if cell.x - 1 >= 0 and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x - 1].id == -1 \
                    and not self.board[cell.y + 1][cell.x - 1].alive:
                    self.new_grains.append(Cell(cell.x - 1, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x - 1].alive = True
                # Cell on the bottom right
                if cell.x + 1 < self.cols and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x + 1].id == -1 \
                    and not self.board[cell.y + 1][cell.x + 1].alive:
                    self.new_grains.append(Cell(cell.x + 1, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x + 1].alive = True
                # Cell on the right
                if cell.x + 1 < self.cols and self.board[cell.y][cell.x + 1].id == -1 \
                    and not self.board[cell.y][cell.x + 1].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x + 1, cell.y, True, cell.id))
                    self.board[cell.y][cell.x + 1].alive = True
                # Cell on the left
                if cell.x - 1 >= 0 and self.board[cell.y][cell.x - 1].id == -1 \
                    and not self.board[cell.y][cell.x - 1].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x - 1, cell.y, True, cell.id))
                    self.board[cell.y][cell.x - 1].alive = True
                # Cell on the bottom
                if cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x].id == -1 \
                    and not self.board[cell.y + 1][cell.x].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x].alive = True
                # Cell on the top
                if cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x].id == -1 \
                    and not self.board[cell.y - 1][cell.x].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x].alive = True
            self.add_new_grains(id)

    def von_neuman(self, border_cond=False):
        """
		Von Neuman neighbourhood
		"""
        for id in self.starting_embryos_location.keys():
            for cell in self.starting_embryos_location[id]:
                # Cell on the right
                if border_cond:
                    self.periodic_bc(cell)
                if cell.x + 1 < self.cols and self.board[cell.y][cell.x + 1].id == -1 \
                    and not self.board[cell.y][cell.x + 1].alive:
                    new_cell = Cell(cell.x + 1, cell.y, True, cell.id)
                    self.new_grains.append(new_cell)
                    self.board[cell.y][cell.x + 1].alive = True
                # Cell on the left
                if cell.x - 1 >= 0 and self.board[cell.y][cell.x - 1].id == -1 \
                    and not self.board[cell.y][cell.x - 1].alive:
                    new_cell = Cell(cell.x - 1, cell.y, True, cell.id)
                    self.new_grains.append(new_cell)
                    self.board[cell.y][cell.x - 1].alive = True
                # Cell on the bottom
                if cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x].id == -1 \
                    and not self.board[cell.y + 1][cell.x].alive:
                    new_cell = Cell(cell.x, cell.y + 1, True, cell.id)
                    self.new_grains.append(new_cell)
                    self.board[cell.y + 1][cell.x].alive = True
                # Cell on the top
                if cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x].id == -1 \
                    and not self.board[cell.y - 1][cell.x].alive:
                    new_cell = Cell(cell.x, cell.y - 1, True, cell.id)
                    self.new_grains.append(new_cell)
                    self.board[cell.y - 1][cell.x].alive = True
            self.add_new_grains(id)

    def hexagonal_left(self, border_cond=False):
        """
		Left hexagonal neighbourhood
		"""
        for id in self.starting_embryos_location.keys():
            for cell in self.starting_embryos_location[id]:
                if border_cond:
                    self.periodic_bc(cell)
                # Cell on the top left
                if cell.x - 1 >= 0 and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x - 1].id == -1 \
                    and not self.board[cell.y - 1][cell.x - 1].alive:
                    self.new_grains.append(Cell(cell.x - 1, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x - 1].alive = True
                # Cell on the left
                if cell.x - 1 >= 0 and self.board[cell.y][cell.x - 1].id == -1 \
                    and not self.board[cell.y][cell.x - 1].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x - 1, cell.y, True, cell.id))
                    self.board[cell.y][cell.x - 1].alive = True
                # Cell on the top
                if cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x].id == -1 \
                    and not self.board[cell.y - 1][cell.x].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x].alive = True
                # Cell on the right
                if cell.x + 1 < self.cols and self.board[cell.y][cell.x + 1].id == -1 \
                    and not self.board[cell.y][cell.x + 1].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x + 1, cell.y, True, cell.id))
                    self.board[cell.y][cell.x + 1].alive = True
                # Cell on the bottom
                if cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x].id == -1 \
                    and not self.board[cell.y + 1][cell.x].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x].alive = True
                # Cell on the bottom right
                if cell.x + 1 < self.cols and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x + 1].id == -1 \
                    and not self.board[cell.y + 1][cell.x + 1].alive:
                    self.new_grains.append(Cell(cell.x + 1, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x + 1].alive = True
            self.add_new_grains(id)

    def hexagonal_right(self, border_cond=False):
        """
		Right hexagonal neighbourhood
		"""
        for id in self.starting_embryos_location.keys():
            for cell in self.starting_embryos_location[id]:
                if border_cond:
                    self.periodic_bc(cell)
                # Cell on the top right
                if cell.x + 1 < self.cols and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x + 1].id == -1 \
                    and not self.board[cell.y - 1][cell.x + 1].alive:
                    self.new_grains.append(Cell(cell.x + 1, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x + 1].alive = True
                # Cell on the bottom left
                if cell.x - 1 >= 0 and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x - 1].id == -1 \
                    and not self.board[cell.y + 1][cell.x - 1].alive:
                    self.new_grains.append(Cell(cell.x - 1, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x - 1].alive = True
                # Cell on the right
                if cell.x + 1 < self.cols and self.board[cell.y][cell.x + 1].id == -1 \
                    and not self.board[cell.y][cell.x + 1].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x + 1, cell.y, True, cell.id))
                    self.board[cell.y][cell.x + 1].alive = True
                # Cell on the left
                if cell.x - 1 >= 0 and self.board[cell.y][cell.x - 1].id == -1 \
                    and not self.board[cell.y][cell.x - 1].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x - 1, cell.y, True, cell.id))
                    self.board[cell.y][cell.x - 1].alive = True
                # Cell on the bottom
                if cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x].id == -1 \
                    and not self.board[cell.y + 1][cell.x].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x].alive = True
                # Cell on the top
                if cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x].id == -1 \
                    and not self.board[cell.y - 1][cell.x].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x].alive = True
            self.add_new_grains(id)

    def hexagonal_random(self, border_cond=False):
        """
		Random hexagonal neighbourhood
		"""
        rand_num = randint(0, 10)
        if rand_num % 2:
            self.hexagonal_left(border_cond)
        else:
            self.hexagonal_right(border_cond)

    def pentagonal_left(self, border_cond=False):
        """
		Pentagonal left neighbourhood
		"""
        for id in self.starting_embryos_location.keys():
            for cell in self.starting_embryos_location[id]:
                if border_cond:
                    self.periodic_bc(cell)
                # Cell on the top left
                if cell.x - 1 >= 0 and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x - 1].id == -1 \
                    and not self.board[cell.y - 1][cell.x - 1].alive:
                    self.new_grains.append(Cell(cell.x - 1, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x - 1].alive = True
                # Cell on the left
                if cell.x - 1 >= 0 and self.board[cell.y][cell.x - 1].id == -1 \
                    and not self.board[cell.y][cell.x - 1].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x - 1, cell.y, True, cell.id))
                    self.board[cell.y][cell.x - 1].alive = True
                # Cell on the top
                if cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x].id == -1 \
                    and not self.board[cell.y - 1][cell.x].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x].alive = True
                # Cell on the bottom left
                if cell.x - 1 >= 0 and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x - 1].id == -1 \
                    and not self.board[cell.y + 1][cell.x - 1].alive:
                    self.new_grains.append(Cell(cell.x - 1, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x - 1].alive = True
                # Cell on the bottom
                if cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x].id == -1 \
                    and not self.board[cell.y + 1][cell.x].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x].alive = True
            self.add_new_grains(id)

    def pentagonal_right(self, border_cond=False):
        """
		Pentagonal left neighbourhood
		"""
        for id in self.starting_embryos_location.keys():
            for cell in self.starting_embryos_location[id]:
                if border_cond:
                    self.periodic_bc(cell)
                # Cell on the top right
                if cell.x + 1 < self.cols and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x + 1].id == -1 \
                    and not self.board[cell.y - 1][cell.x + 1].alive:
                    self.new_grains.append(Cell(cell.x + 1, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x + 1].alive = True
                # Cell on the top
                if cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x].id == -1 \
                    and not self.board[cell.y - 1][cell.x].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x, cell.y - 1, True, cell.id))
                    self.board[cell.y - 1][cell.x].alive = True
                # Cell on the right
                if cell.x + 1 < self.cols and self.board[cell.y][cell.x + 1].id == -1 \
                    and not self.board[cell.y][cell.x + 1].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x + 1, cell.y, True, cell.id))
                    self.board[cell.y][cell.x + 1].alive = True
                # Cell on the bottom right
                if cell.x + 1 < self.cols and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x + 1].id == -1 \
                    and not self.board[cell.y + 1][cell.x + 1].alive:
                    self.new_grains.append(Cell(cell.x + 1, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x + 1].alive = True
                # Cell on the bottom
                if cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x].id == -1 \
                    and not self.board[cell.y + 1][cell.x].alive:
                    # Add new embryo
                    self.new_grains.append(Cell(cell.x, cell.y + 1, True, cell.id))
                    self.board[cell.y + 1][cell.x].alive = True
            self.add_new_grains(id)

    def pentagonal_random(self, border_cond=False):
        """
		Random pentagonal neighbourhood
		"""
        rand_num = randint(0, 10)
        if rand_num % 2:
            self.pentagonal_left(border_cond)
        else:
            self.pentagonal_right(border_cond)

    def random_embryo_loc(self, quantity):
        """
		Set random location of @quantity embryons
		"""
        print "Random embryos:"
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

    def linear_embryo_loc(self, quantity):
        """
		Set location of embryons with given offset
		"""
        offset = int(self.cols / quantity)
        k = 0
        for i in range(self.rows):
            for j in range(0, self.cols, offset):
                self.board[i][j].alive = True
                self.board[i][j].id = k
                self.board[i][j].x = j
                self.board[i][j].y = i
                self.starting_embryos_location[k] = list()
                self.starting_embryos_location[k].append(self.board[i][j])
                print "Added cell: {}".format(self.board[i][j])
                k += 1

    def radius_embryo_loc(self, radius):
        """
		Set location of embryons with given radius
		"""
        k = 0
        for i in range(0, self.rows, radius):
            for j in range(0, self.cols, radius):
                self.board[i][j].alive = True
                self.board[i][j].id = k
                self.board[i][j].x = j
                self.board[i][j].y = i
                self.starting_embryos_location[k] = list()
                self.starting_embryos_location[k].append(self.board[i][j])
                print "Added cell: {}".format(self.board[i][j])
                k += 1

    def mouse_embryo_loc(self, points):
        """
		Set location of embryons with mouse clicks
		"""
        for nr, (x, y) in enumerate(points):
            row = x
            col = y
            print row, col
            self.board[row][col].alive = True
            self.board[row][col].id = nr
            self.board[row][col].x = col
            self.board[row][col].y = row
            self.starting_embryos_location[nr] = list()
            self.starting_embryos_location[nr].append(self.board[row][col])
            print "Added cell: {}".format(self.board[row][col])

    def periodic_bc(self, cell):
        """
		Set periodic border conditions
		"""
        # Cell appears on the left
        if cell.x + 1 == self.cols and self.board[cell.y][0].id == -1 \
            and not self.board[cell.y][0].alive:
            # Add new embryo
            self.new_grains.append(Cell(0, cell.y, True, cell.id))
            self.board[cell.y][0].alive = True
        # Cell appears on the right
        if cell.x - 1 == 0 and self.board[cell.y][self.cols - 1].id == -1 \
            and not self.board[cell.y][self.cols - 1].alive:
            # Add new embryo
            self.new_grains.append(Cell(self.cols-1, cell.y, True, cell.id))
            self.board[cell.y][self.cols-1].alive = True
        # Cell appears on the top
        if cell.y + 1 == self.rows and self.board[0][cell.x].id == -1 \
            and not self.board[0][cell.x].alive:
            # Add new embryo
            self.new_grains.append(Cell(cell.x, 0, True, cell.id))
            self.board[0][cell.x].alive = True
        # Cell appears at the bottom
        if cell.y - 1 == 0 and self.board[self.rows - 1][cell.x].id == -1 \
            and not self.board[self.rows - 1][cell.x].alive:
            # Add new embryo
            self.new_grains.append(Cell(cell.x, self.rows - 1, True, cell.id))
            self.board[self.rows - 1][cell.x].alive = True


def update(grid):
    for i in range(grid.rows):
        for j in range(grid.cols):
            color = 'white'
            if grid.board[i][j].id == 0:
                color = 'red'
            elif grid.board[i][j].id == 1:
                color = 'blue'
            elif grid.board[i][j].id == 2:
                color = 'green'
            elif grid.board[i][j].id == 3:
                color = 'brown'
            elif grid.board[i][j].id == 4:
                color = 'cyan'
            elif grid.board[i][j].id == 5:
                color = 'orange'
            elif grid.board[i][j].id == 6:
                color = 'magenta'
            elif grid.board[i][j].id == 7:
                color = 'yellow'
            elif grid.board[i][j].id == 8:
                color = 'violet'
            cells[i][j].configure(background=color)
    grid.von_neuman()
    root.after(100, update, grid)


if __name__ == '__main__':
    root = Tkinter.Tk()
    r, c = 75, 75
    cells = [[0 for x in range(c)] for y in range(r)]
    grid = Grid(r, c)
    grid.random_embryo_loc(9)
    for i in range(grid.rows):
        for j in range(grid.cols):
            color = 'white'
            if grid.board[i][j].id == 0:
                color = 'red'
            elif grid.board[i][j].id == 1:
                color = 'blue'
            elif grid.board[i][j].id == 2:
                color = 'green'
            elif grid.board[i][j].id == 3:
                color = 'brown'
            elif grid.board[i][j].id == 4:
                color = 'cyan'
            elif grid.board[i][j].id == 5:
                color = 'orange'
            elif grid.board[i][j].id == 6:
                color = 'magenta'
            elif grid.board[i][j].id == 7:
                color = 'yellow'
            elif grid.board[i][j].id == 8:
                color = 'violet'
            cells[i][j] = Tkinter.Canvas(root, background=color, width=2, height=2, borderwidth=0)
            cells[i][j].grid(row=i, column=j)
    update(grid)
    root.mainloop()
