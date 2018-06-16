from colorconsole import terminal
import Model

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random

blue = Model.blue
green = Model.green
red = Model.red
orange = Model.orange
yellow = Model.yellow
white = Model.white

face_names = ["white", "green", "orange", "blue", "red", "yellow"]
face_names2 = {white : "white", green : "green", orange : "orange", blue : "blue", red : "red", yellow : "yellow"}
face_names3 = {"white" : white, "green" : green, "orange" : orange, "blue" : blue, "red" : red, "yellow" : yellow}
console_to_open_GL = {1 : (0, 0, 1), 2 : (0, 1, 0), 4 : (1, 0, 0), 13 : (1, 0.5, 0), 14 : (1, 1, 0), 15 : (1, 1, 1)}

screen = terminal.get_terminal(conEmu=False)

now = """
www
www
www
ggg
ggg
ybo
ooo
ooo
yob
bbb
bbb
ygr
rrr
rrr
gro
ryy
yyy
gyb
"""

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
    def __init__(self, cube):
        self.cube = cube

        self.moveMode = "face"

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

    def setMode(self, mode):
        self.moveMode = mode

    def move(self, m):
        if self.moveMode == "face":
            self.cube.rotate(m)
            self.moves.append(m)

    def short(self):
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

        self.moves = moves

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
                notation.append(i[0][0].upper() + "`")

        return " ".join(notation)

    def draw(self):
        x = 0
        y = 0
        for i in self.cube.faces.items():
            h = i[1]
            for j in h.squares:
                for l in j:
                    screen.set_color(0, l.col1)
                    screen.print_at(x, y, "  ")
                    x += 2

                y += 1
                x = 0
            y += 2
        screen.set_color(15, 0)

    def Open_GL_draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        self.DrawFaceFront(1.5, self.cube.faces["green"].squares, "green", self.r)
        self.DrawFaceBack(-1.5, self.cube.faces["blue"].squares, "blue", self.r)

        self.DrawFaceLeft(-1.5, self.cube.faces["orange"].squares, "orange", self.r)
        self.DrawFaceRight(1.5, self.cube.faces["red"].squares, "red", self.r)

        self.DrawFaceTop(1.5, self.cube.faces["white"].squares, "white", self.r)
        self.DrawFaceBottom(-1.5, self.cube.faces["yellow"].squares, "yellow", self.r)

        if not (self.up == 0 and self.left == 0):

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

    def update(self):
        if self.m:
            if not self.r:
                self.tripl = False
                if not self.back:
                    if self.i + 2 < self.l:
                        if self.moves[self.i] == self.moves[self.i + 1] and self.moves[self.i] == self.moves[self.i + 2]:
                            self.r = Rotation(self.moves[self.i], -1)
                            self.tripl = True
                        else:
                            self.r = Rotation(self.moves[self.i], 1)
                    else:
                        self.r = Rotation(self.moves[self.i], 1)
                else:
                    if self.i - 3 >= 0:
                        if self.moves[self.i - 1] == self.moves[self.i - 2] and self.moves[self.i - 1] == self.moves[self.i - 3]:
                            self.r = Rotation(self.moves[self.i - 1], 1)
                            self.tripl = True
                        else:
                            self.r = Rotation(self.moves[self.i - 1], -1)
                    else:
                        self.r = Rotation(self.moves[self.i - 1], -1)
            
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

    def DrawFaceFront(self, z, tiles, facecolor, rotation):
        colors = []
        for row in tiles:
            for tile in row:
                colors.append(tile.col1)

        tilenum = 0
        for ycorner in (0.5, -0.5, -1.5):
            for xcorner in (-1.5, -0.5, 0.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                glColor3f(*console_to_open_GL[colors[tilenum]])
                glVertex3fv((xcorner+self.offset, ycorner+self.offset, z))
                glVertex3fv((xcorner+(1-self.offset), ycorner+self.offset, z))
                glVertex3fv((xcorner+(1-self.offset), ycorner+(1-self.offset), z))
                glVertex3fv((xcorner+self.offset, ycorner+(1-self.offset), z))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1
                
    def DrawFaceBack(self, z, tiles, facecolor, rotation):
        colors = []
        for row in tiles:
            for tile in row:
                colors.append(tile.col1)

        tilenum = 0
        for ycorner in (0.5, -0.5, -1.5):
            for xcorner in (0.5, -0.5, -1.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                glColor3f(*console_to_open_GL[colors[tilenum]])
                glVertex3fv((xcorner+self.offset, ycorner+self.offset, z))
                glVertex3fv((xcorner+(1-self.offset), ycorner+self.offset, z))
                glVertex3fv((xcorner+(1-self.offset), ycorner+(1-self.offset), z))
                glVertex3fv((xcorner+self.offset, ycorner+(1-self.offset), z))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1

    # Function for generating left and right faces (x is fixed)
    def DrawFaceLeft(self, x, tiles, facecolor, rotation):
        colors = []
        for row in tiles:
            for tile in row:
                colors.append(tile.col1)

        tilenum = 0
        for ycorner in (0.5, -0.5, -1.5):
            for zcorner in (-1.5, -0.5, 0.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                glColor3f(*console_to_open_GL[colors[tilenum]])
                glVertex3fv((x, ycorner+self.offset, zcorner+self.offset))
                glVertex3fv((x, ycorner+self.offset, zcorner+(1-self.offset)))
                glVertex3fv((x, ycorner+(1-self.offset), zcorner+(1-self.offset)))
                glVertex3fv((x, ycorner+(1-self.offset), zcorner+self.offset))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1

    def DrawFaceRight(self, x, tiles, facecolor, rotation):
        colors = []
        for row in tiles:
            for tile in row:
                colors.append(tile.col1)

        tilenum = 0
        for ycorner in (0.5, -0.5, -1.5):
            for zcorner in (0.5, -0.5, -1.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                glColor3f(*console_to_open_GL[colors[tilenum]])
                glVertex3fv((x, ycorner+self.offset, zcorner+self.offset))
                glVertex3fv((x, ycorner+self.offset, zcorner+(1-self.offset)))
                glVertex3fv((x, ycorner+(1-self.offset), zcorner+(1-self.offset)))
                glVertex3fv((x, ycorner+(1-self.offset), zcorner+self.offset))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1

    # Function for generating top and bottom faces (y is fixed)
    def DrawFaceTop(self, y, tiles, facecolor, rotation):
        colors = []
        for row in tiles:
            for tile in row:
                colors.append(tile.col1)

        tilenum = 0
        for zcorner in (-1.5, -0.5, 0.5):
            for xcorner in (-1.5, -0.5, 0.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                glColor3f(*console_to_open_GL[colors[tilenum]])
                glVertex3fv((xcorner+self.offset, y, zcorner+self.offset))
                glVertex3fv((xcorner+(1-self.offset), y, zcorner+self.offset))
                glVertex3fv((xcorner+(1-self.offset), y, zcorner+(1-self.offset)))
                glVertex3fv((xcorner+self.offset, y, zcorner+(1-self.offset)))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1

    def DrawFaceBottom(self, y, tiles, facecolor, rotation):
        colors = []
        for row in tiles:
            for tile in row:
                colors.append(tile.col1)

        tilenum = 0
        for zcorner in (0.5, -0.5, -1.5):
            for xcorner in (-1.5, -0.5, 0.5):
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPushMatrix()
                        rotation.apply_rotation()
                glBegin(GL_POLYGON)
                glColor3f(*console_to_open_GL[colors[tilenum]])
                glVertex3fv((xcorner+self.offset, y, zcorner+self.offset))
                glVertex3fv((xcorner+(1-self.offset), y, zcorner+self.offset))
                glVertex3fv((xcorner+(1-self.offset), y, zcorner+(1-self.offset)))
                glVertex3fv((xcorner+self.offset, y, zcorner+(1-self.offset)))
                glEnd()
                if rotation:
                    if rotation.should_rotate(facecolor, tilenum):
                        glPopMatrix()
                tilenum += 1

    def paint(self, c):
        lines = now.split()

        faces = [[], [], [], [], [], []]

        j = 0
        for i in range(len(faces)):
            face = faces[i]
            j = i * 2
            j += i

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
        move = self.rot_calc_edge("yellow", pos[1], face_names2[color])
        
        for i in range(move):
            self.move("yellow")

        for i in redo[::-1]:
            self.move(i)
            self.move(i)
            self.move(i)

        self.move(face_names2[color])
        self.move(face_names2[color])


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
                self.move(pos[2])
                self.move(pos[2])
                self.move(pos[2])
            else:
                self.move(pos[2])
                self.move(pos[2])
                self.move(pos[2])
                self.move("yellow")
                self.move("yellow")
                self.move("yellow")
                self.move(pos[2])

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
            if right[face_names2[col1]] == face_names2[col2]:
                moves = self.rot_calc_edge("yellow", pos[2], face_names2[col1])
            else:
                moves = self.rot_calc_edge("yellow", pos[2], face_names2[col2])
        else:
            if left[face_names2[col1]] == face_names2[col2]:
                moves = self.rot_calc_edge("yellow", pos[2], face_names2[col1])
            else:
                moves = self.rot_calc_edge("yellow", pos[2], face_names2[col2])

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

    def insert_other_edge(self, col1, col2):
        pos = self.getEdge(col1, col2)
        
        if "yellow" in pos:
            if pos[1] == "yellow":
                t = [col1, pos[0]]
                b = [col2, pos[1]]
            else:
                t = [col2, pos[1]]
                b = [col1, pos[0]]

            m = self.rot_calc_edge("yellow", t[1], face_names2[t[0]])
            
            for i in range(m):
                self.move("yellow")

            if self.rot_calc_edge("yellow", face_names2[t[0]], face_names2[b[0]]) == 1:
                for i in range(3):
                    self.move("yellow")
                for i in range(3):
                    self.move(face_names2[b[0]])
                self.move("yellow")
                self.move(face_names2[b[0]])
            else:
                self.move("yellow")
                self.move(face_names2[b[0]])
                for i in range(3):
                    self.move("yellow")
                for i in range(3):
                    self.move(face_names2[b[0]])

            protect = [["green", "red"], ["red", "blue"], ["blue", "orange"], ["orange", "green"]]
            if [face_names2[col1], face_names2[col2]] in protect:
                protect.remove([face_names2[col1], face_names2[col2]])
            else:
                protect.remove([face_names2[col2], face_names2[col1]])
            self.insert_corner(col1, col2, protect)

        else:
            if (pos[0] == face_names2[col1] and pos[1] == face_names2[col2]) or (pos[0] == face_names2[col2] and pos[1] == face_names2[col1]):
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

            self.insert_corner(face_names3[pos[0]], face_names3[pos[1]], protect)

            self.insert_other_edge(col1, col2)

    def insert_other_edges(self):
        self.insert_other_edge(blue, orange)
        self.insert_other_edge(red, green)
        self.insert_other_edge(green, orange)
        self.insert_other_edge(red, blue)

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

        sides = [face_names2[self.cube.faces["yellow"].squares[2][1].col2],
                 face_names2[self.cube.faces["yellow"].squares[1][2].col2],
                 face_names2[self.cube.faces["yellow"].squares[0][1].col2],
                 face_names2[self.cube.faces["yellow"].squares[1][0].col2]]

        right = {"green" : "orange", "orange" : "blue", "blue" : "red", "red" : "green"}

        if not (sides[1] == right[sides[0]] and sides[2] == right[sides[1]] and sides[3] == right[sides[2]] and sides[0] == right[sides[3]]):

            if sides[0] == right[right[sides[2]]]:
                self.cross_algo2("green")
            elif sides[1] == right[right[sides[3]]]:
                self.cross_algo2("orange")

            sides = [face_names2[self.cube.faces["yellow"].squares[2][1].col2],
                     face_names2[self.cube.faces["yellow"].squares[1][2].col2],
                     face_names2[self.cube.faces["yellow"].squares[0][1].col2],
                     face_names2[self.cube.faces["yellow"].squares[1][0].col2]]

            if sides[1] == right[sides[0]]:
                self.cross_algo2("green")
            elif sides[2] == right[sides[1]]:
                self.cross_algo2("orange")
            elif sides[3] == right[sides[2]]:
                self.cross_algo2("blue")
            elif sides[0] == right[sides[3]]:
                self.cross_algo2("red")

        m = self.rot_calc_edge("yellow", sides[0], "blue")
        for i in range(m):
            self.move("yellow")

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

    def event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.left = -1
                self.up = 0
            elif event.key == pygame.K_LEFT:
                self.left = 1
                self.up = 0
            elif event.key == pygame.K_UP:
                self.up = 1
                self.left = 0
            elif event.key == pygame.K_DOWN:
                self.up = -1
                self.left = 0

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

    def start_loop(self):
        self.short()
        self.l = len(self.moves)
        self.paint(now)

def main():
    cube = Model.Cube()
    solver = Solver(cube)

    pygame.init()
    size = (800,600)
    display = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

    clock = pygame.time.Clock()

    gluPerspective(45, (size[0]/size[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10.0)
    glEnable(GL_DEPTH_TEST)

    solver.paint(now)

    #solver.white_cross()
    #solver.insert_corners()
    #solver.insert_other_edges()

    solver.yellow_cross()
    
    solver.short()

    solver.start_loop()
    
    while True:
        for event in pygame.event.get():
            solver.event(event)
            
                

        solver.Open_GL_draw()
        solver.update()
        
            
        clock.tick(60)
        pygame.display.flip()

if __name__ == "__main__":
    main()