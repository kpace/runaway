import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from core.cells import Direction, Position
from core.map import Map
from core.game_manager import GameManager
from utils import get_style

import config
from resources import resources_rc

DIRECTIONS = {
    QtCore.Qt.Key_W: Direction.UP,
    QtCore.Qt.Key_S: Direction.DOWN,
    QtCore.Qt.Key_A: Direction.LEFT,
    QtCore.Qt.Key_D: Direction.RIGHT
}

class Playground(QtWidgets.QFrame):
    def __init__(self, gm, *args, **kwargs):
        super(Playground, self).__init__(*args, **kwargs)

        self.gm = gm
        self.gm.bind_move(self.refresh_cells)
        self.height, self.width = gm.dimensions()
        self.hero_movement_timer = QtCore.QBasicTimer()
        self.monster_movement_timer = QtCore.QBasicTimer()
        self.chase_wander_timer = QtCore.QBasicTimer()
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(0)
        self.style = get_style()
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
                self.create_cell(self.gm.cell_at(Position(i, j)).symbol, i, j)
        self.setStyleSheet(self.style)

    def refresh_cells(self, cells):
        for cell in cells:
            cell_gui = self.grid.itemAtPosition(cell.y, cell.x).widget()
            cell_gui.setProperty('symbol', cell.symbol)
            cell_gui.setStyleSheet(self.style)

    def create_cell(self, symbol, i, j):
        cell = QtWidgets.QToolButton()
        cell.setAutoFillBackground(True)
        cell.setAutoRaise(True)
        cell.setFixedSize(config.CELL_SIZE, config.CELL_SIZE)
        cell.setProperty('symbol', symbol)
        self.grid.addWidget(cell, i, j)

    def keyPressEvent(self, event):
        if event.key() in DIRECTIONS:
            self.gm.set_direction(DIRECTIONS.get(event.key()))
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def timerEvent(self, event):
        if event.timerId() == self.hero_movement_timer.timerId():
            self.gm.move_hero()
        elif event.timerId() == self.monster_movement_timer.timerId():
            self.gm.move_monsters()
            if self.gm.game_over:
                QMessageBox.information(self, 'Game Over', ':( :( :(')
                sys.exit()
        elif event.timerId() == self.chase_wander_timer.timerId():
            self.gm.toggle_chasing()
        else:
            QtWidgets.QWidget.timerEvent(event)

    def start(self):
        self.hero_movement_timer.start(config.HERO_MOVEMENT_SPEED, self)
        self.monster_movement_timer.start(config.MONSTER_MOVEMENT_SPEED, self)
        self.chase_wander_timer.start(config.CHASE_WANDER_SPEED, self)


def main():
    QtCore.QResource.registerResource(config.BINARY_RESOURCES_PATH)
    m = Map('../maps/m1.txt')
    gm = GameManager(m, Direction.RIGHT)
    app = QtWidgets.QApplication(sys.argv)
    playground = Playground(gm)
    playground.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
