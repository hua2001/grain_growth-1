__author__ = 'steman'
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MoviePlayer(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle('Grain growth progress')
        self.movie_screen = QLabel()
        # expand and center the label
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding,
                                        QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        btn_start = QPushButton("Start Animation")
        self.connect(btn_start, SIGNAL("clicked()"), self.start)
        btn_stop = QPushButton("Stop Animation")
        self.connect(btn_stop, SIGNAL("clicked()"), self.stop)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        main_layout.addWidget(btn_start)
        main_layout.addWidget(btn_stop)
        self.setLayout(main_layout)

    def start(self, *args):
        if args:
            self.gif_path = args[0]
        self.movie = QMovie(self.gif_path, QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()

    def stop(self):
        self.movie.stop()

