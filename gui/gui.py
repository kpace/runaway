import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from core.map import Map
from core.game_manager import GameManager
import config

DIRECTIONS = {
    QtCore.Qt.Key_A: (0, -1),
    QtCore.Qt.Key_D: (0, 1),
    QtCore.Qt.Key_W: (-1, 0),
    QtCore.Qt.Key_S: (1, 0)
}


class CellGui(QtWidgets.QLabel):
    def __init__(self, symbol, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(config.CELL_SIZE, config.CELL_SIZE)
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


class Playground(QtWidgets.QFrame):
    def __init__(self, gm, *args, **kwargs):
        super(Playground, self).__init__(*args, **kwargs)

        self.gm = gm
        self.height, self.width = gm.dimensions()
        self.timer = QtCore.QBasicTimer()
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(0)
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.grid)
        self.draw()

        self.move(config.WINDOW_OFFSET_X, config.WINDOW_OFFSET_Y)
        self.setWindowTitle('Runaway')
        self.show()

    def draw(self):
        for i in range(self.height):
            for j in range(self.width):
                cell = CellGui(self.gm.cell_at((i, j)).symbol)
                self.grid.addWidget(cell, i, j)

    def refresh_cell_style(self):
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
            self.refresh_cell_style()
        else:
            QtWidgets.QWidget.timerEvent(event)

    def start(self):
        self.timer.start(config.SPEED, self)


def main():
    m = Map('../maps/m1.txt')
    gm = GameManager(m, DIRECTIONS[QtCore.Qt.Key_D])
    app = QtWidgets.QApplication(sys.argv)
    playground = Playground(gm)
    playground.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
