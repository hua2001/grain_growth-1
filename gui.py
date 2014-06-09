# coding=utf-8
import os
import random
import sys
import ImageQt
import datetime
import numpy as np
# from threading import Thread
# import matplotlib.pyplot as plt
import time
from PyQt4 import QtCore, QtGui
from images2gif import writeGif
from PIL import Image
from gif_dialog import MoviePlayer
from grid import Grid
from utils import sorted_ls


class SimulationGUI(QtGui.QWidget):
    def __init__(self):
        super(SimulationGUI, self).__init__()
        self.scene = QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView(self.scene)
        self.grid = None
        self.mouse_cords = list()
        self.layout = QtGui.QHBoxLayout()

        self.simulation_button = QtGui.QPushButton('Start simulation')
        self.gif_button = QtGui.QPushButton('Load grain growth animation')
        self.gif_button.setDisabled(True)
        self.recrystallized_button = QtGui.QPushButton('Show recrystallization result')
        self.recrystallized_button.setDisabled(True)

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
        self.gif_button.clicked.connect(self.show_gif_animation)
        self.recrystallized_button.clicked.connect(self.display_recrystallized_img)

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
        self.layout.addWidget(self.view)
        self.vbox_layout = QtGui.QVBoxLayout()
        self.vbox_layout.addWidget(self.simulation_button)
        self.vbox_layout.addWidget(self.gif_button)
        self.vbox_layout.addWidget(self.recrystallized_button)
        self.vbox_layout.addWidget(self.rule_combo)
        self.vbox_layout.addWidget(self.location_combo)
        self.vbox_layout.addWidget(self.embryos_label)
        self.vbox_layout.addWidget(self.embryos_spin_box)
        self.vbox_layout.addWidget(self.rows_label)
        self.vbox_layout.addWidget(self.rows_spin_box)
        self.vbox_layout.addWidget(self.cols_label)
        self.vbox_layout.addWidget(self.cols_spin_box)
        self.vbox_layout.addWidget(self.bc_checkbox)
        self.layout.addLayout(self.vbox_layout)
        self.setLayout(self.layout)

    def mousePressEvent(self, QMouseEvent):
        mouse_pos =  QMouseEvent.pos()
        if self.location_combo.currentIndex() == 3 and \
            (0, 0) <= (mouse_pos.x(), mouse_pos.y()) < (self.view.frameSize().width(), self.view.frameSize().height()):
            self.mouse_cords.append((mouse_pos.x(), mouse_pos.y()))
            print 'Cursor positions x[{}] y[{}]'.format(mouse_pos.x(), mouse_pos.y())

    def update_label(self):
        # Not so pretty but it works
        if self.location_combo.currentIndex() == 1:
            self.embryos_label.setDisabled(False)
            self.embryos_spin_box.setDisabled(False)
            self.embryos_label.setText('Offset')
        elif self.location_combo.currentIndex() == 2:
            self.embryos_label.setDisabled(False)
            self.embryos_spin_box.setDisabled(False)
            self.embryos_label.setText('Radius')
        elif self.location_combo.currentIndex() == 3:
            self.scene.clear()
            self.view.resize(0, 0)
            self.rows_spin_box.valueChanged.connect(self.update_view_size)
            self.cols_spin_box.valueChanged.connect(self.update_view_size)
            self.embryos_label.setDisabled(True)
            self.embryos_spin_box.setDisabled(True)
        else:
            self.embryos_label.setDisabled(False)
            self.embryos_spin_box.setDisabled(False)
            self.embryos_label.setText('Number of starting embryons')

    def update_view_size(self):
        """
        Resizes QGraphicsView when point&click options is selected.
        """
        self.view.resize(self.rows_spin_box.value(), self.cols_spin_box.value())

    def simulation(self):
        """
        Don't touch this - it's magic!
        """
        enable_bc = False
        num_of_rows = self.rows_spin_box.value()
        num_of_cols = self.cols_spin_box.value()

        self.grid = Grid(num_of_rows, num_of_cols)
        num_of_embryos = self.embryos_spin_box.value()
        if self.location_combo.currentIndex() == 0:
            self.grid.random_embryo_loc(num_of_embryos)
        elif self.location_combo.currentIndex() == 1:
            self.grid.linear_embryo_loc(num_of_embryos)
        elif self.location_combo.currentIndex() == 2:
            self.grid.radius_embryo_loc(num_of_embryos)
        else:
            self.grid.mouse_embryo_loc(self.mouse_cords)
            self.mouse_cords = list()

        if self.bc_checkbox.isChecked():
            enable_bc = True

        self.RGB_dict = self.generate_RGB_dict()
        self.starting_embryos = self.grid.starting_embryos_location.copy()
        self.iteration_counter = 0
        while(not self.grid.is_full()):
            if self.rule_combo.currentIndex() == 0:
                self.grid.moore(enable_bc)
            elif self.rule_combo.currentIndex() == 1:
                self.grid.von_neuman(enable_bc)
            elif self.rule_combo.currentIndex() == 2:
                self.grid.hexagonal_left(enable_bc)
            elif self.rule_combo.currentIndex() == 3:
                self.grid.hexagonal_right(enable_bc)
            elif self.rule_combo.currentIndex() == 4:
                self.grid.hexagonal_random(enable_bc)
            else:
                self.grid.hexagonal_random(enable_bc)
            self.iteration_counter += 1
        self.create_grains_img()
        self.display_grains_img()
        self.grid.find_edged_grains()
        # for cell in self.grid.edged_grains:
        #     print cell
        print self.iteration_counter
        self.gif_button.setDisabled(False)
        self.recrystallized_button.setDisabled(False)

    def display_grains_img(self):
        """
        Simply displays final form of grain growth process in main window.
        """
        self.scene.clear()
        img = Image.open('grains.png')
        width, height = img.size
        self.imgQ = ImageQt.ImageQt(img)
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)
        self.view.fitInView(QtCore.QRectF(0, 0, width, height))#    , QtCore.Qt.KeepAspectRatio)
        self.scene.update()

    def display_recrystallized_img(self):
        """
        Simply displays final form of grain growth process in main window.
        """
        self.scene.clear()
        img = Image.open('grains2.png')
        width, height = img.size
        self.imgQ = ImageQt.ImageQt(img)
        pixMap = QtGui.QPixmap.fromImage(self.imgQ)
        self.scene.addPixmap(pixMap)
        self.view.fitInView(QtCore.QRectF(0, 0, width, height))#    , QtCore.Qt.KeepAspectRatio)
        self.scene.update()

    def _create_grains_img(self, counter):
        """
        Create .png file from numpy array which will be used to
        generate gif animation showing grain growth over time.
        """
        self.animated_grid.find_edged_grains()
        img_array = np.zeros((self.animated_grid.rows, self.animated_grid.cols, 3), dtype=np.uint8)
        for i in range(self.animated_grid.rows):
            for j in range(self.animated_grid.cols):
                img_array[i, j] = self.RGB_dict[self.animated_grid.board[i][j].id]
        img = Image.fromarray(img_array, 'RGB')
        img_filename = 'grains{}.png'.format(counter)
        img.save(os.path.join(self.dirname, img_filename))

    def generate_gif_frames(self):
        """
        Uses _create_grains_img method to generate .png files which will be used to
        create gif file.
        """
        self.dirname = self.create_frames_dir()

        if self.bc_checkbox.isChecked():
            enable_bc = True
        else:
            enable_bc = False

        num_of_rows = self.rows_spin_box.value()
        num_of_cols = self.cols_spin_box.value()

        self.animated_grid = Grid(num_of_rows, num_of_cols)
        self.animated_grid.starting_embryos_location = self.starting_embryos
        counter = 0
        while(not self.animated_grid.is_full()):
            self._create_grains_img(counter)
            if self.rule_combo.currentIndex() == 0:
                self.animated_grid.moore(enable_bc)
            elif self.rule_combo.currentIndex() == 1:
                self.animated_grid.von_neuman(enable_bc)
            elif self.rule_combo.currentIndex() == 2:
                self.animated_grid.hexagonal_left(enable_bc)
            elif self.rule_combo.currentIndex() == 3:
                self.animated_grid.hexagonal_right(enable_bc)
            elif self.rule_combo.currentIndex() == 4:
                self.animated_grid.hexagonal_random(enable_bc)
            else:
                self.animated_grid.hexagonal_random(enable_bc)
            counter += 1
        print counter
        # don't forget about final gif frame
        self._create_grains_img(counter+1)

    def create_grains_img(self):
        """
        Creates a .png file which contains final state of grains growth process.
        """
        img_array = np.zeros((self.grid.rows, self.grid.cols, 3), dtype=np.uint8)
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                img_array[i, j] = self.RGB_dict[self.grid.board[i][j].id]
        img = Image.fromarray(img_array, 'RGB')
        img.save('grains.png')

        self.grid.find_edged_grains()
        print 'ilosc krawedziowych', len(self.grid.edged_grains)
        while(self.grid.time <= 1):
            self.grid.assign_dyslocations()
            for i in range(self.grid.rows):
                for j in range(self.grid.cols):
                    if self.grid.critical_dyslocation_density <= self.grid.board[i][j].dislocations_quantity:
                        self.grid.transition_rule(self.grid.board[i][j])
                        try:
                            self.RGB_dict[self.grid.board[i][j].id]
                        except:
                            self.RGB_dict[self.grid.board[i][j].id] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
                        img_array[self.grid.board[i][j].y, self.grid.board[i][j].x] = self.RGB_dict[self.grid.board[i][j].id]
        img = Image.fromarray(img_array, 'RGB')
        img.save('grains2.png')

    def generate_RGB_dict(self):
        """
        Creates dictionary where key is a cell's id and value is a RGB value.
        Used to determine which colour should be used for a particular cell
        when creating a .png file.
        """
        RGB_dict = dict()
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                cell = self.grid.board[i][j]
                if cell.id == -1:
                    RGB_dict[cell.id] = [255, 255, 255]
                else:
                    RGB_dict[cell.id] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        return RGB_dict

    def create_frames_dir(self):
        """
        Create directory containing images representing steps of grain growth.
        """
        dirname = 'grain_growth_{}'.format(datetime.datetime.now())
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return dirname

    def show_gif_animation(self):
        """
        Generates animation of grain growth process and displays in dialog window.
        """
        self.generate_gif_frames()
        file_names = sorted_ls(self.dirname)
        images = [Image.open(os.path.join(self.dirname, fn)) for fn in file_names]

        size = (self.animated_grid.rows, self.animated_grid.cols)
        for im in images:
            im.thumbnail(size, Image.ANTIALIAS)

        filename = os.path.join(self.dirname, 'animated_grain_growth.gif')
        writeGif(filename, images, duration=0.2)
        player = MoviePlayer(self)
        player.start(filename)
        player.exec_()
        self.gif_button.setDisabled(True)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    f = SimulationGUI()
    f.resize(800, 600)
    f.setWindowTitle('Grain growth simulation')
    f.show()
    sys.exit(app.exec_())
