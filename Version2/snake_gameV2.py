#AUTHOR: Smayan Nirantare

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, random, time

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Snake Game")
        self.setGeometry(100, 100, COLS * CELL_SIZE, ROWS * CELL_SIZE + RELIEF)

        self.cells = [[QLabel(self) for i in range(COLS)] for j in range(ROWS)]

        loop = QTimer(self)
        loop.timeout.connect(self.mainLoop)
        loop.start(80)

        self.dirx = 0
        self.diry = 0
        self.row = 5
        self.col = 5

        self.snake_body = []
        self.pre_body = []
        self.snake_length = 1

        self.cells[self.row][self.col].setStyleSheet("border: 1px solid black; background-color: green")
        self.food_row, self.food_col = self.getFoodPos()

        self.score_lbl = QLabel(self)
        self.score_lbl.setFont(FONT1)
        self.score_lbl.setGeometry(10, 0, 500, RELIEF)

        self.createGrid()

    def createGrid(self):
        x = 0
        y = RELIEF

        for row in range(ROWS):
            for col in range(COLS):
                cell = self.cells[row][col]
                
                #alligns text in label to the center
                cell.setAlignment(QtCore.Qt.AlignCenter)
                cell.setFont(FONT1)

                #determines placement and size of label
                cell.setGeometry(x, y, CELL_SIZE, CELL_SIZE)
                x += CELL_SIZE

                cell.setStyleSheet("border: 1px solid black; background-color: white")
            x = 0
            y += CELL_SIZE

    
    def mainLoop(self):
        self.score_lbl.setText("Score: " + str(self.snake_length))
        self.move()

    def move(self):
        self.row += self.diry
        self.col += self.dirx

        if self.col == -1:
            self.col = COLS - 1
        if self.row == -1:
            self.row = ROWS - 1
        if self.col == COLS:
            self.col = 0
        if self.row == ROWS:
            self.row = 0

        self.handleLength()

        color = LIGHT_GREEN
        for i, segment in enumerate(self.snake_body):
            if i == len(self.snake_body) - 1: color = GREEN

            self.cells[segment[0]][segment[1]].setStyleSheet("border: 1px solid black; background-color: " + color)    


        for row in range(ROWS):
            for col in range(COLS):
                if [row, col] not in self.snake_body:
                    self.cells[row][col].setStyleSheet("border: 1px solid black; background-color: white")
        
        
        self.cells[self.food_row][self.food_col].setStyleSheet("border: 1px solid black; background-color: red")

    def handleLength(self):

        snake_head = []
        snake_head.append(self.row)
        snake_head.append(self.col)
        self.snake_body.append(snake_head)
        if len(self.snake_body) > self.snake_length:
            self.snake_body.pop(0)

        if self.snake_body[-1] in self.snake_body[:-1]:
            self.reset()

        if self.row == self.food_row and self.col == self.food_col:
            self.snake_length += 1
            self.food_row, self.food_col = self.getFoodPos()

    def getFoodPos(self):
        food_col = random.randint(0, COLS - 1) 
        food_row = random.randint(0, ROWS - 1)
        
        return food_row, food_col

    def reset(self):
        time.sleep(1)
        self.dirx = 0
        self.diry = 0
        self.snake_length = 1
        self.snake_body.clear()

        self.row = 5
        self.col = 5

        self.food_row, self.food_col = self.getFoodPos()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Down and self.diry != -1:
            self.diry = 1
            self.dirx = 0
        elif event.key() == QtCore.Qt.Key_Up and self.diry != 1:
            self.diry = -1
            self.dirx = 0
        elif event.key() == QtCore.Qt.Key_Left and self.dirx != 1:
            self.dirx = -1
            self.diry = 0
        elif event.key() == QtCore.Qt.Key_Right and self.dirx != -1:
            self.dirx = 1
            self.diry = 0


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


ROWS = 15
COLS = 15
CELL_SIZE = 75
RELIEF = 100

FONT1 = QFont("Arial", 20)

RED = "rgb(255, 0, 0)"
GREEN = "rgb(0, 180, 0)"
LIGHT_GREEN = "rgb(0, 255, 0)"
BLUE = "rgb(0, 0, 255)"


if __name__ == '__main__':
    main()