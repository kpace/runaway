import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from core.cells import Direction
from core.map import Map
from core.game_manager import GameManager
import config

DIRECTIONS = {
    QtCore.Qt.Key_W: Direction.UP,
    QtCore.Qt.Key_S: Direction.DOWN,
    QtCore.Qt.Key_A: Direction.LEFT,
    QtCore.Qt.Key_D: Direction.RIGHT
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
        self.hero_movement_timer = QtCore.QBasicTimer()
        self.monster_movement_timer = QtCore.QBasicTimer()
        self.chase_wander_timer = QtCore.QBasicTimer()
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
        if event.timerId() == self.hero_movement_timer.timerId():
            self.gm.move_hero()
            self.refresh_cell_style()
        elif event.timerId() == self.monster_movement_timer.timerId():
            self.gm.move_monsters()
            if self.gm.game_over:
                QMessageBox.information(self, 'Game Over', ':( :( :(')
                sys.exit()
            self.refresh_cell_style()
        elif event.timerId() == self.chase_wander_timer.timerId():
            self.gm.toggle_chasing()
        else:
            QtWidgets.QWidget.timerEvent(event)

    def start(self):
        self.hero_movement_timer.start(config.HERO_MOVEMENT_SPEED, self)
        self.monster_movement_timer.start(config.MONSTER_MOVEMENT_SPEED, self)
        self.chase_wander_timer.start(config.CHASE_WANDER_SPEED, self)


def main():
    m = Map('../maps/m1.txt')
    gm = GameManager(m, Direction.RIGHT)
    app = QtWidgets.QApplication(sys.argv)
    playground = Playground(gm)
    playground.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
