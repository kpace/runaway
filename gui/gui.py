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
    QtCore.Qt.Key_Up: Direction.UP,
    QtCore.Qt.Key_Down: Direction.DOWN,
    QtCore.Qt.Key_Left: Direction.LEFT,
    QtCore.Qt.Key_Right: Direction.RIGHT
}


class Runaway(QtWidgets.QMainWindow):

    def __init__(self, gm):
        # TODO: call constructors identically everywhere
        super().__init__()

        self.status_bar = self.statusBar()
        self.playground = Playground(gm, self.status_bar)
        self.setCentralWidget(self.playground)

        self.move(config.WINDOW_OFFSET_X, config.WINDOW_OFFSET_Y)
        self.setWindowTitle('Runaway')
        self.show()
        self.playground.start()
        # set the focus to the playground so arrow keys can work
        self.playground.setFocus()

class Playground(QtWidgets.QFrame):
    def __init__(self, gm, status_bar, *args, **kwargs):
        super(Playground, self).__init__(*args, **kwargs)

        self.gm = gm
        self.status_bar = status_bar
        self.gm.bind_move(self.refresh_style)
        self.height, self.width = gm.dimensions()
        self.hero_movement_timer = QtCore.QBasicTimer()
        self.monster_movement_timer = QtCore.QBasicTimer()
        self.chase_wander_timer = QtCore.QBasicTimer()
        self.header = QtWidgets.QGridLayout()
        self.field = QtWidgets.QGridLayout()
        self.field.setSpacing(0)
        self.style = get_style()
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.field)
        self.draw()

    def draw(self):
        for i in range(self.height):
            for j in range(self.width):
                self.create_cell(self.gm.cell_at(Position(i, j)).symbol, i, j)
        self.setStyleSheet(self.style)

    def refresh_style(self, cells):
        for cell in cells:
            cell_gui = self.field.itemAtPosition(cell.y, cell.x).widget()
            cell_gui.setProperty('symbol', cell.symbol)
            cell_gui.setStyleSheet(self.style)

    def refresh_style_all(self):
        for i in range(self.height):
            for j in range(self.width):
                cell = self.gm.cell_at(Position(i, j))
                cell_gui = self.field.itemAtPosition(i, j).widget()
                cell_gui.setProperty('symbol', cell.symbol)
        self.setStyleSheet(self.style)

    def create_cell(self, symbol, i, j):
        cell = QtWidgets.QToolButton()
        cell.setAutoFillBackground(True)
        cell.setAutoRaise(True)
        cell.setFixedSize(config.CELL_SIZE, config.CELL_SIZE)
        cell.setProperty('symbol', symbol)
        self.field.addWidget(cell, i, j)

    def keyPressEvent(self, event):
        if event.key() in DIRECTIONS:
            self.gm.set_direction(DIRECTIONS.get(event.key()))
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def timerEvent(self, event):
        # TODO: move this functionality in GameManager
        # in order to have better decoupling
        self.status_bar.showMessage("Points: " + str(self.gm.points))
        if event.timerId() == self.hero_movement_timer.timerId():
            self.gm.move_hero()
        elif event.timerId() == self.monster_movement_timer.timerId():
            self.gm.move_monsters()
            if self.gm.game_over:
                self.game_over()
        elif event.timerId() == self.chase_wander_timer.timerId():
            self.gm.toggle_chasing()
        else:
            QtWidgets.QWidget.timerEvent(event)

    def start_timers(self):
        self.hero_movement_timer.start(config.HERO_MOVEMENT_SPEED, self)
        self.monster_movement_timer.start(config.MONSTER_MOVEMENT_SPEED, self)
        self.chase_wander_timer.start(config.CHASE_WANDER_SPEED, self)

    def stop_timers(self):
        self.hero_movement_timer.stop()
        self.monster_movement_timer.stop()
        self.chase_wander_timer.stop()

    def start(self):
        self.start_timers()

    def game_over(self):
        self.stop_timers()
        answer = QMessageBox.question(self, 'Game Over',
                                      'The game is over. Restart?',
                                      QMessageBox.Yes, QMessageBox.No)
        if answer == QMessageBox.Yes:
            self.gm.restart()
            self.refresh_style_all()
            self.start_timers()
        else:
            QtWidgets.QApplication.quit()


def main():
    QtCore.QResource.registerResource(config.BINARY_RESOURCES_PATH)
    m = Map('../maps/m1.txt')
    gm = GameManager(m, Direction.RIGHT)
    app = QtWidgets.QApplication(sys.argv)
    game = Runaway(gm)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
