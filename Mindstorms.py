import Config
import solver
import os

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pygame
from pygame.locals import *

import time

class Mindstorms:
    def __init__(self):
        self.config = Config.Config(640, 360)
        self.scanCommands = ["hand2", "hand1 hand2", "rotate1 hand1 hand2", "hand1 hand2", "hand1 hand2", "rotate3 hand1 hand2"]
        self.solveCommand = []
        self.scanRotate = [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]

        self.hand_state = None
        self.orientation = ["white", "blue"]

        self.x_change = 0
        self.y_change = 0

        self.opposite = {
            "white": "yellow",
            "yellow": "white",
            "green": "blue",
            "blue": "green",
            "orange": "red",
            "red": "orange"
            }

        self.rotList = {
            "white": ["green", "orange", "blue", "red"],
            "green": ["white", "red", "yellow", "orange"],
            "orange": ["white", "green", "yellow", "blue"],
            "blue": ["white", "orange", "yellow", "red"],
            "red": ["white", "blue", "yellow", "green"],
            "yellow": ["green", "red", "blue", "orange"]
            }

        self.notation = {
            "W": "white",
            "G": "green",
            "O": "orange",
            "B": "blue",
            "R": "red",
            "Y": "yellow",
            "2": 2,
            "'": 3
            }

    def start_scan(self, canvas = None):
        if canvas:
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.config.update(canvas)
            pygame.display.flip()

        for i in range(len(self.scanCommands)):
            #print(self.scanCommands[i], i in self.rotate)
            self.do_command(self.scanCommands[i])
            time.sleep(0.5)
            if canvas:
                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.config.update(canvas)
            self.config.saveFace(self.config.image)

            

            self.config.current_face += 1
            pygame.display.flip()

        self.config.guess()
        self.config.state = "guess"
        self.config.cap.release()
        
        print(self.config.guess_data)

        for i in self.scanRotate:
            old = self.config.guess_data[i]
            new = [[old[0][2], old[1][2], old[2][2]],
                   [old[0][1], old[1][1], old[2][1]],
                   [old[0][0], old[1][0], old[2][0]]]
            self.config.guess_data[i] = new

        print(self.config.guess_data)
        #self.do_command("hand1")

    def do_command(self, command):
        file = open("commands.txt", "w")
        file.write(command)
        file.close()
        os.system("pscp -pw maker commands.txt robot@ev3dev:")
        os.system("plink -pw maker robot@ev3dev python3 execute.py")

    """def solve(self):
        self.config.guess()
        print(self.config.guess_data)"""

    def hand_down(self):
        if self.hand_state == "up":
            self.solveCommand.append("hand1")
            self.hand_state = "down"
            return True
        return False

    def hand_up(self):
        if self.hand_state == "down":
            self.solveCommand.append("hand2")
            self.hand_state = "up"

            self.orientation = [self.orientation[1], self.opposite[self.orientation[0]]]
            return True
        return False

    def rotate(self, times):
        self.solveCommand.append("rotate" + str(times))
        if self.hand_state == "up":
            index = self.rotList[self.orientation[0]].index(self.orientation[1])
            index = (index + times) % 4
            self.orientation = [self.orientation[0], self.rotList[self.orientation[0]][index]]

    def event(self, event, canvas):
        if self.config.state == "pictures":
            self.config.event(event)
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_DOWN: #and self.config.state == "pictures":
                if self.config.state == "guess":
                    self.hand_state = "down"
                    self.hand_up()
                    self.solve()
                #else:
                #self.y_change = 1
            elif event.key == pygame.K_UP: #and self.config.state == "pictures":
                if self.config.state == "guess":
                    self.hand_state = "up"
                    self.solve()

                #else:
                #self.y_change = -1
            #elif event.key == pygame.K_RIGHT and self.config.state == "pictures":
            #    self.x_change = 1
            #elif event.key == pygame.K_LEFT and self.config.state == "pictures":
            #    self.x_change = -1
            #elif event.key == pygame.K_SPACE and self.config.state == "pictures":
                #self.start_scan(canvas)
                #self.solve()
        elif event.type == pygame.KEYUP:
            self.x_change = 0
            self.y_change = 0

    def update(self, canvas):
        self.config.update(canvas)
        self.config.x += self.x_change
        self.config.y += self.y_change

    def turnFace(self, face, times, next = None):
        if self.hand_state == "down":
            self.hand_up()

        if self.orientation[0] == face:
            self.hand_down()
            self.hand_up()
            self.hand_down()
            self.hand_up()

        elif not self.orientation[0] == self.opposite[face]:
            current = self.rotList[self.orientation[0]].index(self.orientation[1])
            goal = self.rotList[self.orientation[0]].index(self.opposite[face])
            rotations = (goal - current) % 4

            if not rotations == 0:
                self.rotate(rotations)
            self.hand_down()
            self.hand_up()

        if next and (not next == self.opposite[face]):
            current = self.rotList[self.orientation[0]].index(self.orientation[1])
            goal = self.rotList[self.orientation[0]].index(self.opposite[next])
            rotations = (goal - current) % 4
            if not rotations == 0:
                self.rotate(rotations)
        self.hand_down()
        self.rotate(times)

    def solve(self):
        cubeSolver = solver.Solver()
        cubeSolver.paint2(self.config.guess_data[:6])
        
        cubeSolver.solve2()
        solution = cubeSolver.notes()

        for i in range(len(solution)):
            move = solution[i]
            next = None
            if i < len(solution) - 1:
                next = self.notation[solution[i + 1][0]]
            
            times = 1
            if len(move) > 1:
                times = self.notation[move[1]]
            face = self.notation[move[0]]

            self.turnFace(face, times, next)

        self.hand_up()
        print(self.solveCommand)

        self.do_command(" ".join(self.solveCommand))

def main():

    width = 640
    height = 360
    canvas = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

    mindstroms = Mindstorms()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                done = True
            mindstroms.event(event, canvas)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        mindstroms.config.update(canvas)
        pygame.display.flip()

if __name__ == "__main__":
    main()