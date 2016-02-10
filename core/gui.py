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

class Playground(QtGui.QFrame):

    def __init__(self, gm):
        super(Playground, self).__init__()

        self.gm = gm
        self.height, self.width = gm.dimensions()
        self.hero_direction = DIRECTIONS[QtCore.Qt.Key_D]
        self.timer = QtCore.QBasicTimer()
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(0)
        self.init_ui()
        self.setStyleSheet(
            """
            QPushButton {
            background-color: red;
            border: 0;
            }
            """
        )

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
                button.setFixedSize(20, 20)
                button.setFlat(True)
                self.grid.addWidget(button, i, j)

    def update_playground(self):
        for i in range(self.height):
            for j in range(self.width):
                button = self.grid.itemAtPosition(i, j).widget()
                button.setText(self.gm.symbol_at((i, j)))

    def keyPressEvent(self, event):
        if event.key() in DIRECTIONS:
            self.hero_direction = DIRECTIONS.get(event.key(), self.hero_direction)
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.gm.move_cells(self.hero_direction)
            if self.gm.game_over:
                    QMessageBox.information(self, 'Game Over', ':( :( :(')
                    sys.exit()
            self.update_playground()
        else:
            QtGui.QWidget.timerEvent(event)

    def start(self):
        self.timer.start(SPEED, self)

def main():
    m = Map('../maps/m2.txt')
    gm = GameManager(m)
    app = QtGui.QApplication(sys.argv)
    playground = Playground(gm)
    playground.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
