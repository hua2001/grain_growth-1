# coding=utf-8
import math
import time

__author__ = 'steman'
import Tkinter
from random import randint, random, shuffle
from math import sqrt, pow
from cell import Cell

A = 86710969050178.5
B = 9.41268203527779

current_ro = lambda t: A/B + (1 - A/B) * math.exp(-B*t)

edge_dislocation = lambda: randint(100, 120)/float(100)
grain_dislocation = lambda: randint(10, 30)/float(100)

class Grid(object):
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[Cell(x, y) for x in range(cols)] for y in range(rows)]
        self.starting_embryos_location = dict()
        self.new_grains = list()
        self.time = 0
        self.ro = 86710969050178.5
        self.sigma = 9.41268203527779
        self.critical_dyslocation_density = 4215840142323.42 / (self.rows * self.cols)
        self.prev_ro = self.ro
        self.edged_grains = []

    def is_full(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j].id == -1:
                    return False
        return True

    def all_visited(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.board[i][j].visited:
                    return False
        return True

    def find_edged_grains(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if not cell in self.edged_grains:
                    # Cell on the top left
                    if cell.x - 1 >= 0 and cell.y - 1 >= 0 and (self.board[cell.y - 1][cell.x - 1].id != -1
                        and self.board[cell.y - 1][cell.x - 1].id != cell.id):
                        self.edged_grains.append(cell)
                    # Cell on the top right
                    elif cell.x + 1 < self.cols and cell.y - 1 >= 0 and (self.board[cell.y - 1][cell.x + 1].id != -1
                        and self.board[cell.y - 1][cell.x + 1].id != cell.id):
                        self.edged_grains.append(cell)
                    # Cell on the bottom left
                    elif cell.x - 1 >= 0 and cell.y + 1 < self.rows and (self.board[cell.y + 1][cell.x - 1].id != -1
                        and self.board[cell.y + 1][cell.x - 1].id != cell.id):
                        self.edged_grains.append(cell)
                    # Cell on the bottom right
                    elif cell.x + 1 < self.cols and cell.y + 1 < self.rows and (self.board[cell.y + 1][cell.x + 1].id != -1
                        and self.board[cell.y + 1][cell.x + 1].id != cell.id):
                        self.edged_grains.append(cell)
                    # Cell on the right
                    elif cell.x + 1 < self.cols and (self.board[cell.y][cell.x + 1].id != -1
                        and self.board[cell.y][cell.x + 1].id != cell.id):
                        # Add new embryo
                        self.edged_grains.append(cell)
                    # Cell on the left
                    elif cell.x - 1 >= 0 and (self.board[cell.y][cell.x - 1].id != -1
                        and self.board[cell.y][cell.x - 1].id != cell.id):
                        # Add new embryo
                        self.edged_grains.append(cell)
                    # Cell on the bottom
                    elif cell.y + 1 < self.rows and (self.board[cell.y + 1][cell.x].id != -1
                        and self.board[cell.y + 1][cell.x].id != cell.id):
                        # Add new embryo
                        self.edged_grains.append(cell)
                    # Cell on the top
                    elif cell.y - 1 >= 0 and (self.board[cell.y - 1][cell.x].id != -1
                        and self.board[cell.y - 1][cell.x].id != cell.id):
                        # Add new embryo
                        self.edged_grains.append(cell)
                    else:
                        pass

    def sum_up_dislocations(self, cell):
        dislocations_sum = 0
        # Cell on the top left
        if cell.x - 1 >= 0 and cell.y - 1 >= 0:
            dislocations_sum += self.board[cell.y - 1][cell.x - 1].dislocations_quantity
        # Cell on the top right
        if cell.x + 1 < self.cols and cell.y - 1 >= 0:
            dislocations_sum += self.board[cell.y - 1][cell.x + 1].dislocations_quantity
        # Cell on the bottom left
        if cell.x - 1 >= 0 and cell.y + 1 < self.rows:
            dislocations_sum += self.board[cell.y + 1][cell.x - 1].dislocations_quantity
        # Cell on the bottom right
        if cell.x + 1 < self.cols and cell.y + 1 < self.rows:
            dislocations_sum += self.board[cell.y + 1][cell.x + 1].dislocations_quantity
        # Cell on the right
        if cell.x + 1 < self.cols:
            dislocations_sum += self.board[cell.y][cell.x + 1].dislocations_quantity
        # Cell on the left
        if cell.x - 1 >= 0:
            dislocations_sum += self.board[cell.y][cell.x - 1].dislocations_quantity
        # Cell on the bottom
        if cell.y + 1 < self.rows:
            dislocations_sum += self.board[cell.y + 1][cell.x].dislocations_quantity
        # Cell on the top
        if cell.y - 1 >= 0:
            dislocations_sum += self.board[cell.y - 1][cell.x].dislocations_quantity
        return dislocations_sum

    def transition_rule(self, cell):
        # Cell on the top left
        # if cell.x - 1 >= 0 and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x - 1].recrystallized:
        #     print 'Lewy top'
        #     cell.recrystallized = 1
        #     cell.id = self.board[cell.y - 1][cell.x - 1].id
        #     cell.dislocations_quantity = self.ro
        #     if cell.dislocations_quantity >= self.sum_up_dislocations(cell):
        #         print '{} {}'.format(cell.dislocations_quantity, self.sum_up_dislocations(cell))
        # # Cell on the top right
        # elif cell.x + 1 < self.cols and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x + 1].recrystallized:
        #     print 'prawy top'
        #     cell.recrystallized = 1
        #     cell.id = self.board[cell.y - 1][cell.x + 1].id
        #     cell.dislocations_quantity = self.ro
        #     if cell.dislocations_quantity >= self.sum_up_dislocations(cell):
        #         print '{} {}'.format(cell.dislocations_quantity, self.sum_up_dislocations(cell))
        # # Cell on the bottom left
        # elif cell.x - 1 >= 0 and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x - 1].recrystallized:
        #     print 'lewy bot'
        #     cell.recrystallized = 1
        #     cell.id = self.board[cell.y + 1][cell.x - 1].id
        #     cell.dislocations_quantity = self.ro
        #     if cell.dislocations_quantity >= self.sum_up_dislocations(cell):
        #         print '{} {}'.format(cell.dislocations_quantity, self.sum_up_dislocations(cell))
        # # Cell on the bottom right
        # elif cell.x + 1 < self.cols and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x + 1].recrystallized:
        #     print 'prawy bot'
        #     cell.recrystallized = 1
        #     cell.id = self.board[cell.y + 1][cell.x + 1].id
        #     cell.dislocations_quantity = self.ro
        #     if cell.dislocations_quantity >= self.sum_up_dislocations(cell):
        #         print '{} {}'.format(cell.dislocations_quantity, self.sum_up_dislocations(cell))

        # Cell on the right
        # print '{} <=> {}'.format(cell.dislocations_quantity, self.sum_up_dislocations(cell))
        if cell.x + 1 < self.cols and self.board[cell.y][cell.x + 1].recrystallized:
            print 'prawa'
            cell.id = self.board[cell.y][cell.x + 1].id
            cell.recrystallized = 1
            cell.dislocations_quantity = self.ro
            self.new_grains.append(cell)
            # self.edged_grains.append(self.board[cell.y][cell.x + 1])
            if cell.dislocations_quantity >= self.sum_up_dislocations(cell):
                print '{} {}'.format(cell.dislocations_quantity, self.sum_up_dislocations(cell))
        # Cell on the left
        elif cell.x - 1 >= 0 and self.board[cell.y][cell.x - 1].recrystallized:
            print 'lewy'
            cell.id = self.board[cell.y][cell.x - 1].id
            cell.recrystallized = 1
            cell.dislocations_quantity = self.ro
            self.new_grains.append(cell)
            # self.edged_grains.append(self.board[cell.y][cell.x - 1])
            if cell.dislocations_quantity >= self.sum_up_dislocations(cell):
                print '{} {}'.format(cell.dislocations_quantity, self.sum_up_dislocations(cell))
        # Cell on the bottom
        elif cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x].recrystallized:
            print 'bot'
            cell.id = self.board[cell.y + 1][cell.x].id
            cell.recrystallized = 1
            cell.dislocations_quantity = self.ro
            self.new_grains.append(cell)
            # self.edged_grains.append(self.board[cell.y + 1][cell.x])
            if cell.dislocations_quantity >= self.sum_up_dislocations(cell):
                print '{} {}'.format(cell.dislocations_quantity, self.sum_up_dislocations(cell))
        # Cell on the top
        elif cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x].recrystallized:
            print 'top'
            cell.id = self.board[cell.y - 1][cell.x].id
            cell.recrystallized = 1
            cell.dislocations_quantity = self.ro
            self.new_grains.append(cell)
            # self.edged_grains.append(self.board[cell.y - 1][cell.x])
            if cell.dislocations_quantity >= self.sum_up_dislocations(cell):
                print '{} {}'.format(cell.dislocations_quantity, self.sum_up_dislocations(cell))
        else:
            cell.recrystallized = 1
            cell.dislocations_quantity = self.ro
            cell.id = max(max(c[1:]) for c in self.board).id + 1
            self.board[cell.y][cell.x].id = cell.id
            self.new_grains.append(cell)
            print '===============>', cell.id
        # return self.edged_grains.pop(self.edged_grains.index(cell))

    def assign_dyslocations(self):
        if self.time:
            ro = current_ro(self.time) - current_ro(self.time - 0.001)
        else:
            ro = current_ro(self.time)
        self.time += 0.001
        tmp = ro
        ro = ro / (self.rows * self.cols)

        for cell in self.edged_grains:
            cell.dislocations_quantity += edge_dislocation() * ro
            tmp -= cell.dislocations_quantity

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if not cell in self.edged_grains and tmp:
                    cell.dislocations_quantity += grain_dislocation() * ro
                    tmp -= cell.dislocations_quantity

        while(tmp > 0):
            rand_row = randint(0, self.rows-1)
            rand_col = randint(0, self.cols-1)
            gift = tmp / (self.rows * self.cols)
            self.board[rand_row][rand_col].dislocations_quantity += gift
            tmp -= self.board[rand_row][rand_col].dislocations_quantity

    def add_new_grains(self, id):
        try:
            del self.starting_embryos_location[id]
        except KeyError as ke:
            print ke
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
                # if cell.x + 1 < self.cols and self.board[cell.y][cell.x + 1].id == -1 \
                if cell.x + 1 < self.cols and not self.board[cell.y][cell.x + 1].alive:
                    new_cell = Cell(cell.x + 1, cell.y, True, cell.id)
                    self.new_grains.append(new_cell)
                    self.board[cell.y][cell.x + 1].alive = True
                # Cell on the left
                if cell.x - 1 >= 0 and not self.board[cell.y][cell.x - 1].alive:
                    new_cell = Cell(cell.x - 1, cell.y, True, cell.id)
                    self.new_grains.append(new_cell)
                    self.board[cell.y][cell.x - 1].alive = True
                # Cell on the bottom
                if cell.y + 1 < self.rows and not self.board[cell.y + 1][cell.x].alive:
                    new_cell = Cell(cell.x, cell.y + 1, True, cell.id)
                    self.new_grains.append(new_cell)
                    self.board[cell.y + 1][cell.x].alive = True
                # Cell on the top
                if cell.y - 1 >= 0 and not self.board[cell.y - 1][cell.x].alive:
                    new_cell = Cell(cell.x, cell.y - 1, True, cell.id)
                    self.new_grains.append(new_cell)
                    self.board[cell.y - 1][cell.x].alive = True
            self.add_new_grains(id)

    def von_neuman2(self, cell, border_cond=False):
        """
		Von Neuman neighbourhood
		"""
        # Cell on the right
        if border_cond:
            self.periodic_bc(cell)
        if cell.x + 1 < self.cols and not self.board[cell.y][cell.x + 1].alive:
            new_cell = Cell(cell.x + 1, cell.y, True, cell.id)
            self.new_grains.append(new_cell)
            self.board[cell.y][cell.x + 1].alive = True
        # Cell on the left
        if cell.x - 1 >= 0 and not self.board[cell.y][cell.x - 1].alive:
            new_cell = Cell(cell.x - 1, cell.y, True, cell.id)
            self.new_grains.append(new_cell)
            self.board[cell.y][cell.x - 1].alive = True
        # Cell on the bottom
        if cell.y + 1 < self.rows and not self.board[cell.y + 1][cell.x].alive:
            new_cell = Cell(cell.x, cell.y + 1, True, cell.id)
            self.new_grains.append(new_cell)
            self.board[cell.y + 1][cell.x].alive = True
        # Cell on the top
        if cell.y - 1 >= 0 and not self.board[cell.y - 1][cell.x].alive:
            new_cell = Cell(cell.x, cell.y - 1, True, cell.id)
            self.new_grains.append(new_cell)
            self.board[cell.y - 1][cell.x].alive = True
        self.add_new_grains(cell.id)

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
        for i in range(0, self.rows, offset):
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

    def shuffle_grid(self):
        # losowo zageszczona siatka
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j].id = randint(0, 50)

    def cell_energy(self, cell):
        energy = 0
        # Cell on the top left
        if cell.x - 1 >= 0 and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x - 1].id != cell.id:
            energy += 1
        # Cell on the top right
        if cell.x + 1 < self.cols and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x + 1].id != cell.id:
            energy += 1
        # Cell on the bottom left
        if cell.x - 1 >= 0 and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x - 1].id != cell.id:
            energy += 1
        # Cell on the bottom right
        if cell.x + 1 < self.cols and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x + 1].id != cell.id:
            energy += 1
        # Cell on the right
        if cell.x + 1 < self.cols and self.board[cell.y][cell.x + 1].id != cell.id:
            energy += 1
        # Cell on the left
        if cell.x - 1 >= 0 and self.board[cell.y][cell.x - 1].id != cell.id:
            energy += 1
        # Cell on the bottom
        if cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x].id != cell.id:
            energy += 1
        # Cell on the top
        if cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x].id != cell.id:
            energy += 1
        return energy

    def environment_states(self, cell):
        if cell.x - 1 >= 0 and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x - 1].id != cell.id \
            and not self.board[cell.y - 1][cell.x - 1].id in cell.environment:
            cell.environment.append(self.board[cell.y - 1][cell.x - 1].id)
        # Cell on the top right
        if cell.x + 1 < self.cols and cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x + 1].id != cell.id \
            and not self.board[cell.y - 1][cell.x + 1].id in cell.environment:
            cell.environment.append(self.board[cell.y - 1][cell.x + 1].id)
        # Cell on the bottom left
        if cell.x - 1 >= 0 and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x - 1].id != cell.id \
            and not self.board[cell.y + 1][cell.x - 1].id in cell.environment:
            cell.environment.append(self.board[cell.y + 1][cell.x - 1].id)
        # Cell on the bottom right
        if cell.x + 1 < self.cols and cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x + 1].id != cell.id \
            and not self.board[cell.y + 1][cell.x + 1].id in cell.environment:
            cell.environment.append(self.board[cell.y + 1][cell.x + 1].id)
        # Cell on the right
        if cell.x + 1 < self.cols and self.board[cell.y][cell.x + 1].id != cell.id \
            and not self.board[cell.y][cell.x + 1].id in cell.environment:
            cell.environment.append(self.board[cell.y][cell.x + 1].id)
        # Cell on the left
        if cell.x - 1 >= 0 and self.board[cell.y][cell.x - 1].id != cell.id \
            and not self.board[cell.y][cell.x - 1].id in cell.environment:
            cell.environment.append(self.board[cell.y][cell.x - 1].id)
        # Cell on the bottom
        if cell.y + 1 < self.rows and self.board[cell.y + 1][cell.x].id != cell.id \
            and not self.board[cell.y + 1][cell.x].id in cell.environment:
            cell.environment.append(self.board[cell.y + 1][cell.x].id)
        # Cell on the top
        if cell.y - 1 >= 0 and self.board[cell.y - 1][cell.x].id != cell.id \
            and not self.board[cell.y - 1][cell.x].id in cell.environment:
            cell.environment.append(self.board[cell.y - 1][cell.x].id)

    def monte_carlo(self):
        elements = list()
        for i in range(self.rows):
            for j in range(self.cols):
                elements.append(self.board[i][j])

        shuffle(elements)
        # print 'ilosc', len(elements)
        for element in elements:
            # print "wylosowana", element
            self.environment_states(element)
            # print "otoczenie", element.environment
            energy = self.cell_energy(element)
            # print "obecna energia", energy
            prev_state = element.id
            new_state = element.environment[randint(0, len(element.environment)-1)]
            element.id = new_state
            if energy < self.cell_energy(element):
                element.id = prev_state
                # print 'odrzucono'
            element.visited = True





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
    r, c = 10, 10
    cells = [[0 for x in range(c)] for y in range(r)]
    grid = Grid(r, c)
    # grid.random_embryo_loc(9)
    grid.linear_embryo_loc(9)
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
            cells[i][j] = Tkinter.Canvas(root, background=color, width=10, height=10, borderwidth=0)
            cells[i][j].grid(row=i, column=j)
    update(grid)
    root.mainloop()
