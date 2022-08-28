import os
import PIL
import sys
import random
from tkinter import *
from PIL import Image, ImageTk


class Constant:
    BOARD_WIDTH = 300
    BOARD_HEIGHT = 300
    DOT_SIZE = 10
    DELAY = 100
    MAX_RAND_POS = 27
    DIFFICULTY = 'Medium'


class Board(Canvas):
    def __init__(self):
        super().__init__(width=Constant.BOARD_WIDTH, height=
        Constant.BOARD_HEIGHT, background=
                         'green', highlightthickness=0)
        self.initGame()
        self.pack()

    def initGame(self):
        self.inGame = True
        self.dots = 3
        self.score = 0

        self.moveX = Constant.DOT_SIZE
        self.moveY = 0

        self.appleX = 100
        self.appleY = 150

        self.loadImages()
        self.createObjects()
        self.locateApple()
        self.locateMine()
        self.bind_all('<Key>', self.onKeyPressed)
        self.after(Constant.DELAY, self.onTimer)

    def loadImages(self):
        try:
            self.idot = Image.open('dot.png')
            self.dot = ImageTk.PhotoImage(self.idot)
            self.ihead = Image.open('head.png')
            self.head = ImageTk.PhotoImage(self.ihead)
            self.iapple = Image.open('apple.png')
            self.apple = ImageTk.PhotoImage(self.iapple)
            self.imine = Image.open('mine.png')
            self.mine = ImageTk.PhotoImage(self.imine)
        except IOError as e:
            print(e)
            sys.exit(1)

    def createObjects(self):
        self.create_text(30, 10, text="Счет: {0}".format(self.score),
                         tag='score', fill='white')
        self.create_image(self.appleX, self.appleY,
                          image=self.apple, anchor=NW,
                          tag='apple')
        self.create_image(50, 50, image=self.head, anchor=NW,
                          tag='head')
        self.create_image(30, 50, image=self.dot, anchor=NW,
                          tag='dot')
        self.create_image(40, 50, image=self.dot, anchor=NW,
                          tag='dot')
        self.create_image(35, 50, image=self.mine, anchor=NW,
                          tag='mine')

    def moveSnake(self):
        dots = self.find_withtag('dot')
        head = self.find_withtag('head')
        items = dots + head
        p = 0
        while p < len(items) - 1:
            k1 = self.coords(items[p])
            k2 = self.coords(items[p + 1])
            self.move(items[p], k2[0] - k1[0], k2[1] - k1[1])
            p += 1
        self.move(head, self.moveX, self.moveY)

    def locateApple(self):
        apple = self.find_withtag("apple")
        for x in range(apple.__len__()):
            self.delete(apple[x])
        count = 1
        if Constant.DIFFICULTY == 'Easy':
            count = random.randint(1, 4)
        elif Constant.DIFFICULTY == 'Medium':
            count = random.randint(1, 3)
        elif Constant.DIFFICULTY == 'Hard':
            count = random.randint(1, 2)
        elif Constant.DIFFICULTY == 'Harder':
            count = random.randint(1, 1)
        for x in range(count):
            r = random.randint(0, Constant.MAX_RAND_POS)
            self.appleX = r * Constant.DOT_SIZE
            r = random.randint(0, Constant.MAX_RAND_POS)
            self.appleY = r * Constant.DOT_SIZE
            self.create_image(self.appleX, self.appleY, anchor=NW,
                              image=self.apple, tag="apple")

    def locateMine(self):
        mine = self.find_withtag('mine')
        self.delete(mine[0])
        r = random.randint(0, Constant.MAX_RAND_POS)
        self.mineX = r * Constant.DOT_SIZE
        r = random.randint(0, Constant.MAX_RAND_POS)
        self.mineY = r * Constant.DOT_SIZE
        self.create_image(self.mineX, self.mineY, anchor=NW,
                          image=self.mine, tag='mine')

    def onKeyPressed(self, e):
        key = e.keysym
        LEFT_CURSOR_KEY = 'Left'
        if key == LEFT_CURSOR_KEY and self.moveX <= 0:
            self.moveX = -Constant.DOT_SIZE
            self.moveY = 0

        RIGHT_CURSOR_KEY = 'Right'
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
            self.moveX = Constant.DOT_SIZE
            self.moveY = 0

        UP_CURSOR_KEY = 'Up'
        if key == UP_CURSOR_KEY and self.moveY <= 0:
            self.moveX = 0
            self.moveY = -Constant.DOT_SIZE

        DOWN_CURSOR_KEY = 'Down'
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:
            self.moveX = 0
            self.moveY = Constant.DOT_SIZE

    def onTimer(self):
        self.drawScore()
        self.checkCollision()
        if self.inGame:
            self.checkAppleCollision()
            self.moveSnake()
            self.checkMineCollision()
            self.after(Constant.DELAY, self.onTimer)
        else:
            self.gameOver()

    def drawScore(self):
        score = self.find_withtag('score')
        self.itemconfigure(score, text="Счет: {0}".format(self.score))

    def gameOver(self):
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2,
                         text="Вы проиграли! Счет: {0}".format(self.score),
                         fill="white")
        btn = Button(self, text='Заново', command=self.restartGame)
        btn.place(x=110, y=170)

    def restartGame(self):
        self.destroy()
        sn = Snake()
        self.mainloop()

    def checkCollision(self):
        dots = self.find_withtag('dot')
        head = self.find_withtag('head')
        x1, y1, x2, y2 = self.bbox('head')
        overlap = self.find_overlapping(x1, y1, x2, y2)
        for dot in dots:
            for over in overlap:
                if over == dot:
                    self.inGame = False
        if x1 < 0:
            self.inGame = False
        if x1 > Constant.BOARD_WIDTH - Constant.DOT_SIZE:
            self.inGame = False
        if y1 < 0:
            self.inGame = False
        if y1 > Constant.BOARD_HEIGHT - Constant.DOT_SIZE:
            self.inGame = False

    def checkAppleCollision(self):
        apples = self.find_withtag('apple')
        head = self.find_withtag('head')
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
        for over in overlap:
            for apple in apples:
                if apple == over:
                    self.score += 1
                    x, y = self.coords(apple)
                    self.create_image(x, y, image=self.dot,
                                      anchor=NW, tag='dot')
                    self.locateApple()
                    self.locateMine()

    def checkMineCollision(self):
        mine = self.find_withtag('mine')
        head = self.find_withtag('head')
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)
        for over in overlap:
            if mine[0] == over:
                self.inGame = False


class Snake(Frame):
    def __init__(self):
        super().__init__()
        self.master.title('Snake Beta')
        self.board = Board()
        self.pack()


class Menu(Canvas):
    def __init__(self):

        super().__init__(width=Constant.BOARD_WIDTH, height=
        Constant.BOARD_HEIGHT, background=
                         'green', highlightthickness=0)

        self.level = IntVar()
        self.level.set(0)
        self.menu()

    def startGame(self):
        print(self.level.get())
        print('Игра началась!')
        if self.level.get() == 1:
            Constant.DIFFICULTY = 'Easy'
            Constant.DELAY = 100
        elif self.level.get() == 2:
            Constant.DIFFICULTY = 'Medium'
            Constant.DELAY = 85
        elif self.level.get() == 3:
            Constant.DIFFICULTY = 'Hard'
            Constant.DELAY = 75
        elif self.level.get() == 4:
            Constant.DIFFICULTY = 'Harder'
            Constant.DELAY = 50

        self.destroy()
        self.quit()

    def menu(self):
        header = Label(text='Выберите сложность:', padx=15, pady=10)
        header.place(relx=0.3, rely=0.05)
        levels = [('Easy', 1), ('Medium', 2), ('Hard', 3), ('Harder', 4)]

        lvleasy_checkbutton = Radiobutton(text='Easy', value=1, variable=self.level, padx=15, pady=10)
        lvleasy_checkbutton.place(relx=0.3, rely=0.25)

        lvlmed_checkbutton = Radiobutton(text='Medium', value=2, variable=self.level, padx=15, pady=10)
        lvlmed_checkbutton.place(relx=0.3, rely=0.4)

        lvlhard_checkbutton = Radiobutton(text='Hard', value=3, variable=self.level, padx=15, pady=10)
        lvlhard_checkbutton.place(relx=0.3, rely=0.55)

        lvlhardr_checkbutton = Radiobutton(text='Harder', value=4, variable=self.level, padx=15, pady=10)
        lvlhardr_checkbutton.place(relx=0.3, rely=0.70)
        startButton = Button(self, text='Играть')
        startButton.config(command=self.startGame)
        startButton.place(relx=0.3, rely=0.9)
        self.pack()
        self.mainloop()


def main():
    root = Tk()

    root.resizable(False, False)

    menu = Menu()
    sn = Snake()
    root.mainloop()

if __name__ == '__main__':
    main()
