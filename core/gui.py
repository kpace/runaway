import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from map import Map
from game_manager import GameManager

DIRECTIONS = {
    QtCore.Qt.Key_A: (0, -1),
    QtCore.Qt.Key_D: (0, 1),
    QtCore.Qt.Key_W: (-1, 0),
    QtCore.Qt.Key_S: (1, 0)
}

SPEED = 200
CELL_SIZE = 20

class CellGui(QtGui.QLabel):

    def __init__(self, symbol, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(CELL_SIZE, CELL_SIZE)
        self.setProperty('symbol', symbol)

    def set_style(self, symbol):
        self.setProperty('symbol', symbol)
        self.setStyleSheet(
            """
            QLabel[symbol='#'] {
                background-color: blue;
            }
            QLabel[symbol='H']{
                background-color: black;
            }
            QLabel[symbol='$']{
                background-color: red;
            }
            """
        )

class Playground(QtGui.QFrame):

    def __init__(self, gm, *args, **kwargs):
        super(Playground, self).__init__(*args, **kwargs)

        self.gm = gm
        self.height, self.width = gm.dimensions()
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
                cell = CellGui(self.gm.cell_at((i, j)).symbol)
                self.grid.addWidget(cell, i, j)

    def update_playground(self):
        for i in range(self.height):
            for j in range(self.width):
                cell = self.grid.itemAtPosition(i, j).widget()
                # TODO: Refactor...
                cell.set_style(self.gm.cell_at((i, j)).symbol)

    def keyPressEvent(self, event):
        if event.key() in DIRECTIONS:
            self.gm.set_direction(DIRECTIONS.get(event.key()))
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.gm.move_cells()
            if self.gm.game_over:
                    QMessageBox.information(self, 'Game Over', ':( :( :(')
                    sys.exit()
            self.update_playground()
        else:
            QtGui.QWidget.timerEvent(event)

    def start(self):
        self.timer.start(SPEED, self)

def main():
    m = Map('../maps/m1.txt')
    gm = GameManager(m, DIRECTIONS[QtCore.Qt.Key_D])
    app = QtGui.QApplication(sys.argv)
    playground = Playground(gm)
    playground.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
