import random
import time

__author__ = 'steman'
import sys
import ImageQt
from PIL import Image
from PyQt4 import QtCore, QtGui
import numpy as np
from grid import Grid

class Foo(QtGui.QWidget):
    def __init__(self):
        super(Foo, self).__init__()
        self.scene = QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView(self.scene)
        self.grid = None
        self.mouse_cords = list()
        self.box_layout = QtGui.QVBoxLayout()
        self.simulation_button = QtGui.QPushButton('Start simulation')

        self.rule_combo = QtGui.QComboBox()
        self.location_combo = QtGui.QComboBox()
        self.embryos_spin_box = QtGui.QSpinBox()
        self.rows_spin_box = QtGui.QSpinBox()
        self.cols_spin_box = QtGui.QSpinBox()

        self.embryos_label = QtGui.QLabel('Number of starting embryons')
        self.rows_label = QtGui.QLabel('Number of rows')
        self.cols_label = QtGui.QLabel('Number of collumns')

        self.init_combo_boxes()
        self.init_spin_boxes()

        self.bc_checkbox = QtGui.QCheckBox('Enable periodic border conditions')

        self.init_layout()

        self.simulation_button.clicked.connect(self.simulation)


    def init_combo_boxes(self):
        rules = ['Moore', 'Von Neumann', 'Hexagonal left', 'Hexagonal right', 'Random hexagonal', 'Random pentagonal']
        locations = ['Random loc.', 'Linear loc.', 'Radius loc.', 'Point & click']
        self.rule_combo.addItems(rules)
        self.location_combo.addItems(locations)
        self.location_combo.currentIndexChanged.connect(self.update_label)


    def init_spin_boxes(self):
        self.rows_spin_box.setMaximum(1331)
        self.cols_spin_box.setMaximum(999)
        self.embryos_spin_box.setMaximum(255)



    def init_layout(self):
        self.box_layout.addWidget(self.view)
        self.hbox_layout = QtGui.QHBoxLayout()
        self.hbox_layout.addWidget(self.simulation_button)
        self.hbox_layout.addWidget(self.rule_combo)
        self.hbox_layout.addWidget(self.location_combo)
        self.hbox_layout.addWidget(self.embryos_label)
        self.hbox_layout.addWidget(self.embryos_spin_box)
        self.hbox_layout.addWidget(self.rows_label)
        self.hbox_layout.addWidget(self.rows_spin_box)
        self.hbox_layout.addWidget(self.cols_label)
        self.hbox_layout.addWidget(self.cols_spin_box)
        self.hbox_layout.addWidget(self.bc_checkbox)
        self.box_layout.addLayout(self.hbox_layout)
        self.setLayout(self.box_layout)


    def mousePressEvent(self, QMouseEvent):
        mouse_pos =  QMouseEvent.pos()
        if self.location_combo.currentIndex() == 3 and \
            (0, 0) <= (mouse_pos.x(), mouse_pos.y()) < (self.view.frameSize().width(), self.view.frameSize().height()):
            self.mouse_cords.append((mouse_pos.x(), mouse_pos.y()))
            print (mouse_pos.x(), mouse_pos.y())


    def update_label(self):
        # Not so pretty but it works
        if self.location_combo.currentIndex() == 1:
            self.embryos_label.setDisabled(False)
            self.embryos_spin_box.setDisabled(False)
            self.embryos_label.setText('Offset')
        elif self.location_combo.currentIndex() == 3:
            self.rows_spin_box.valueChanged.connect(self.update_view_size)
            self.cols_spin_box.valueChanged.connect(self.update_view_size)
            self.embryos_label.setDisabled(True)
            self.embryos_spin_box.setDisabled(True)
        else:
            self.embryos_label.setDisabled(False)
            self.embryos_spin_box.setDisabled(False)
            self.embryos_label.setText('Number of starting embryons')

    def update_view_size(self):
        self.view.resize(self.rows_spin_box.value(), self.cols_spin_box.value())

    def simulation(self):
        print self.mouse_cords
        num_of_rows = self.rows_spin_box.value()
        num_of_cols = self.cols_spin_box.value()
        # self.view.resize(num_of_rows, num_of_cols)

        self.grid = Grid(num_of_rows, num_of_cols)
        num_of_embryos = self.embryos_spin_box.value()

        if self.location_combo.currentIndex() == 0:
            self.grid.random_embryo_loc(num_of_embryos)
        elif self.location_combo.currentIndex() == 1:
            self.grid.linear_embryo_loc(num_of_embryos)
        elif self.location_combo.currentIndex() == 2:
            self.grid.radius_embryo_loc(num_of_embryos)
        else:
            self.grid.mouse_embyro_loc(self.mouse_cords)
            self.mouse_cords = list()

        if self.bc_checkbox.isChecked():
            self.grid.periodic_bc()

        while(not self.grid.full()):
            if self.rule_combo.currentIndex() == 0:
                self.grid.moore()
            elif self.rule_combo.currentIndex() == 1:
                self.grid.von_neuman()
            elif self.rule_combo.currentIndex() == 2:
                self.grid.hexagonal_left()
            elif self.rule_combo.currentIndex() == 3:
                self.grid.hexagonal_right()
            elif self.rule_combo.currentIndex() == 4:
                self.grid.hexagonal_random()
            else:
                self.grid.hexagonal_random()
        self.create_grains_img()
        self.display_grains_img()

    def display_grains_img(self):
        self.scene.clear()
        img = Image.open('grains.png')
        width, height = img.size
        self.imgQ = ImageQt.ImageQt(img)
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)
        self.view.fitInView(QtCore.QRectF(0, 0, width, height))#, QtCore.Qt.KeepAspectRatio)
        self.scene.update()

    def create_grains_img(self):
        RGB_dict = self.generate_RGB_dict()
        img_array = np.zeros((self.grid.rows, self.grid.cols, 3), dtype=np.uint8)
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                img_array[i, j] = RGB_dict[self.grid.board[i][j].id]
        img = Image.fromarray(img_array, 'RGB')
        img.save('grains.png')

    def generate_RGB_dict(self):
        RGB_dict = dict()
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                cell = self.grid.board[i][j]
                RGB_dict[cell.id] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        return RGB_dict


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    f = Foo()
    f.resize(800, 600)
    f.show()
    sys.exit(app.exec_())
