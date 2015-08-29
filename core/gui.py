import sys
from PyQt4 import QtGui, QtCore
from map import Map
from game_manager import GameManager

DIRECTIONS = {
    QtCore.Qt.Key_A: (0, -1),
    QtCore.Qt.Key_D: (0, 1),
    QtCore.Qt.Key_W: (-1, 0),
    QtCore.Qt.Key_S: (1, 0)
}

SPEED = 50

class MainWindow(QtGui.QMainWindow):
    def __init__(self, gm):
        super(MainWindow, self).__init__()
        self.board = Playground(gm)
        self.setCentralWidget(self.board)
        self.board.start()
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

class Playground(QtGui.QFrame):

    def __init__(self, gm):
        super(Playground, self).__init__()

        self.gm = gm
        self.height, self.width = gm.dimensions()
        self.direction = DIRECTIONS[QtCore.Qt.Key_D]
        self.timer = QtCore.QBasicTimer()
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
        for i in range(self.height):
            for j in range(self.width):
                button = QtGui.QPushButton(self.gm.symbol_at((i, j)))
                button.setMaximumSize(25, 25)
                button.setMinimumSize(25, 25)
                button.setFlat(True)
                self.grid.addWidget(button, i, j)

    def update_playground(self):
        for i in range(self.height):
            for j in range(self.width):
                button = self.grid.itemAtPosition(i, j).widget()
                button.setText(self.gm.symbol_at((i, j)))

    def keyPressEvent(self, event):
        if event.key() in DIRECTIONS:
            self.direction = DIRECTIONS.get(event.key(), self.direction)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.move_hero(self.direction):
                self.update_playground()
        else:
            QtGui.QWidget.timerEvent(event)

    def move_hero(self, position):
        return self.gm.move_hero(position)

    def start(self):
        self.timer.start(SPEED, self)

def main():
    m = Map('../maps/m2-o.txt')
    gm = GameManager(m)
    app = QtGui.QApplication(sys.argv)
    mn = MainWindow(gm)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
