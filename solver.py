import Model

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random

import math

import json

import copy

blue = Model.blue
green = Model.green
red = Model.red
orange = Model.orange
yellow = Model.yellow
white = Model.white

face_names = ["white", "green", "orange", "blue", "red", "yellow"]
face_names2 = {"white" : white, "green" : green, "orange" : orange, "blue" : blue, "red" : red, "yellow" : yellow}
openGLcolors = [(1, 1, 1), (0, 1, 0), (1, 0.5, 0), (0, 0, 1), (1, 0, 0), (1, 1, 0)]

sides = {
    "white": [(0, 0, 1), (1, 0, 0), (0, 1, 0), (1, 0.5, 0)],
    "green": [(1, 1, 1), (1, 0, 0), (1, 1, 0), (1, 0.5, 0)],
    "orange": [(1, 1, 1), (0, 1, 0), (1, 1, 0), (0, 0, 1)],
    "blue": [(1, 1, 1), (1, 0.5, 0), (1, 1, 0), (1, 0, 0)],
    "red": [(1, 1, 1), (0, 0, 1), (1, 1, 0), (0, 1, 0)],
    "yellow": [(0, 1, 0), (1, 0, 0), (0, 0, 1), (1, 0.5, 0)]
    }

testing = [[[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[1, 1, 1], [1, 1, 1], [2, 2, 5]], [[2, 2, 2], [2, 2, 2], [4, 4, 3]], [[3, 3, 3], [3, 3, 3], [1, 1, 5]], [[4, 4, 4], [4, 4, 4], [2, 3, 5]], [[5, 5, 1], [5, 5, 5], [3, 5, 4]]],
           [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[1, 1, 1], [1, 1, 1], [2, 3, 5]], [[2, 2, 2], [2, 2, 2], [2, 2, 5]], [[3, 3, 3], [3, 3, 3], [4, 4, 3]], [[4, 4, 4], [4, 4, 4], [1, 1, 5]], [[1, 5, 4], [5, 5, 5], [5, 5, 3]]],
           [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[1, 1, 1], [1, 1, 1], [4, 1, 2]], [[2, 2, 2], [2, 2, 2], [3, 3, 1]], [[3, 3, 3], [3, 3, 3], [2, 4, 4]], [[4, 4, 4], [4, 4, 4], [1, 2, 3]], [[5, 5, 5], [5, 5, 5], [5, 5, 5]]],
           [[[0, 0, 0], [0, 0, 0], [0, 0, 3]], [[1, 1, 4], [1, 1, 4], [5, 1, 1]], [[2, 2, 2], [2, 2, 2], [1, 2, 2]], [[3, 3, 3], [3, 3, 3], [1, 1, 4]], [[5, 4, 4], [5, 4, 4], [4, 3, 2]], [[3, 4, 5], [5, 5, 5], [0, 5, 5]]],
           [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[1, 1, 1], [1, 1, 4], [1, 1, 4]], [[2, 2, 2], [2, 2, 2], [4, 1, 2]], [[3, 3, 3], [3, 3, 3], [2, 5, 5]], [[4, 4, 4], [5, 4, 4], [5, 5, 3]], [[5, 5, 1], [4, 5, 3], [3, 2, 5]]],
           [[[1, 0, 0], [0, 0, 0], [0, 0, 0]], [[1, 1, 1], [1, 1, 4], [5, 5, 3]], [[5, 2, 2], [4, 2, 2], [2, 1, 4]], [[3, 3, 2], [3, 3, 1], [2, 5, 0]], [[4, 4, 4], [5, 4, 4], [5, 3, 3]], [[1, 3, 4], [5, 5, 2], [3, 2, 5]]],
           [[[0, 5, 5], [3, 0, 1], [0, 1, 1]], [[4, 2, 2], [5, 1, 3], [4, 4, 3]], [[1, 0, 1], [0, 2, 2], [4, 1, 3]], [[4, 4, 2], [2, 3, 2], [2, 0, 1]], [[5, 4, 3], [4, 4, 3], [0, 3, 3]], [[0, 0, 2], [5, 5, 5], [5, 1, 5]]],
           [[[2, 2, 0], [3, 0, 3], [3, 0, 3]], [[4, 2, 4], [3, 1, 3], [1, 5, 4]], [[5, 2, 0], [0, 2, 4], [0, 0, 5]], [[1, 5, 3], [2, 3, 1], [5, 1, 3]], [[5, 5, 2], [0, 4, 1], [1, 4, 1]], [[4, 1, 0], [4, 5, 5], [2, 4, 2]]],
           [[[0, 4, 2], [1, 0, 0], [1, 4, 2]], [[0, 1, 1], [1, 1, 5], [5, 5, 0]], [[3, 2, 4], [0, 2, 0], [5, 4, 4]], [[4, 0, 4], [5, 3, 3], [5, 3, 1]], [[0, 2, 3], [2, 4, 4], [2, 3, 2]], [[1, 1, 3], [3, 5, 5], [2, 2, 3]]],
           [[[1, 3, 4], [3, 0, 1], [0, 2, 2]], [[2, 3, 3], [1, 1, 2], [3, 0, 1]], [[5, 4, 3], [0, 2, 0], [1, 5, 4]], [[5, 5, 2], [1, 3, 3], [4, 2, 4]], [[5, 4, 1], [5, 4, 2], [2, 5, 3]], [[5, 4, 0], [4, 5, 1], [0, 0, 0]]]
           ]

class Rotation:
    """Manage rotation of a given face color"""
    def __init__(self, facecolor, angle_increase=1):
        self.facecolor = facecolor
        self.angle_increase = angle_increase
        self.rotation = 0
        self.completed = False

    def should_rotate(self, color, tilenum):
        """Whether the given tilenum with the given color should be rotated
        when the face with facecolor is rotated"""
        if self.facecolor == color:
            return True

        if self.facecolor == "red":
            # Red affects yellow, blue, green, white
            if color == "white" and tilenum in [2, 5, 8]:
                return True
            if color == "blue" and tilenum in [0, 3, 6]:
                return True
            if color == "yellow" and tilenum in [2, 5, 8]:
                return True
            if color == "green" and tilenum in [2, 5, 8]:
                return True
        elif self.facecolor == "yellow":
            # Yellow affects red, blue, orange, green
            if color in ["red", "orange", "green", "blue"] and tilenum in [6, 7, 8]:
                return True

        elif self.facecolor == "green":
            # Green affects red, yellow, orange, white
            if color == "red" and tilenum in [0, 3, 6]:
                return True
            if color == "orange" and tilenum in [2, 5, 8]:
                return True
            if color == "yellow" and tilenum in [0, 1, 2]:
                return True
            if color == "white" and tilenum in [6, 7, 8]:
                return True
        elif self.facecolor == "blue":
            # Blue affects orange, yellow, red, white
            if color == "red" and tilenum in [2, 5, 8]:
                return True
            if color == "orange" and tilenum in [0, 3, 6]:
                return True
            if color == "yellow" and tilenum in [6, 7, 8]:
                return True
            if color == "white" and tilenum in [0, 1, 2]:
                return True
        elif self.facecolor == "orange":
            # Orange affects yellow, blue, white, green
            if color == "white" and tilenum in [0, 3, 6]:
                return True
            if color == "blue" and tilenum in [2, 5, 8]:
                return True
            if color == "yellow" and tilenum in [0, 3, 6]:
                return True
            if color == "green" and tilenum in [0, 3, 6]:
                return True
        elif self.facecolor == "white":
            # White affects blue, red, green, orange
            if color in ["green", "blue", "red", "orange"] and tilenum in [0, 1, 2]:
                return True

    def rotate(self):
        """Rotate by the given increase"""
        self.rotation += self.angle_increase
        if self.rotation >= 90:
            self.rotation = 90
            self.completed = True
        if self.rotation <= -90:
            self.rotation = -90
            self.completed = True

    def apply_rotation(self):
        """Apply rotation matrix depending on face color"""
        if self.facecolor == "red":
            glRotatef(self.rotation, -1, 0, 0)
        if self.facecolor == "orange":
            glRotatef(self.rotation, 1, 0, 0)
        if self.facecolor == "green":
            glRotatef(self.rotation, 0, 0, -1)
        if self.facecolor == "blue":
            glRotatef(self.rotation, 0, 0, 1)
        if self.facecolor == "yellow":
            glRotatef(self.rotation, 0, 1, 0)
        if self.facecolor == "white":
            glRotatef(self.rotation, 0, -1, 0)

class Solver():
    def __init__(self, cube = Model.Cube()):
        self.cube = cube

        self.moves = []

        self.offset = 0.05

        self.up = 0
        self.left = 0
        self.face = 1
        self.rot = 0
        self.left_rot = 0
        self.up_rot = 0

        self.new = [[[3, 2], [4, 1], [1, 0], [2, 3]],
                    [[0, 0], [4, 0], [5, 0], [2, 0]],
                    [[0, 1], [1, 0], [5, 3], [3, 0]],
                    [[0, 2], [2, 0], [5, 2], [4, 0]],
                    [[0, 3], [3, 0], [5, 1], [1, 0]],
                    [[1, 0], [4, 3], [3, 2], [2, 1]]]

        self.i = 0
        self.m = False
        self.back = False
        self.tripl = False
        self.r = None
        self.l = 0

        self.start = True
        self.cursor = ["white", 0, 0]
        self.x_rot = 90
        self.y_rot = 0

        self.now = [[[0 for i in range(3)] for i in range(3)], 
                    [[1 for i in range(3)] for i in range(3)], 
                    [[2 for i in range(3)] for i in range(3)], 
                    [[3 for i in range(3)] for i in range(3)], 
                    [[4 for i in range(3)] for i in range(3)], 
                    [[5 for i in range(3)] for i in range(3)]]

        with open("algorithms.json", "r") as algorithms:
            self.algorithms = json.load(algorithms)

    def execute(self, algo, front, top, rotation = 0):

        faces = {
            "white": ["green", "red", "blue", "orange", "yellow"],
            "yellow": ["blue", "red", "green", "orange", "white"],
            "green": ["yellow", "red", "white", "orange", "blue"],
            "orange": ["yellow", "green", "white", "blue", "red"],
            "blue": ["yellow", "orange", "white", "red", "green"],
            "red": ["yellow", "blue", "white", "green", "orange"]
            }

        shift = 0
        for i in range(len(faces[top])):
            if faces[top][i] == front:
                shift = i
                break

        #U F R B L D
        notations = {
            "U": top, 
            "F": faces[top][(shift + rotation) % 4],
            "R": faces[top][(shift + 1 + rotation) % 4],
            "B": faces[top][(shift + 2 + rotation) % 4],
            "L": faces[top][(shift + 3 + rotation) % 4],
            "D": faces[top][4],
            }

        step1 = algo.split(" ")
        step2 = []
        for i in step1:
            if len(i) > 1:
                if i[1] == "2":
                    for j in range(2):
                        step2.append(i[0])
                elif i[1] == "'":
                    for j in range(3):
                        step2.append(i[0])
            else:
                step2.append(i[0])
        step3 = []
        for i in step2:
            step3.append(notations[i])

        for i in step3:
            self.move(i)

    def check_cases(self, case):
        #print(case)
        opposite = { 0: 5, 1: 3, 2: 4, 3: 1, 4: 2, 5: 0 }
        rotation = 0
        alg = ""
        for i in case["cases"]:
            for k in range(4):
                req = i[0].split(", ")
                good = True
                for j in req:
                    sections = j.split(" ")
                    tile = self.cube.faces[face_names[int(sections[0][0])]].squares[int(sections[0][2])][int(sections[0][1])].col1
                    if len(sections[2]) == 1:
                        other = int(sections[2])
                    elif len(sections[2]) == 3:
                        other = self.cube.faces[face_names[int(sections[2][0])]].squares[int(sections[2][2])][int(sections[2][1])].col1
                    #print(sections, tile)
                    if sections[1] == "=":
                        if not tile == other:
                            good = False
                            break
                    elif sections[1] == "!":
                        if tile == other:
                            good = False
                            break
                    elif sections[1] == "/":
                        if not opposite[tile] == other:
                            good = False
                            break
                if good:
                    rotation = k
                    alg = i[1]
                self.move(case["rotation"])

        return alg, rotation

    def tran_OLL(self, case):
        oll_cases = ["500", "510", "520", "501", "511", "521", "502", "512", "522", "102", "112", "122", "402", "412", "422", "302", "312", "322", "202", "212", "222"]
        cases = copy.deepcopy(case)
        l = len(cases["cases"])
        for i in range(l):
            numbers = cases["cases"][i][0]
            new = []
            length = len(numbers)
            for j in range(length):
                #print(j)
                if numbers[j] == "0":
                    new.append(oll_cases[j] + " ! 5")
                elif numbers[j] == "1":
                    new.append(oll_cases[j] + " = 5")
                else:
                    pass
            cases["cases"][i][0] = ", ".join(new)
        return cases

    def tran_PLL(self, case):
        pll_cases = ["102", "112", "122", "402", "412", "422", "302", "312", "322", "202", "212", "222"]
        cases = copy.deepcopy(case)
        l = len(cases["cases"])
        for i in range(l):
            numbers = cases["cases"][i][0]
            places = [None for j in range(4)]
            all = [[] for j in range(4)]
            length = len(numbers)
            for j in range(length):
                if not places[int(numbers[j]) - 1]:
                    places[int(numbers[j]) - 1] = pll_cases[j]
                else:
                    all[int(numbers[j]) - 1].append(pll_cases[j])
            new = []
            new.append(places[0] + " / " + places[2])
            new.append(places[1] + " / " + places[3])
            for j in range(len(all)):
                for k in all[j]:
                    new.append(k + " = " + places[j])
            cases["cases"][i][0] = ", ".join(new)
        return cases

    def tran_F2L(self, case, front):
        faces = {
            "green": ["2", "3", "4"],
            "orange": ["3", "4", "1"],
            "blue": ["4", "1", "2"],
            "red": ["1", "2", "3"]
            }

        pos_corner = {
            "5": { "21": "500", "32": "502", "43": "522", "14": "520" },
            "1": { "20": "100", "52": "102", "45": "122", "04": "120" },
            "2": { "30": "200", "53": "202", "15": "222", "01": "220" },
            "3": { "40": "300", "54": "302", "25": "322", "02": "320" },
            "4": { "10": "400", "51": "402", "35": "422", "03": "420" },
            "0": { "23": "000", "12": "002", "41": "022", "34": "020" },
            }

        pos_edge = {
            "5": { "1": "510", "2": "501", "3": "512", "4": "521" },
            "1": { "0": "110", "2": "101", "5": "112", "4": "121" },
            "2": { "0": "210", "3": "201", "5": "212", "1": "221" },
            "3": { "0": "310", "4": "301", "5": "312", "2": "321" },
            "4": { "0": "410", "1": "401", "5": "412", "3": "421" },
            "0": { "3": "010", "2": "001", "1": "012", "4": "021" },
            }

        front_tran = {
            "white": "0",
            "green": "1",
            "orange": "2",
            "blue": "3",
            "red": "4",
            "yellow": "5"
            }
        
        tran = ["5", front_tran[front]] + faces[front] + ["0"]
        cases = copy.deepcopy(case)
        l = len(cases["cases"])
        for i in range(l):
            numbers = cases["cases"][i][0]
            corner = numbers[:3]
            edge = numbers[3:]
            all_case = []
            all_case.append(pos_corner[tran[int(corner[0])]][tran[int(corner[1])] + tran[int(corner[2])]] + " = 0")
            all_case.append(pos_corner[tran[int(corner[1])]][tran[int(corner[2])] + tran[int(corner[0])]] + " = " + tran[1])
            all_case.append(pos_corner[tran[int(corner[2])]][tran[int(corner[0])] + tran[int(corner[1])]] + " = " + tran[2])

            all_case.append(pos_edge[tran[int(edge[0])]][tran[int(edge[1])]] + " = " + tran[1])
            all_case.append(pos_edge[tran[int(edge[1])]][tran[int(edge[0])]] + " = " + tran[2])
            
            cases["cases"][i][0] = ", ".join(all_case)
        return cases

    #Moves given face
    def move(self, m):
        self.cube.rotate(m)
        self.moves.append(m)

    #Shorts up solving moves
    def short(self):
        done = False
        while not done:
            new_moves = []
            for i in self.moves:
                if not len(new_moves) == 0:
                    before_row = new_moves[len(new_moves) - 1]
                    if before_row[0] == i:
                        before_row.append(i)
                    else:
                        new_moves.append([i])
                else:
                     new_moves.append([i])

            moves = []
            for move in new_moves:
                for i in range(len(move) % 4):
                    moves.append(move[0])

            if self.moves == moves:
                done = True
            self.moves = moves

    #Returns solving moves in cube notation
    def notes(self):
        new_moves = []
        for i in self.moves:
            if not len(new_moves) == 0:
                before_row = new_moves[len(new_moves) - 1]
                if before_row[0] == i:
                    before_row.append(i)
                else:
                    new_moves.append([i])
            else:
                 new_moves.append([i])

        notation = []
        for i in new_moves:
            if len(i) == 1:
                notation.append(i[0][0].upper())
            elif len(i) == 2:
                notation.append(i[0][0].upper() + "2")
            elif len(i) == 3:
                notation.append(i[0][0].upper() + "'")

        return notation

    #Draws the cube
    def Open_GL_draw(self, surface):
        

        if not (self.up == 0 and self.left == 0) and not self.start:

            #Calculates the rotation of the cube
            rotation = [
                [
                    [self.up, 0, -self.left],
                    [self.left, 0, self.up],
                    [-self.up, 0, self.left],
                    [-self.left, 0, -self.up]],
                [
                    [self.up, self.left, 0],
                    [self.left, -self.up, 0],
                    [-self.up, -self.left, 0],
                    [-self.left, self.up, 0]],
                [
                    [0, self.left, self.up],
                    [0, -self.up, self.left],
                    [0, -self.left, -self.up],
                    [0, self.up, -self.left]],
                [
                    [-self.up, self.left, 0],
                    [-self.left, -self.up, 0],
                    [self.up, -self.left, 0],
                    [self.left, self.up, 0]],
                [
                    [0, self.left, -self.up],
                    [0, -self.up, -self.left],
                    [0, -self.left, self.up],
                    [0, self.up, self.left]],
                [
                    [self.up, 0, self.left],
                    [self.left, 0, -self.up],
                    [-self.up, 0, -self.left],
                    [-self.left, 0, self.up]
                    ]
                ]
            rota = rotation[self.face][self.rot]

            glRotatef(1, rota[0], rota[1], rota[2])

            self.up_rot += self.up
            self.left_rot += self.left
            
            if self.up_rot >= 45:
                self.up_rot = self.up_rot - 90
                temp = self.rot
                self.rot = self.trans_new(self.face, self.rot, 0)[1]
                self.face = self.trans_new(self.face, temp, 0)[0]

            if self.left_rot >= 45:
                self.left_rot = self.left_rot - 90
                temp = self.rot
                self.rot = self.trans_new(self.face, self.rot, 3)[1]
                self.face = self.trans_new(self.face, temp, 3)[0]

            if self.up_rot < -45:
                self.up_rot = self.up_rot + 90
                temp = self.rot
                self.rot = self.trans_new(self.face, self.rot, 2)[1]
                self.face = self.trans_new(self.face, temp, 2)[0]
                
            if self.left_rot < -45:
                self.left_rot = self.left_rot + 90
                temp = self.rot
                self.rot = self.trans_new(self.face, self.rot, 1)[1]
                self.face = self.trans_new(self.face, temp, 1)[0]

        if self.start:
            glPushMatrix()
            if not (self.x_rot == 0 and self.y_rot == 0):
                glRotatef(self.x_rot, 1, 0, 0)
                glRotatef(self.y_rot, 0, 1, 0)

        #Draws the faces of the cube
        #print(self.cube.faces)
        self.DrawFaceFront(1.5, self.cube.faces["green"].squares, "green", self.r)
        self.DrawFaceBack(-1.5, self.cube.faces["blue"].squares, "blue", self.r)

        self.DrawFaceLeft(-1.5, self.cube.faces["orange"].squares, "orange", self.r)
        self.DrawFaceRight(1.5, self.cube.faces["red"].squares, "red", self.r)

        self.DrawFaceTop(1.5, self.cube.faces["white"].squares, "white", self.r)
        self.DrawFaceBottom(-1.5, self.cube.faces["yellow"].squares, "yellow", self.r)

        if self.start:
            glPopMatrix()

            #Draws the other things
            glBegin(GL_POLYGON)
            glColor3f(1, 1, 1)
            glVertex2fv((-5.5, 3.6))
            glVertex2fv((-5.5, 4.1))
            glVertex2fv((-5, 4.1))
            glVertex2fv((-5, 3.6))
            glEnd()

            glBegin(GL_POLYGON)
            glColor3f(0, 1, 0)
            glVertex2fv((-5, 3.6))
            glVertex2fv((-5, 4.1))
            glVertex2fv((-4.5, 4.1))
            glVertex2fv((-4.5, 3.6))
            glEnd()

            glBegin(GL_POLYGON)
            glColor3f(1, 0.5, 0)
            glVertex2fv((-4.5, 3.6))
            glVertex2fv((-4.5, 4.1))
            glVertex2fv((-4, 4.1))
            glVertex2fv((-4, 3.6))
            glEnd()

            glBegin(GL_POLYGON)
            glColor3f(0, 0, 1)
            glVertex2fv((-4, 3.6))
            glVertex2fv((-4, 4.1))
            glVertex2fv((-3.5, 4.1))
            glVertex2fv((-3.5, 3.6))
            glEnd()

            glBegin(GL_POLYGON)
            glColor3f(1, 0, 0)
            glVertex2fv((-3.5, 3.6))
            glVertex2fv((-3.5, 4.1))
            glVertex2fv((-3, 4.1))
            glVertex2fv((-3, 3.6))
            glEnd()

            glBegin(GL_POLYGON)
            glColor3f(1, 1, 0)
            glVertex2fv((-3, 3.6))
            glVertex2fv((-3, 4.1))
            glVertex2fv((-2.5, 4.1))
            glVertex2fv((-2.5, 3.6))
            glEnd()


            glColor3f(1, 1, 1)
            glBegin(GL_LINES)
            glVertex2fv((-5.25, 3.5))
            glVertex2fv((-5.25, 3))
            glEnd()

            glBegin(GL_LINE_STRIP)
            glVertex2fv((-4.875, 3.5))
            glVertex2fv((-4.625, 3.5))
            glVertex2fv((-4.625, 3.25))
            glVertex2fv((-4.875, 3.25))
            glVertex2fv((-4.875, 3.25))
            glVertex2fv((-4.875, 3))
            glVertex2fv((-4.625, 3))
            glEnd()

            glBegin(GL_LINE_STRIP)
            glVertex2fv((-4.375, 3.5))
            glVertex2fv((-4.125, 3.5))
            glVertex2fv((-4.125, 3.25))
            glVertex2fv((-4.375, 3.25))
            glVertex2fv((-4.125, 3.25))
            glVertex2fv((-4.125, 3))
            glVertex2fv((-4.375, 3))
            glEnd()

            glBegin(GL_LINE_STRIP)
            glVertex2fv((-3.875, 3.5))
            glVertex2fv((-3.875, 3.25))
            glVertex2fv((-3.625, 3.25))
            glVertex2fv((-3.625, 3.5))
            glVertex2fv((-3.625, 3))
            glEnd()

            glBegin(GL_LINE_STRIP)
            glVertex2fv((-3.125, 3.5))
            glVertex2fv((-3.375, 3.5))
            glVertex2fv((-3.375, 3.25))
            glVertex2fv((-3.125, 3.25))
            glVertex2fv((-3.125, 3))
            glVertex2fv((-3.375, 3))
            glEnd()

            glBegin(GL_LINE_STRIP)
            glVertex2fv((-2.625, 3.5))
            glVertex2fv((-2.875, 3.5))
            glVertex2fv((-2.875, 3.25))
            glVertex2fv((-2.625, 3.25))
            glVertex2fv((-2.625, 3))
            glVertex2fv((-2.875, 3))
            glVertex2fv((-2.875, 3.25))
            glEnd()

            glBegin(GL_POLYGON)
            glColor3f(*sides[self.cursor[0]][0])
            glVertex2fv((-0.5, 3))
            glVertex2fv((0.5, 3))
            glVertex2fv((0.5, 2))
            glVertex2fv((-0.5, 2))
            glEnd()

            glBegin(GL_POLYGON)
            glColor3f(*sides[self.cursor[0]][1])
            glVertex2fv((3, 0.5))
            glVertex2fv((3, -0.5))
            glVertex2fv((2, -0.5))
            glVertex2fv((2, 0.5))
            glEnd()

            glBegin(GL_POLYGON)
            glColor3f(*sides[self.cursor[0]][2])
            glVertex2fv((-0.5, -3))
            glVertex2fv((0.5, -3))
            glVertex2fv((0.5, -2))
            glVertex2fv((-0.5, -2))
            glEnd()

            glBegin(GL_POLYGON)
            glColor3f(*sides[self.cursor[0]][3])
            glVertex2fv((-3, 0.5))
            glVertex2fv((-3, -0.5))
            glVertex2fv((-2, -0.5))
            glVertex2fv((-2, 0.5))
            glEnd()

    #Update function
    def update(self):
        speed = 10
        if self.m:
            if not self.r:
                self.tripl = False
                if not self.back:
                    if self.i + 2 < self.l:
                        if self.moves[self.i] == self.moves[self.i + 1] and self.moves[self.i] == self.moves[self.i + 2]:
                            self.r = Rotation(self.moves[self.i], -speed)
                            self.tripl = True
                        else:
                            self.r = Rotation(self.moves[self.i], speed)
                    else:
                        self.r = Rotation(self.moves[self.i], speed)
                else:
                    if self.i - 3 >= 0:
                        if self.moves[self.i - 1] == self.moves[self.i - 2] and self.moves[self.i - 1] == self.moves[self.i - 3]:
                            self.r = Rotation(self.moves[self.i - 1], speed)
                            self.tripl = True
                        else:
                            self.r = Rotation(self.moves[self.i - 1], -speed)
                    else:
                        self.r = Rotation(self.moves[self.i - 1], -speed)
            
            self.r.rotate()
            if self.r: 
                if self.r.completed:
                    
                    self.m = False
                    if not self.back:
                        self.move(self.moves[self.i])
                        self.i += 1
                        if self.tripl:
                            self.move(self.moves[self.i])
                            self.move(self.moves[self.i + 1])
                            self.i += 2
                    else:
                        if not self.tripl:
                            self.move(self.moves[self.i - 1])
                            self.move(self.moves[self.i - 1])
                            self.move(self.moves[self.i - 1])
                            self.i -= 1
                        else:
                            self.move(self.moves[self.i - 1])
                            self.i -= 3
                    self.back = False
                    self.rs = 0
                    self.r = None

    #Draws the front face
    def DrawFaceFront(self, z, tiles, facecolor, rotation):
        colors = []
        for row in range(len(tiles)):
            for tile in range(len(tiles[row])):
                #print(tiles[row][tile].col1)
                colors.append([tiles[row][tile].col1, row, tile])

        tilenum = 0
        for ycorner in (0.5, -0.5, -1.5):
            for xcorner in (-1.5, -0.5, 0.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                if self.cursor[0] == facecolor and self.cursor[1] == colors[tilenum][1] and self.cursor[2] == colors[tilenum][2] and self.start:
                    glColor3f(openGLcolors[colors[tilenum][0]][0] * 0.5, openGLcolors[colors[tilenum][0]][1] * 0.5, openGLcolors[colors[tilenum][0]][2] * 0.5)
                else:
                    glColor3f(*openGLcolors[colors[tilenum][0]])
                glVertex3fv((xcorner+self.offset, ycorner+self.offset, z))
                glVertex3fv((xcorner+(1-self.offset), ycorner+self.offset, z))
                glVertex3fv((xcorner+(1-self.offset), ycorner+(1-self.offset), z))
                glVertex3fv((xcorner+self.offset, ycorner+(1-self.offset), z))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1
                
    #Draws the back face
    def DrawFaceBack(self, z, tiles, facecolor, rotation):
        colors = []
        for row in range(len(tiles)):
            for tile in range(len(tiles[row])):
                colors.append([tiles[row][tile].col1, row, tile])

        tilenum = 0
        for ycorner in (0.5, -0.5, -1.5):
            for xcorner in (0.5, -0.5, -1.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                if self.cursor[0] == facecolor and self.cursor[1] == colors[tilenum][1] and self.cursor[2] == colors[tilenum][2] and self.start:
                    glColor3f(openGLcolors[colors[tilenum][0]][0] * 0.5, openGLcolors[colors[tilenum][0]][1] * 0.5, openGLcolors[colors[tilenum][0]][2] * 0.5)
                else:
                    glColor3f(*openGLcolors[colors[tilenum][0]])
                glVertex3fv((xcorner+self.offset, ycorner+self.offset, z))
                glVertex3fv((xcorner+(1-self.offset), ycorner+self.offset, z))
                glVertex3fv((xcorner+(1-self.offset), ycorner+(1-self.offset), z))
                glVertex3fv((xcorner+self.offset, ycorner+(1-self.offset), z))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1

    #Draws the left face
    def DrawFaceLeft(self, x, tiles, facecolor, rotation):
        colors = []
        for row in range(len(tiles)):
            for tile in range(len(tiles[row])):
                colors.append([tiles[row][tile].col1, row, tile])

        tilenum = 0
        for ycorner in (0.5, -0.5, -1.5):
            for zcorner in (-1.5, -0.5, 0.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                if self.cursor[0] == facecolor and self.cursor[1] == colors[tilenum][1] and self.cursor[2] == colors[tilenum][2] and self.start:
                    glColor3f(openGLcolors[colors[tilenum][0]][0] * 0.5, openGLcolors[colors[tilenum][0]][1] * 0.5, openGLcolors[colors[tilenum][0]][2] * 0.5)
                else:
                    glColor3f(*openGLcolors[colors[tilenum][0]])
                glVertex3fv((x, ycorner+self.offset, zcorner+self.offset))
                glVertex3fv((x, ycorner+self.offset, zcorner+(1-self.offset)))
                glVertex3fv((x, ycorner+(1-self.offset), zcorner+(1-self.offset)))
                glVertex3fv((x, ycorner+(1-self.offset), zcorner+self.offset))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1

    #Draws the right face
    def DrawFaceRight(self, x, tiles, facecolor, rotation):
        colors = []
        for row in range(len(tiles)):
            for tile in range(len(tiles[row])):
                colors.append([tiles[row][tile].col1, row, tile])

        tilenum = 0
        for ycorner in (0.5, -0.5, -1.5):
            for zcorner in (0.5, -0.5, -1.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                if self.cursor[0] == facecolor and self.cursor[1] == colors[tilenum][1] and self.cursor[2] == colors[tilenum][2] and self.start:
                    glColor3f(openGLcolors[colors[tilenum][0]][0] * 0.5, openGLcolors[colors[tilenum][0]][1] * 0.5, openGLcolors[colors[tilenum][0]][2] * 0.5)
                else:
                    glColor3f(*openGLcolors[colors[tilenum][0]])
                glVertex3fv((x, ycorner+self.offset, zcorner+self.offset))
                glVertex3fv((x, ycorner+self.offset, zcorner+(1-self.offset)))
                glVertex3fv((x, ycorner+(1-self.offset), zcorner+(1-self.offset)))
                glVertex3fv((x, ycorner+(1-self.offset), zcorner+self.offset))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1

    #Draws the top face
    def DrawFaceTop(self, y, tiles, facecolor, rotation):
        colors = []
        for row in range(len(tiles)):
            for tile in range(len(tiles[row])):
                colors.append([tiles[row][tile].col1, row, tile])

        tilenum = 0
        for zcorner in (-1.5, -0.5, 0.5):
            for xcorner in (-1.5, -0.5, 0.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                if self.cursor[0] == facecolor and self.cursor[1] == colors[tilenum][1] and self.cursor[2] == colors[tilenum][2] and self.start:
                    glColor3f(openGLcolors[colors[tilenum][0]][0] * 0.5, openGLcolors[colors[tilenum][0]][1] * 0.5, openGLcolors[colors[tilenum][0]][2] * 0.5)
                else:
                    glColor3f(*openGLcolors[colors[tilenum][0]])
                glVertex3fv((xcorner+self.offset, y, zcorner+self.offset))
                glVertex3fv((xcorner+(1-self.offset), y, zcorner+self.offset))
                glVertex3fv((xcorner+(1-self.offset), y, zcorner+(1-self.offset)))
                glVertex3fv((xcorner+self.offset, y, zcorner+(1-self.offset)))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1

    #Draws the bottom face
    def DrawFaceBottom(self, y, tiles, facecolor, rotation):
        colors = []
        for row in range(len(tiles)):
            for tile in range(len(tiles[row])):
                colors.append([tiles[row][tile].col1, row, tile])

        tilenum = 0
        for zcorner in (0.5, -0.5, -1.5):
            for xcorner in (-1.5, -0.5, 0.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                if self.cursor[0] == facecolor and self.cursor[1] == colors[tilenum][1] and self.cursor[2] == colors[tilenum][2] and self.start:
                    glColor3f(openGLcolors[colors[tilenum][0]][0] * 0.5, openGLcolors[colors[tilenum][0]][1] * 0.5, openGLcolors[colors[tilenum][0]][2] * 0.5)
                else:
                    glColor3f(*openGLcolors[colors[tilenum][0]])
                glVertex3fv((xcorner+self.offset, y, zcorner+self.offset))
                glVertex3fv((xcorner+(1-self.offset), y, zcorner+self.offset))
                glVertex3fv((xcorner+(1-self.offset), y, zcorner+(1-self.offset)))
                glVertex3fv((xcorner+self.offset, y, zcorner+(1-self.offset)))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1

    #Sets color of cube
    def paint(self, lines):
        faces = [[], [], [], [], [], []]

        for i in range(len(faces)):
            face = faces[i]
            j = i * 3

            face.append(lines[j])
            face.append(lines[j+1])
            face.append(lines[j+2])

        new_f = []
        for i in faces:
            new = []
            for j in i:
                new.append(list(j))

            new_f.append(new)

        faces = new_f

        new_f = []
        for i in faces:
            new = []
            for j in i:
                n = []
                for k in j:
                    
                    if k == "w":
                        k = white
                    elif k == "g":
                        k = green
                    elif k == "o":
                        k = orange
                    elif k == "b":
                        k = blue
                    elif k == "r":
                        k = red
                    elif k == "y":
                        k = yellow
                    n.append(k)
                new.append(n)
            new_f.append(new)
        faces = new_f

        for i in range(len(faces)):
            face = faces[i]
            self.cube.paint(face_names[i], face)

    def paint2(self, faces):
        for i in range(len(faces)):
            face = faces[i]
            self.cube.paint(face_names[i], face)

    #Finds given edge
    def getEdge(self, col1, col2):

        pos = ["", ""]

        for face in self.cube.faces.items():
            face0 = face[0]
            face1 = face[1]

            for row in face1.squares:
                for c in row:
                    if isinstance(c, Model.Edge):
                        if c.col1 == col1 and c.col2 == col2:
                            pos[0] = face0

                        elif c.col1 == col2 and c.col2 == col1:
                            pos[1] = face0
        
        return pos

    #Finds given corner
    def getCorner(self, col1, col2, col3):

        pos = ["", "", ""]

        for face in self.cube.faces.items():
            face0 = face[0]
            face1 = face[1]

            for row in face1.squares:
                for c in row:
                    if isinstance(c, Model.Corner):
                        if (c.col1 == col1 or c.col1 == col2 or c.col1 == col3) and \
                            (c.col2 == col1 or c.col2 == col2 or c.col2 == col3) and \
                            (c.col3 == col1 or c.col3 == col2 or c.col3 == col3):
                            if c.col1 == col1:
                                pos[0] = face0
                            elif c.col1 == col2:
                                pos[1] = face0
                            elif c.col1 == col3:
                                pos[2] = face0

        return pos

    #A rotation calculation function for edges
    def rot_calc_edge(self, face, start, stop):
        white_f = {"green" : 0, "red" : 1, "blue" : 2, "orange" : 3}
        yellow_f = {"blue" : 0, "red" : 1, "green" : 2, "orange" : 3}
        green_f = {"yellow" : 0, "red" : 1, "white" : 2, "orange" : 3}
        orange_f = {"yellow" : 0, "green" : 1, "white" : 2, "blue" : 3}
        blue_f = {"yellow" : 0, "orange" : 1, "white" : 2, "red" : 3}
        red_f = {"yellow" : 0, "blue" : 1, "white" : 2, "green" : 3}

        f = {"white" : white_f, "yellow" : yellow_f, "green" : green_f, "orange" : orange_f, "blue" : blue_f, "red" : red_f}
        
        move = f[face]
        moves = move[start] - move[stop]
        if moves < 0:
            moves = moves + 4

        return moves

    #Inserts an edge for the white cross
    def insert_edge(self, color, protect):
        redo = []

        pos = self.getEdge(white, color)
        if pos[1] == "white" or pos[1] == "yellow":
            self.move(pos[0])
            
            for j in protect:
                if j == pos[0]:
                    redo.append(pos[0])

        pos = self.getEdge(white, color)

        move = self.rot_calc_edge(pos[1], pos[0], "yellow")
        

        for i in range(move):
            self.move(pos[1])
            for j in protect:
                if j == pos[1]:
                    redo.append(pos[1])

        
        pos = self.getEdge(white, color)
        move = self.rot_calc_edge("yellow", pos[1], face_names[color])
        
        for i in range(move):
            self.move("yellow")

        for i in redo[::-1]:
            self.move(i)
            self.move(i)
            self.move(i)

        self.move(face_names[color])
        self.move(face_names[color])

    #Solves the white cross
    def white_cross(self):
        protect = []

        self.insert_edge(green, protect)
        protect.append("green")

        self.insert_edge(orange, protect) 
        protect.append("orange")

        self.insert_edge(blue, protect)
        protect.append("blue")

        self.insert_edge(red, protect)
        protect.append("red")

    #Inserts a corner to the white face
    def insert_corner(self, col1, col2, protect):
        
        pos = self.getCorner(col1, col2, white)

        right = { "green" : "red", "red" : "blue", "blue" : "orange", "orange" : "green" }
        left = { "green" : "orange", "red" : "green", "blue" : "red", "orange" : "blue" }

        if pos[0] == "white" or pos[1] == "white":
            if pos[0] == "white":
                side = pos[1]
            else:
                side = pos[0]

            if right[pos[2]] == side:
                self.move(pos[2])
                self.move("yellow")
                for i in range(3):
                    self.move(pos[2])
            else:
                for i in range(3):
                    self.move(pos[2])
                for i in range(3):
                    self.move("yellow")
                self.move(pos[2])

        if pos[2] == "white" and not ((col1 == pos[0] and col2 == pos[1]) or (col1 == pos[1] and col2 == pos[2])):
            if right[pos[0]] == pos[1]:
                side = pos[1]
            else:
                side = pos[0]
            for i in range(3):
                self.move(side)
            for i in range(3):
                self.move("yellow")
            self.move(side)

        if pos[2] == "yellow":
            

            end = False
            while not end:
                pos = self.getCorner(col1, col2, white)
                correct = False
                for i in protect:
                    if (pos[0] == i[0] and pos[1] == i[1]) or (pos[0] == i[1] and pos[1] == i[0]):
                        correct = True

                if not correct:
                    break
                else:
                    self.move("yellow")

            pos = self.getCorner(col1, col2, white)

            if right[pos[0]] == pos[1]:
                left = pos[0]
            else:
                left = pos[1]
            self.move(left)
            self.move("yellow")
            self.move("yellow")
            self.move("yellow")
            self.move(left)
            self.move(left)
            self.move(left)

        pos = self.getCorner(col1, col2, white)

        if pos[0] == "yellow":
            side = pos[1]
        else:
            side = pos[0]

        if side == right[pos[2]]:
            type = "right"
        else:
            type = "left"

        if type == "right":
            if right[face_names[col1]] == face_names[col2]:
                moves = self.rot_calc_edge("yellow", pos[2], face_names[col1])
            else:
                moves = self.rot_calc_edge("yellow", pos[2], face_names[col2])
        else:
            if left[face_names[col1]] == face_names[col2]:
                moves = self.rot_calc_edge("yellow", pos[2], face_names[col1])
            else:
                moves = self.rot_calc_edge("yellow", pos[2], face_names[col2])

        for i in range(moves):
            self.move("yellow")

        if type == "right":
            m1 = 1
            m2 = 3
        else:
            m1 = 3
            m2 = 1

        pos = self.getCorner(col1, col2, white)

        if pos[0] == "yellow":
            side = pos[1]
        else:
            side = pos[0]

        for i in range(m2):
            self.move("yellow")
        for i in range(m2):
            self.move(side)
        for i in range(m1):
            self.move("yellow")
        for i in range(m1):
            self.move(side)

    #Inserts all the corners for the white face
    def insert_corners(self):
        protect = []

        self.insert_corner(green, red, protect)
        protect.append(["green", "red"])
        self.insert_corner(green, orange, protect)
        protect.append(["green", "orange"])
        self.insert_corner(blue, red, protect)
        protect.append(["blue", "red"])
        self.insert_corner(blue, orange, protect)
        protect.append(["blue", "orange"])

    #Inserts an edge to the second layer
    def insert_other_edge(self, col1, col2):
        pos = self.getEdge(col1, col2)
        
        if "yellow" in pos:
            if pos[1] == "yellow":
                t = [col1, pos[0]]
                b = [col2, pos[1]]
            else:
                t = [col2, pos[1]]
                b = [col1, pos[0]]

            m = self.rot_calc_edge("yellow", t[1], face_names[t[0]])
            
            for i in range(m):
                self.move("yellow")

            if self.rot_calc_edge("yellow", face_names[t[0]], face_names[b[0]]) == 1:
                for i in range(3):
                    self.move("yellow")
                for i in range(3):
                    self.move(face_names[b[0]])
                self.move("yellow")
                self.move(face_names[b[0]])
            else:
                self.move("yellow")
                self.move(face_names[b[0]])
                for i in range(3):
                    self.move("yellow")
                for i in range(3):
                    self.move(face_names[b[0]])

            protect = [["green", "red"], ["red", "blue"], ["blue", "orange"], ["orange", "green"]]
            if [face_names[col1], face_names[col2]] in protect:
                protect.remove([face_names[col1], face_names[col2]])
            else:
                protect.remove([face_names[col2], face_names[col1]])
            self.insert_corner(col1, col2, protect)

        else:
            if (pos[0] == face_names[col1] and pos[1] == face_names[col2]):
                return
            if self.rot_calc_edge("yellow", pos[0], pos[1]) == 1:
                f = pos[1]
            else:
                f = pos[0]
            
            for i in range(3):
                self.move(f)
            self.move("yellow")
            self.move(f)

            protect = [["green", "red"], ["red", "blue"], ["blue", "orange"], ["orange", "green"]]
            if [pos[0], pos[1]] in protect:
                protect.remove([pos[0], pos[1]])
            else:
                protect.remove([pos[1], pos[0]])

            self.insert_corner(face_names2[pos[0]], face_names2[pos[1]], protect)

            self.insert_other_edge(col1, col2)

    #Inserts all the edges to the second layer
    def insert_other_edges(self):
        self.insert_other_edge(blue, orange)
        self.insert_other_edge(red, green)
        self.insert_other_edge(green, orange)
        self.insert_other_edge(red, blue)

    #Solves the yellow cross
    def yellow_cross(self):
        up = [self.cube.faces["yellow"].squares[2][1].col1 == yellow,
              self.cube.faces["yellow"].squares[1][2].col1 == yellow,
              self.cube.faces["yellow"].squares[0][1].col1 == yellow,
              self.cube.faces["yellow"].squares[1][0].col1 == yellow]

        if not True in up:
            self.cross_algo("green")

        up = [self.cube.faces["yellow"].squares[2][1].col1 == yellow,
              self.cube.faces["yellow"].squares[1][2].col1 == yellow,
              self.cube.faces["yellow"].squares[0][1].col1 == yellow,
              self.cube.faces["yellow"].squares[1][0].col1 == yellow]
        
        if up[2] and up[3] and not up[0]:
            self.cross_algo("green")
        elif up[3] and up[0] and not up[1]:
            self.cross_algo("orange")
        elif up[0] and up[1] and not up[2]:
            self.cross_algo("blue")
        elif up[1] and up[2] and not up[3]:
            self.cross_algo("red")

        up = [self.cube.faces["yellow"].squares[2][1].col1 == yellow,
              self.cube.faces["yellow"].squares[1][2].col1 == yellow,
              self.cube.faces["yellow"].squares[0][1].col1 == yellow,
              self.cube.faces["yellow"].squares[1][0].col1 == yellow]

        if up[2] and up[0] and not up[1]:
            self.cross_algo("orange")
        elif up[1] and up[3] and not up[0]:
            self.cross_algo("green")

    def yellow_cross2(self):

        sides = [face_names[self.cube.faces["yellow"].squares[2][1].col2],
                 face_names[self.cube.faces["yellow"].squares[1][2].col2],
                 face_names[self.cube.faces["yellow"].squares[0][1].col2],
                 face_names[self.cube.faces["yellow"].squares[1][0].col2]]

        right = {"green" : "orange", "orange" : "blue", "blue" : "red", "red" : "green"}

        if not (sides[1] == right[sides[0]] and sides[2] == right[sides[1]] and sides[3] == right[sides[2]] and sides[0] == right[sides[3]]):

            if sides[0] == right[right[sides[2]]]:
                self.cross_algo2("green")
            elif sides[1] == right[right[sides[3]]]:
                self.cross_algo2("orange")

            sides = [face_names[self.cube.faces["yellow"].squares[2][1].col2],
                     face_names[self.cube.faces["yellow"].squares[1][2].col2],
                     face_names[self.cube.faces["yellow"].squares[0][1].col2],
                     face_names[self.cube.faces["yellow"].squares[1][0].col2]]

            if sides[1] == right[sides[0]]:
                self.cross_algo2("green")
            elif sides[2] == right[sides[1]]:
                self.cross_algo2("orange")
            elif sides[3] == right[sides[2]]:
                self.cross_algo2("blue")
            elif sides[0] == right[sides[3]]:
                self.cross_algo2("red")

        sides = [face_names[self.cube.faces["yellow"].squares[2][1].col2],
                 face_names[self.cube.faces["yellow"].squares[1][2].col2],
                 face_names[self.cube.faces["yellow"].squares[0][1].col2],
                 face_names[self.cube.faces["yellow"].squares[1][0].col2]]

        m = self.rot_calc_edge("yellow", "blue", sides[0])
        for i in range(m):
            self.move("yellow")

    #Yellow cross algorithm
    def cross_algo(self, col):
        right = {"green" : "orange", "orange" : "blue", "blue" : "red", "red" : "green"}
        self.move(col)
        self.move(right[col])
        self.move("yellow")
        for i in range(3):
            self.move(right[col])
        for i in range(3):
            self.move("yellow")
        for i in range(3):
            self.move(col)

    #Yellow cross algorithm 2
    def cross_algo2(self, col):
        right = {"green" : "orange", "orange" : "blue", "blue" : "red", "red" : "green"}
        self.move(right[col])
        self.move("yellow")
        self.move("yellow")
        for i in range(3):
            self.move(right[col])
        for i in range(3):
            self.move("yellow")
        self.move(right[col])
        for i in range(3):
            self.move("yellow")
        for i in range(3):
            self.move(right[col])

    #Solves the last corners
    def last_corners(self):
        correct = [self.check_corner(green, orange),
                   self.check_corner(orange, blue),
                   self.check_corner(blue, red),
                   self.check_corner(red, green)]

        if not True in correct:
            self.corner_algo("green")

        for i in range(2):
            correct = [self.check_corner(green, orange),
                       self.check_corner(orange, blue),
                       self.check_corner(blue, red), 
                       self.check_corner(red, green)]

            all = ["green", "orange", "blue", "red"]

            if not (correct[0] and correct[1] and correct[2] and correct[3]):
                index = 0
                for i in range(4):
                    if correct[i]:
                        index = i
                        break
                self.corner_algo(all[index])

        orient = [self.check_corner2(green, orange),
                  self.check_corner2(orange, blue),
                  self.check_corner2(blue, red),
                  self.check_corner2(red, green)]
        done = 0
        for i in orient:
            if i == "yellow":
                done += 1

        if done == 1:
            if orient[0] == "yellow":
                self.corner_algo2("blue")
            elif orient[1] == "yellow":
                self.corner_algo2("red")
            elif orient[2] == "yellow":
                self.corner_algo2("green")
            elif orient[3] == "yellow":
                self.corner_algo2("orange")

        orient = [self.check_corner2(green, orange),
                  self.check_corner2(orange, blue),
                  self.check_corner2(blue, red),
                  self.check_corner2(red, green)]
        done = 0
        for i in orient:
            if i == "yellow":
                done += 1

        if done == 0:
            if orient[0] == orient[1]:
                self.corner_algo2("green")
            elif orient[1] == orient[2]:
                self.corner_algo2("orange")
            elif orient[2] == orient[3]:
                self.corner_algo2("blue")
            elif orient[3] == orient[0]:
                self.corner_algo2("red")

        orient = [self.check_corner2(green, orange),
                  self.check_corner2(orange, blue),
                  self.check_corner2(blue, red),
                  self.check_corner2(red, green)]
        done = 0
        for i in orient:
            if i == "yellow":
                done += 1

        if done == 2:
            if orient[0] == "green" and orient[2] == "red":
                self.corner_algo2("blue")
            elif orient[0] == "orange" and orient[2] == "blue":
                self.corner_algo2("green")
            elif orient[1] == "orange" and orient[3] == "green":
                self.corner_algo2("red")
            elif orient[1] == "blue" and orient[3] == "red":
                self.corner_algo2("orange")
            elif orient[0] == "green" and orient[1] == "blue":
                self.corner_algo2("green")
            elif orient[1] == "orange" and orient[2] == "red":
                self.corner_algo2("orange")
            elif orient[2] == "blue" and orient[3] == "green":
                self.corner_algo2("blue")
            elif orient[3] == "red" and orient[0] == "orange":
                self.corner_algo2("red")

            orient = [self.check_corner2(green, orange),
                      self.check_corner2(orange, blue),
                      self.check_corner2(blue, red),
                      self.check_corner2(red, green)]
            done = 0
            for i in orient:
                if i == "yellow":
                    done += 1

            if orient[0] == orient[1] and not orient[0] == "yellow":
                self.corner_algo2("green")
            elif orient[1] == orient[2] and not orient[1] == "yellow":
                self.corner_algo2("orange")
            elif orient[2] == orient[3] and not orient[2] == "yellow":
                self.corner_algo2("blue")
            elif orient[3] == orient[0] and not orient[3] == "yellow":
                self.corner_algo2("red")

    #Corner Algorithms
    def check_corner(self, col1, col2):
        pos = self.getCorner(col1, col2, yellow)
        
        if face_names[col1] in pos and face_names[col2] in pos:
            return True
        return False

    def check_corner2(self, col1, col2):
        pos = self.getCorner(col1, col2, yellow)
        return pos[2]

    def corner_algo(self, col):
        right = {"green" : "orange", "orange" : "blue", "blue" : "red", "red" : "green"}
        left = {"green" : "red", "red" : "blue", "blue" : "orange", "orange" : "green"}

        for i in range(3):
            self.move(left[col])
        self.move("yellow")
        self.move(right[col])
        for i in range(3):
            self.move("yellow")
        self.move(left[col])
        self.move("yellow")
        for i in range(3):
            self.move(right[col])
        for i in range(3):
            self.move("yellow")

    def corner_algo2(self, col):
        right = {"green" : "orange", "orange" : "blue", "blue" : "red", "red" : "green"}
        left = {"green" : "red", "red" : "blue", "blue" : "orange", "orange" : "green"}

        self.move(right[col])
        self.move("yellow")
        self.move("yellow")
        for i in range(3):
            self.move(right[col])
        for i in range(3):
            self.move("yellow")
        self.move(right[col])
        for i in range(3):
            self.move("yellow")
        for i in range(3):
            self.move(right[col])

        for i in range(3):
            self.move(left[col])
        self.move("yellow")
        self.move("yellow")
        self.move(left[col])
        self.move("yellow")
        for i in range(3):
            self.move(left[col])
        self.move("yellow")
        self.move(left[col])

    #Checks for key events
    def event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if self.start:
                    self.shift_right()
                else:
                    self.left = -1
                    self.up = 0
            elif event.key == pygame.K_LEFT:
                if self.start:
                    self.shift_left()
                else:
                    self.left = 1
                    self.up = 0
            elif event.key == pygame.K_UP:
                self.up = 1
                self.left = 0
            elif event.key == pygame.K_DOWN:
                self.up = -1
                self.left = 0

            num = { "white" : 0, "green" : 1, "orange" : 2, "blue" : 3, "red" : 4, "yellow" : 5 }
            if event.key == pygame.K_1:
                self.cube.faces[self.cursor[0]].squares[self.cursor[1]][self.cursor[2]].col1 = white
                self.cube.update(self.cursor[0])
                self.now[num[self.cursor[0]]][self.cursor[1]][self.cursor[2]] = white
                self.shift_right()
            elif event.key == pygame.K_2:
                self.cube.faces[self.cursor[0]].squares[self.cursor[1]][self.cursor[2]].col1 = green
                self.cube.update(self.cursor[0])
                self.now[num[self.cursor[0]]][self.cursor[1]][self.cursor[2]] = green
                self.shift_right()
            elif event.key == pygame.K_3:
                self.cube.faces[self.cursor[0]].squares[self.cursor[1]][self.cursor[2]].col1 = orange
                self.cube.update(self.cursor[0])
                self.now[num[self.cursor[0]]][self.cursor[1]][self.cursor[2]] = orange
                self.shift_right()
            elif event.key == pygame.K_4:
                self.cube.faces[self.cursor[0]].squares[self.cursor[1]][self.cursor[2]].col1 = blue
                self.cube.update(self.cursor[0])
                self.now[num[self.cursor[0]]][self.cursor[1]][self.cursor[2]] = blue
                self.shift_right()
            elif event.key == pygame.K_5:
                self.cube.faces[self.cursor[0]].squares[self.cursor[1]][self.cursor[2]].col1 = red
                self.cube.update(self.cursor[0])
                self.now[num[self.cursor[0]]][self.cursor[1]][self.cursor[2]] = red
                self.shift_right()
            elif event.key == pygame.K_6:
                self.cube.faces[self.cursor[0]].squares[self.cursor[1]][self.cursor[2]].col1 = yellow
                self.cube.update(self.cursor[0])
                self.now[num[self.cursor[0]]][self.cursor[1]][self.cursor[2]] = yellow
                self.shift_right()

            if event.key == pygame.K_d and self.i < self.l:
                self.m = True
            if event.key == pygame.K_a and self.i > 0:
                self.m = True
                self.back = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.up = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.left = 0

    def trans_new(self, face, rot, dir):
        l = self.new[face]
        new_l = [[], [], [], []]

        for i in range(4):
            pos = (i - rot) % 4
            r = (l[i][1] + rot) % 4
            new_l[pos] = [l[i][0], r]

        return new_l[dir]

    #Solves the cube
    def solve(self):
        self.moves = []
        stats = []
        self.white_cross()
        self.short()
        #print(self.notes())
        stats.append(self.length())
        self.insert_corners()
        self.short()
        stats.append(self.length() - math.fsum(stats))
        self.insert_other_edges()
        self.short()
        stats.append(self.length() - math.fsum(stats))
        self.yellow_cross()
        self.yellow_cross2()
        self.last_corners()
        self.short()
        stats.append(self.length() - math.fsum(stats))
        
        #print(len(self.notes()), "moves.", self.notes())
        return stats

    def insert_edge2(self, col, solved):
        pos = self.getEdge(face_names2[col], white)

        if pos[0] == "white":
            self.move(pos[1])
            pos = self.getEdge(face_names2[col], white)
        elif pos[0] == "yellow":
            protect = [self.getEdge(face_names2[i], white)[0] for i in solved]
            while pos[1] in protect:
                self.move("yellow")
                pos = self.getEdge(face_names2[col], white)
            self.move(pos[1])
            pos = self.getEdge(face_names2[col], white)
        elif pos[1] == "white":
            self.move(pos[0])
            pos = self.getEdge(face_names2[col], white)

        
        rot = ["green", "orange", "blue", "red"]
        if not len(solved) == 0:
            reference = solved[0]
            wanted = (rot.index(reference) - rot.index(col)) % 4
            difference = (rot.index(self.getEdge(face_names2[reference], white)[0]) - 
                          rot.index(self.getEdge(face_names2[col], white)[0])) % 4
            rotations = (wanted - difference) % 4

            for i in range(rotations):
                self.move("white")

        while not pos[1] == "white": 
            self.move(pos[0])
            pos = self.getEdge(face_names2[col], white)

    def cross2(self):
        edges = ["green", "orange", "blue", "red"]
        record = [100000, []]
        for i in edges:
            edges2 = [n for n in edges if n != i]
            for j in edges2:
                edges3 = [n for n in edges2 if n != j]
                for k in edges3:
                    edges4 = [n for n in edges3 if n != k]
                    for l in edges4:
                        self.insert_edge2(i, [])
                        self.insert_edge2(j, [i])
                        self.insert_edge2(k, [i, j])
                        self.insert_edge2(l, [i, j, k])
                        self.short()
                        if self.length() < record[0]:
                            record = [self.length(), [i, j, k, l]]
                        back = self.moves.copy()
                        back.reverse()
                        for a in back:
                            for b in range(3):
                                self.move(a)
                        self.moves = []

        self.insert_edge2(record[1][0], [])
        self.insert_edge2(record[1][1], [record[1][0]])
        self.insert_edge2(record[1][2], [record[1][0], record[1][1]])
        self.insert_edge2(record[1][3], [record[1][0], record[1][1], record[1][2]])
        self.short()

        pos = self.getEdge(green, white)
        rotations = self.rot_calc_edge("white", pos[0], "green")
        for i in range(rotations):
            self.move("white")

    def move_corner_edge(self, corner):
        other = { 
                "green": ["orange", "blue"],
                "orange": ["blue", "red"],
                "blue": ["red", "green"],
                "red": ["green", "orange"],
                "yellow": ["", ""],
                "white": ["", ""]
                }

        posEdge = self.getEdge(face_names2[corner], face_names2[other[corner][0]])
        posCorner = self.getCorner(white, face_names2[corner], face_names2[other[corner][0]])

        if not "yellow" in posEdge and not "yellow" in posCorner:
            if other[posEdge[0]][0] == posEdge[1]:
                edge = posEdge[0]
            elif other[posEdge[1]][0] == posEdge[0]:
                edge = posEdge[1]
            self.execute(self.algorithms["algorithms"]["F2L"]["Out"], edge, "yellow")
            posEdge = self.getEdge(face_names2[corner], face_names2[other[corner][0]])
            posCorner = self.getCorner(white, face_names2[corner], face_names2[other[corner][0]])

    def insert_pair(self, col):
        self.move_corner_edge(col)
        alg, rot = self.check_cases (self.tran_F2L(self.algorithms["cases"]["F2L"], col))
        if not alg == "Done" and alg:
            for j in range(rot):
                self.move("yellow")
            self.execute(self.algorithms["algorithms"]["F2L"][alg], col, "yellow")

        done, rot = self.check_cases (self.tran_F2L(self.algorithms["cases"]["F2L"], col))
        return done

    def F2L(self):
        pairs = ["green", "orange", "blue", "red"]
        record = [100000, []]
        self.moves.append("seperator")
        index = len(self.moves)
        before = self.moves.copy()

        for i in pairs:
            pairs2 = [n for n in pairs if n != i]
            for j in pairs2:
                pairs3 = [n for n in pairs2 if n != j]
                for k in pairs3:
                    pairs4 = [n for n in pairs3 if n != k]
                    for l in pairs4:
                        #print(self.moves, "before")
                        self.insert_pair(i)
                        self.insert_pair(j)
                        self.insert_pair(k)
                        self.insert_pair(l)
                        self.short()
                        if self.length() < record[0]:
                            record = [self.length(), [i, j, k, l]]
                        back = self.moves[index:len(self.moves)].copy()
                        #print(self.moves, "after")
                        #print(back, "back")
                        back.reverse()
                        for a in back:
                            for b in range(3):
                                self.move(a)
                        self.moves = self.moves[0:index]

        self.insert_pair(record[1][0])
        self.insert_pair(record[1][1])
        self.insert_pair(record[1][2])
        self.insert_pair(record[1][3])

        self.moves.remove("seperator")

    def last_layer(self):
        algs = []
        #self.yellow_cross_lite()

        alg, rot = self.check_cases(self.tran_OLL(self.algorithms["cases"]["OLL"]))
        if not alg == "Done" and alg:
            self.execute(self.algorithms["algorithms"]["OLL"][alg], "blue", "yellow", rot)
        done, rot = self.check_cases(self.tran_OLL(self.algorithms["cases"]["OLL"]))
        algs.append([alg, done == "Done"])

        alg, rot = self.check_cases(self.tran_PLL(self.algorithms["cases"]["PLL"]))
        if not alg == "Done" and alg:
            self.execute(self.algorithms["algorithms"]["PLL"][alg], "blue", "yellow", rot)
        done, rot = self.check_cases(self.tran_PLL(self.algorithms["cases"]["PLL"]))
        algs.append([alg, done == "Done"])

        pos = self.getEdge(yellow, green)
        moves = self.rot_calc_edge("yellow", pos[1], "green")
        for i in range(moves):
            self.move("yellow")
        return algs

    

    def solve2(self):
        self.moves = []
        stats2 = []
        self.cross2()
        self.short()
        stats2.append(self.length())
        #self.insert_corners()
        self.short()
        stats2.append(self.length() - math.fsum(stats2))
        #self.insert_other_edges()
        self.F2L()
        self.short()
        stats2.append(self.length() - math.fsum(stats2))
        algs = self.last_layer()
        self.short()
        stats2.append(self.length() - math.fsum(stats2))

        #self.tran_F2L(self.algorithms["cases"]["F2L"], "red")
        algs = []
        
        return stats2, algs

    def solve_optimal(self):
        tran = {
            "green": { "white": "green", "green": "yellow", "orange": "orange", "blue": "white", "red": "red", "yellow": "blue" }
            }
        green_solver = Solver(Model.Cube())
        #self.cube.faces[]

    #Functions for shifting the marker's position
    def shift_right(self):
        tiles = { (0, 0) : (0, 1), (0, 1) : (0, 2), (0, 2) : (1, 0), (1, 0) : (1, 2), (1, 2) : (2, 0), (2, 0) : (2, 1), (2, 1) : (2, 2), (2, 2) : "last" }
        now = tiles[(self.cursor[1], self.cursor[2])]
        if now == "last":
            if self.cursor[0] == "white":
                self.x_rot = 0
                self.cursor = ["green", 0, 0]
            elif self.cursor[0] == "green":
                self.y_rot = 90
                self.cursor = ["orange", 0, 0]
            elif self.cursor[0] == "orange":
                self.y_rot = 180
                self.cursor = ["blue", 0, 0]
            elif self.cursor[0] == "blue":
                self.y_rot = 270
                self.cursor = ["red", 0, 0]
            elif self.cursor[0] == "red":
                self.y_rot = 0
                self.x_rot = 270
                self.cursor = ["yellow", 0, 0]
            elif self.cursor[0] == "yellow":
                try:
                    self.solve()
                    self.x_rot = 0
                    self.start = False
                    self.l = len(self.moves)
                    self.paint2(self.now)
                except:
                    self.paint2(self.now)
        else:
            self.cursor[1] = now[0]
            self.cursor[2] = now[1]

    def shift_left(self):
        tiles = { (2, 2) : (2, 1), (2, 1) : (2, 0), (2, 0) : (1, 2), (1, 2) : (1, 0), (1, 0) : (0, 2), (0, 2) : (0, 1), (0, 1) : (0, 0), (0, 0) : "last" }
        now = tiles[(self.cursor[1], self.cursor[2])]
        if now == "last":
            if self.cursor[0] == "green":
                self.x_rot = 90
                self.cursor = ["white", 2, 2]
            elif self.cursor[0] == "orange":
                self.y_rot = 0
                self.cursor = ["green", 2, 2]
            elif self.cursor[0] == "blue":
                self.y_rot = 90
                self.cursor = ["orange", 2, 2]
            elif self.cursor[0] == "red":
                self.y_rot = 180
                self.cursor = ["blue", 2, 2]
            elif self.cursor[0] == "yellow":
                self.cursor = ["red", 2, 2]
                self.x_rot = 0
                self.y_rot = 270
        else:
            self.cursor[1] = now[0]
            self.cursor[2] = now[1]

    #Checks if the cube is solved
    def is_solved(self):
        colors = [white, green, orange, blue, red, yellow]
        solved = True

        for i in range(len(self.cube.faces)):
            for j in list(self.cube.faces.values())[i].squares:
                for k in j:
                    if not k.col1 == colors[i]:
                        solved = False
                        break

        return solved

    def length(self):
        before = ""
        total = 0
        for i in self.moves:
            if not i == before:
                total += 1
                before = i
        return total
        
def main():
    cube = Model.Cube()
    solver = Solver(cube)
    solver.start = False
    """mix = []
    for i in range(random.randint(20, 50)):
        mix.append(random.choice(["white", "green", "orange", "blue", "red", "yellow"]))
    for i in mix:
        solver.move(i)
    solver.moves = []
    print(solver.solve2())
    solver.l = len(solver.moves)
    moves = solver.moves
    solver.solve()
    for i in mix:
        solver.move(i)
    solver.moves = moves
    """
    solver.paint2(testing[8])
    solver.solve2()
    solver.paint2(testing[8])
    solver.l = len(solver.moves)

    pygame.init()
    size = (800,600)
    display = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

    clock = pygame.time.Clock()

    gluPerspective(45, (size[0]/size[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10.0)
    glEnable(GL_DEPTH_TEST)
    
    while True:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for event in pygame.event.get():
            solver.event(event)

        solver.Open_GL_draw(display)
        solver.update()
        
            
        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    main()