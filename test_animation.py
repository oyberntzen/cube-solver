import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random

# Color table for the tiles
colors = {
    "red"   :  (1.0, 0, 0),
    "green" :  (0, 1.0, 0),
    "blue"  :  (0, 0, 1.0),
    "white" :  (1.0, 1.0, 1.0),
    "orange":  (1.0, 0.5, 0),
    "yellow":  (1.0, 1.0, 0),
}

# Space between each tile
offset = 0.1

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

# Class representing the individual tile
class Tile:
    def __init__(self, color):
        self.color = color

# Function for generating front and back faces (z is fixed)
def DrawFaceFront(z, tiles, facecolor, rotation):
    tilenum = 0
    for ycorner in (0.5, -0.5, -1.5):
        for xcorner in (-1.5, -0.5, 0.5):
            if rotation.should_rotate(facecolor, tilenum):
                glPushMatrix()
                rotation.apply_rotation()
            glBegin(GL_POLYGON)
            glColor3f(*tiles[tilenum].color)
            glVertex3fv((xcorner+offset, ycorner+offset, z))
            glVertex3fv((xcorner+(1-offset), ycorner+offset, z))
            glVertex3fv((xcorner+(1-offset), ycorner+(1-offset), z))
            glVertex3fv((xcorner+offset, ycorner+(1-offset), z))
            glEnd()
            if rotation.should_rotate(facecolor, tilenum):
                glPopMatrix()
            tilenum += 1

def DrawFaceBack(z, tiles, facecolor, rotation):
    tilenum = 0
    for ycorner in (0.5, -0.5, -1.5):
        for xcorner in (0.5, -0.5, -1.5):
            if rotation.should_rotate(facecolor, tilenum):
                glPushMatrix()
                rotation.apply_rotation()
            glBegin(GL_POLYGON)
            glColor3f(*tiles[tilenum].color)
            glVertex3fv((xcorner+offset, ycorner+offset, z))
            glVertex3fv((xcorner+(1-offset), ycorner+offset, z))
            glVertex3fv((xcorner+(1-offset), ycorner+(1-offset), z))
            glVertex3fv((xcorner+offset, ycorner+(1-offset), z))
            glEnd()
            if rotation.should_rotate(facecolor, tilenum):
                glPopMatrix()
            tilenum += 1

# Function for generating left and right faces (x is fixed)
def DrawFaceLeft(x, tiles, facecolor, rotation):
    tilenum = 0
    for ycorner in (0.5, -0.5, -1.5):
        for zcorner in (-1.5, -0.5, 0.5):
            if rotation.should_rotate(facecolor, tilenum):
                glPushMatrix()
                rotation.apply_rotation()
            glBegin(GL_POLYGON)
            glColor3f(*tiles[tilenum].color)
            glVertex3fv((x, ycorner+offset, zcorner+offset))
            glVertex3fv((x, ycorner+offset, zcorner+(1-offset)))
            glVertex3fv((x, ycorner+(1-offset), zcorner+(1-offset)))
            glVertex3fv((x, ycorner+(1-offset), zcorner+offset))
            glEnd()
            if rotation.should_rotate(facecolor, tilenum):
                glPopMatrix()
            tilenum += 1

def DrawFaceRight(x, tiles, facecolor, rotation):
    tilenum = 0
    for ycorner in (0.5, -0.5, -1.5):
        for zcorner in (0.5, -0.5, -1.5):
            if rotation.should_rotate(facecolor, tilenum):
                glPushMatrix()
                rotation.apply_rotation()
            glBegin(GL_POLYGON)
            glColor3f(*tiles[tilenum].color)
            glVertex3fv((x, ycorner+offset, zcorner+offset))
            glVertex3fv((x, ycorner+offset, zcorner+(1-offset)))
            glVertex3fv((x, ycorner+(1-offset), zcorner+(1-offset)))
            glVertex3fv((x, ycorner+(1-offset), zcorner+offset))
            glEnd()
            if rotation.should_rotate(facecolor, tilenum):
                glPopMatrix()
            tilenum += 1

# Function for generating top and bottom faces (y is fixed)
def DrawFaceTop(y, tiles, facecolor, rotation):
    tilenum = 0
    for zcorner in (-1.5, -0.5, 0.5):
        for xcorner in (-1.5, -0.5, 0.5):
            if rotation.should_rotate(facecolor, tilenum):
                glPushMatrix()
                rotation.apply_rotation()
            glBegin(GL_POLYGON)
            glColor3f(*tiles[tilenum].color)
            glVertex3fv((xcorner+offset, y, zcorner+offset))
            glVertex3fv((xcorner+(1-offset), y, zcorner+offset))
            glVertex3fv((xcorner+(1-offset), y, zcorner+(1-offset)))
            glVertex3fv((xcorner+offset, y, zcorner+(1-offset)))
            glEnd()
            if rotation.should_rotate(facecolor, tilenum):
                glPopMatrix()
            tilenum += 1

def DrawFaceBottom(y, tiles, facecolor, rotation):
    tilenum = 0
    for zcorner in (0.5, -0.5, -1.5):
        for xcorner in (-1.5, -0.5, 0.5):
            if rotation.should_rotate(facecolor, tilenum):
                glPushMatrix()
                rotation.apply_rotation()
            glBegin(GL_POLYGON)
            glColor3f(*tiles[tilenum].color)
            glVertex3fv((xcorner+offset, y, zcorner+offset))
            glVertex3fv((xcorner+(1-offset), y, zcorner+offset))
            glVertex3fv((xcorner+(1-offset), y, zcorner+(1-offset)))
            glVertex3fv((xcorner+offset, y, zcorner+(1-offset)))
            glEnd()
            if rotation.should_rotate(facecolor, tilenum):
                glPopMatrix()
            tilenum += 1

def main():
    pygame.init()
    display = (1024,768)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glEnable(GL_DEPTH_TEST)


    # Choose an initial face to rotate
    color_picker = ["red", "white", "orange", "blue", "green", "yellow"]
    r = Rotation(random.choice(color_picker))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glRotatef(1, 1, 1, 1)

        DrawFaceFront(1.5, [Tile(colors["green"])] * 9, "green", r)
        DrawFaceBack(-1.5, [Tile(colors["blue"])] * 9, "blue", r)

        DrawFaceLeft(-1.5, [Tile(colors["orange"])] * 9, "orange", r)
        DrawFaceRight(1.5, [Tile(colors["red"])] * 9, "red", r)

        DrawFaceTop(1.5, [Tile(colors["white"])] * 9, "white", r)
        DrawFaceBottom(-1.5, [Tile(colors["yellow"])] * 9, "yellow", r)

        r.rotate()
        if r.completed:
            r = Rotation(random.choice(color_picker))

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
