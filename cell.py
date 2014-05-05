__author__ = 'steman'


class Cell(object):
    def __init__(self, x, y, alive=False, id=-1):
        self.alive = alive
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return 'Cell id:{} alive:{} x:{} y:{}'.format(self.id, self.alive, self.x, self.y)