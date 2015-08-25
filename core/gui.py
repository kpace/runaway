import sys
from PyQt4 import QtGui, QtCore
from map import Map
from cells import Position
from game_manager import GameManager
import timeit

DIRECTIONS = {
    QtCore.Qt.Key_A: Position(0, -1),
    QtCore.Qt.Key_D: Position(0, 1),
    QtCore.Qt.Key_W: Position(-1, 0),
    QtCore.Qt.Key_S: Position(1, 0)
}

SPEED = 100

class MainWindow(QtGui.QMainWindow):
    def __init__(self, map):
        super(MainWindow, self).__init__()
        self.board = Board(map)
        self.setCentralWidget(self.board)
        self.board.start()
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

class Board(QtGui.QFrame):

    def __init__(self, map):
        super(Board, self).__init__()

        self.map = map
        self.hero_position = map.get_hero().position
        self.direction = DIRECTIONS[QtCore.Qt.Key_D]
        self.timer = QtCore.QBasicTimer()
        self.gm = GameManager(self.map)
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(0)
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.grid)
        self.draw()

        self.move(300, 150)
        self.setWindowTitle('Runaway')
        self.show()

    def draw(self):
        for i in range(self.map.height):
            for j in range(self.map.width):
                position_obj = Position(i, j)
                button = QtGui.QPushButton(self.map[position_obj].symbol)
                button.setMaximumSize(30, 30)
                button.setMinimumSize(30, 30)
                # button.setFlat(True)
                self.grid.addWidget(button, i, j)

    def draw_symbols(self):
        for i in range(self.map.height):
            for j in range(self.map.width):
                position_obj = Position(i, j)
                button = self.grid.itemAtPosition(i, j).widget()
                button.setText(self.map[position_obj].symbol)

    def keyPressEvent(self, event):
        if event.key() in DIRECTIONS:
            self.direction = DIRECTIONS.get(event.key(), self.direction)

    def timerEvent(self, event):
        t1 = timeit.default_timer()
        if event.timerId() == self.timer.timerId():
            self.move_hero(self.direction)
            self.draw_symbols()
            # self.update()
        else:
            QtGui.QWidget.timerEvent(event)

    def move_hero(self, position):
        h_pos = self.hero_position
        n_pos = self.hero_position + position
        self.gm.move_hero(position)
        # if self.gm.move_hero(position):
            # self.update()

    # def paintEvent(self, QPaintEvent):
    #     h_button = QtGui.QPushButton(self.map.get_hero().symbol)
    #     h_button.setMaximumSize(30, 30)
    #     h_button.setMinimumSize(30, 30)
    #     n_button = QtGui.QPushButton(self.map[n_pos].symbol)
    #     n_button.setMaximumSize(30, 30)
    #     n_button.setMinimumSize(30, 30)
    #
    #     self.grid.addWidget(h_button, n_pos.i, n_pos.j)
    #     self.grid.addWidget(n_button, h_pos.i, h_pos.j)

    def start(self):
        self.timer.start(SPEED, self)

def main():
    m = Map('../maps/m2.txt')
    app = QtGui.QApplication(sys.argv)
    mn = MainWindow(m)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
