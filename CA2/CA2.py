from select import select
import turtle
import math
import random
import time
from time import sleep
from sys import argv

INF = math.inf

class Sim:
    # Set true for graphical interface
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()

        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        sleep(1)

    def _swap_turn(self, turn):
        if turn == 'red':
            return 'blue'
        else:
            return 'red'

    def checkMinValue(self,minValue, alpha):
        if minValue <= alpha:
            return True
        else:
            return False

    def checkMaxValue(self,maxValue, beta):
        if maxValue >= beta:
            return True
        else:
            return False

    def _evaluate(self):
        score = 0
        if self.turn == 'red':
            for x in self.available_moves:
                self.red.append(x)
                if len(self.red) >= 3:
                    self.red.sort()
                    for i in range(len(self.red) - 2):
                        for j in range(i + 1, len(self.red) - 1):
                            for k in range(j + 1, len(self.red)):
                                if self.red[i][0] == self.red[j][0] and self.red[i][1] == self.red[k][0] and self.red[j][1] == self.red[k][1]:
                                    score -= 3
                                else:
                                    score += 5
                self.red.remove(x)
            return score
        if self.turn == 'blue':
            for x in self.available_moves:
                self.blue.append(x)
                if len(self.blue) >= 3:
                    self.blue.sort()
                    for i in range(len(self.blue) - 2):
                        for j in range(i + 1, len(self.blue) - 1):
                            for k in range(j + 1, len(self.blue)):
                                if self.blue[i][0] == self.blue[j][0] and self.blue[i][1] == self.blue[k][0] and self.blue[j][1] == self.blue[k][1]:
                                    score += 5
                                else:
                                    score -= 3
                self.blue.remove(x)
            return score

    def set_changes(self, move, depth,alpha, beta, turn):
        self.available_moves.remove(move)
        if turn == 'red':
            self.red.append(move)
            temp = self.minimax(depth - 1, 'blue',alpha,beta)[1]
            self.available_moves.append(move)
            self.red.remove(move)
        if turn == 'blue':
            self.blue.append(move)
            temp = self.minimax(depth - 1, 'red',alpha,beta)[1]
            self.available_moves.append(move)
            self.blue.remove(move)
        return temp

    def minimax(self, depth, player_turn, alpha =-INF, beta = INF):
        #check if a triangle is formed
        if len(self.red) >= 3:
            self.red.sort()
            for i in range(len(self.red) - 2):
                for j in range(i + 1, len(self.red) - 1):
                    for k in range(j + 1, len(self.red)):
                        if self.red[i][0] == self.red[j][0] and self.red[i][1] == self.red[k][0] and self.red[j][1] == self.red[k][1]:
                            return None,-INF
        if len(self.blue) >= 3:
            self.blue.sort()
            for i in range(len(self.blue) - 2):
                for j in range(i + 1, len(self.blue) - 1):
                    for k in range(j + 1, len(self.blue)):
                        if self.blue[i][0] == self.blue[j][0] and self.blue[i][1] == self.blue[k][0] and self.blue[j][1] == self.blue[k][1]:
                            return None,INF

        #check if depth is 0
        if depth == 0:
            return None, self._evaluate()

        selectedMove = None
        #maximizing player
        if player_turn == 'red':
            maxValue = -INF
            for child in self.available_moves:
                temp = self.set_changes(child, depth,alpha,beta,player_turn)

                if temp >= maxValue:
                    selectedMove = child
                    maxValue = temp
                #pruning
                alpha = alpha if alpha > maxValue else maxValue
                if self.prune and self.checkMaxValue(maxValue, beta): return selectedMove, maxValue

            return selectedMove, maxValue
        #minimizing player
        if player_turn == 'blue':
            minValue = INF
            for child in self.available_moves:
                temp = self.set_changes(child, depth,alpha,beta,player_turn)

                if temp <= minValue:
                    selectedMove = child
                    minValue = temp
                #pruning
                beta = beta if beta < minValue else minValue
                if self.prune and self.checkMinValue(minValue, alpha):
                    return selectedMove, minValue

            return selectedMove, minValue

    def enemy(self):
        return random.choice(self.available_moves)

    def play(self):
        self.initialize()
        while True:
            if self.turn == 'red':
                selection = self.minimax(depth=self.minimax_depth, player_turn=self.turn)[0]
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)

            self.available_moves.remove(selection)
            self.turn = self._swap_turn(self.turn)
            selection = []
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                return r

    def gameover(self, r, b):
        if len(r) < 3 and len(b) < 3:
            return 0
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0


if __name__=="__main__":
    game = Sim(minimax_depth=int(argv[1]), prune=True, gui=int(argv[2]))
    results = {"red": 0, "blue": 0}
    start = time.time()
    for i in range(1):
        winner = game.play()
        print("Game",i + 1, "Winner:",winner)
        results[winner] += 1
    end = time.time()
    print("Time taken:", end - start)
    print(results)