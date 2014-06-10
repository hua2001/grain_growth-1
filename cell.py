__author__ = 'steman'


class Cell(object):
    def __init__(self, x, y, alive=False, id=-1):
        self.alive = alive
        self.id = id
        self.x = x
        self.y = y
        self.dislocations_quantity = 0
        self.recrystallized = 0
        self.total_energy = 0
        self.environment = list()
        self.visited = False

    def __str__(self):
        return 'Cell id:{} alive:{} x:{} y:{}'.format(self.id, self.alive, self.x, self.y)

    def __gt__(self, other):
        return self.id > other.id