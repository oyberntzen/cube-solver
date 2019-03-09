import numpy as np
import cv2

import pygame
from pygame.locals import *

import math
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
import Model
import solver


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Interval:
    def __init__(self, min, max):
        self.min = []
        for i in min:
            if i > 255: self.min.append(255)
            elif i < 0: self.min.append(0)
            else: self.min.append(i)
        self.max = []
        for i in max:
            if i > 255: self.max.append(255)
            elif i < 0: self.max.append(0)
            else: self.max.append(i)
        self.num = 1

    def add(self):
        self.num += 1
        
    def change(self, rgb):
        if self.min[0] > rgb[0]:
            self.min[0] = rgb[0]
        if self.min[1] > rgb[1]:
            self.min[1] = rgb[1]
        if self.min[2] > rgb[2]:
            self.min[2] = rgb[2]
        if self.max[0] < rgb[0]:
            self.max[0] = rgb[0]
        if self.max[1] < rgb[1]:
            self.max[1] = rgb[1]
        if self.max[2] < rgb[2]:
            self.max[2] = rgb[2]

    def is_in(self, rgb):
        if rgb[0] >= self.min[0] and rgb[0] <= self.max[0] and \
            rgb[1] >= self.min[1] and rgb[1] <= self.max[1] and \
            rgb[2] >= self.min[2] and rgb[2] <= self.max[2]:
            return True
        return False

    def is_near(self, rgb, threshold):
        if rgb[0] > self.min[0] - threshold and rgb[0] < self.max[0] + threshold and \
            rgb[1] > self.min[1] - threshold and rgb[1] < self.max[1] + threshold and \
            rgb[2] > self.min[2] - threshold and rgb[2] < self.max[2] + threshold:
            return True
        return False

    def average(self):
        return [(self.min[i] + self.max[i]) / 2 for i in range(3)]

    def lab(self):
        return convert_color(sRGBColor(self.average()[0], self.average()[1], self.average()[2], True), LabColor).get_value_tuple()

    def difference(self, interval):
        score = 0
        this = self.lab()
        other = interval.lab()
        
        return math.pow(this[0] - other[0], 2) + math.pow(this[1] - other[1], 2) + math.pow(this[2] - other[2], 2)
     
class Config:
    def __init__(self, width, height):
        self.state = "pictures"

        self.size = 300
        self.res = 50

        self.x = int((width - self.size) / 2)
        self.y = int((height - self.size) / 2)
        self.width = width
        self.height = height

        self.current_face = 0
        self.total_faces = 6
        self.sides = [[0, 3, 4, 1, 2], [1, 0, 4, 5, 2], [2, 0, 1, 5, 3], [3, 0, 2, 5, 4], [4, 0, 3, 5, 1], [5, 1, 4, 3, 2]]
        self.colors = [(255, 255, 255), (0, 255, 0), (255, 255 / 2, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0), (0, 0, 0)]
        self.color_size = self.size / 6
        self.positions = [(self.x + (self.size / 3) * 1.25, self.y + (self.size / 3) * 1.25), 
                     (self.x + (self.size / 3) * 1.25, self.y - (self.size / 3) * 0.75), 
                     (self.x + self.size + (self.size / 3) * 0.25, self.y + (self.size / 3) * 1.25), 
                     (self.x + (self.size / 3) * 1.25, self.y + self.size + (self.size / 3) * 0.25), 
                     (self.x - (self.size / 3) * 0.75, self.y + (self.size / 3) * 1.25)]

        self.images = [pygame.surface.Surface((self.size, self.size)) for i in range(self.total_faces)]
        self.face_data = []
        self.color_data = []
        self.guess_data = []

        self.cube = None
        self.solver3d = None
        self.id = None

        self.threshold = 3.5

        self.cap = cv2.VideoCapture(0)

        self.canvas = pygame.surface.Surface((width, height))
        self.image = None
        self.tiles = [pygame.surface.Surface((self.res / 3, self.res / 3)) for i in range(9)]

    def saveFace(self, imagebad):
        image = pygame.surface.Surface((self.width, self.height))
        image.blit(imagebad, (0, 0), (0, 60, self.width, self.height))

        self.images[self.current_face].blit(image, (0, 0), (self.x, self.y, self.size, self.size))
        self.images[self.current_face] = pygame.transform.scale(self.images[self.current_face], (self.res, self.res))

        for i in range(3):
            for j in range(3):
                self.tiles[i * 3 + j].blit(self.images[self.current_face], (0, 0), (i * self.res / 3, j * self.res / 3, self.res / 3, self.res / 3))
    
        color_intervals = []
        for tile in self.tiles:
            pixels = pygame.pixelarray.PixelArray(tile)
            intervals = []
            for px in pixels:
                for py in px:
                    color = tile.unmap_rgb(py)
                    done = False

                    for interval in intervals:
                        if interval.is_in(color):
                            interval.add()
                            done = True

                    if not done:
                        for interval in intervals:
                            if interval.is_near(color, self.threshold):
                                interval.add()
                                interval.change(color)
                                done = True

                    if not done:
                        intervals.append(Interval([color[0] - self.threshold, color[1] - self.threshold, color[2] - self.threshold], [color[0] + self.threshold, color[1] + self.threshold, color[2] + self.threshold]))

            record = 0
            interval = None
            for i in intervals:
                if i.num > record:
                    record = i.num
                    interval = i
            color_intervals.append(interval)
        self.face_data.append(color_intervals)
        self.color_data.append(color_intervals[4])

    def guess(self):
        for face in self.face_data:
            tile_colors = [[None for i in range(3)] for j in range(3)]

            for tile in range(len(face)):
                best_score = 100000
                i = None
                j = 0
                for interval in self.color_data:
                    score = face[tile].difference(interval)
                    if score < best_score:
                        best_score = score
                        i = j
                    j += 1
                tile_colors[tile % 3][int(tile / 3)] = i
            self.guess_data.append(tile_colors)

    def texid(self, pyimage):
        texData = pygame.image.tostring(pyimage, "RGBA", 1)
        w = pyimage.get_width()
        h = pyimage.get_height()

        glEnable(GL_TEXTURE_2D)
        id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, texData)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
        return id

    def drawid(self):
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2fv((-1, -1))
        glTexCoord2f(1, 0)
        glVertex2fv((1, -1))
        glTexCoord2f(1, 1)
        glVertex2fv((1, 1))
        glTexCoord2f(0, 1)
        glVertex2fv((-1, 1))
        glEnd()

    def solve(self):
        glDeleteTextures([self.id])
        self.cube = Model.Cube()
        self.solver3d = solver.Solver(self.cube)
        self.solver3d.start = False
        print(self.guess_data)
        try:
            self.solver3d.paint2(self.guess_data)
            self.solver3d.solve2()
            self.solver3d.l = len(self.solver3d.moves)
            self.solver3d.paint2(self.guess_data)
            gluPerspective(45, (self.width / self.height), 0.1, 50.0)
            glTranslatef(0.0, 0.0, -10.0)
            glEnable(GL_DEPTH_TEST) 
        except:
            self.__init__(self.width, self.height)

    def event(self, event):
        if self.solver3d:
            self.solver3d.event(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.state == "pictures":
                    self.saveFace(self.image)
                    if self.current_face < self.total_faces - 1:
                        self.current_face += 1
                    else:
                        self.guess()
                        self.state = "guess"
                        self.cap.release() 
                elif self.state == "guess":
                    self.state = "solve"
                    self.solve()

    def update(self, canvas3d):
        if self.state == "pictures":
            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            self.image = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], "RGB")
            self.canvas.blit(self.image, (0, 0), (0, 60, self.width, self.height))

            for i in range(self.x, self.x + self.size - int(self.size / 3) + 1, int(self.size / 3)):
                for j in range(self.y, self.y + self.size - int(self.size / 3) + 1, int(self.size / 3)):
                    pygame.draw.rect(self.canvas, (0, 0, 0), (i, j, self.size / 3, self.size / 3), 3)

            for i in range(len(self.sides[self.current_face])):
                pygame.draw.rect(self.canvas, self.colors[self.sides[self.current_face][i]], (*self.positions[i], self.color_size, self.color_size))

        elif self.state == "guess":
            self.canvas.fill((0, 0, 0))

            for i in range(self.total_faces):
                self.canvas.blit(self.images[i], (i * self.res, 0))
                for j in range(3):
                    for k in range(3):
                        pygame.draw.rect(self.canvas, self.face_data[i][j * 3 + k].min, (i * self.res + j * (self.res / 3), self.res + k * (self.res / 3), self.res / 6, self.res / 3))
                        pygame.draw.rect(self.canvas, self.face_data[i][j * 3 + k].max, (i * self.res + j * (self.res / 3) + self.res / 6, self.res + k * (self.res / 3), self.res / 6, self.res / 3))
                        pygame.draw.rect(self.canvas, self.color_data[self.guess_data[i][j][k]].average(), (i * self.res + j * (self.res / 3), self.res + k * (self.res / 3), self.res / 3, self.res / 3))

        if not self.state == "solve":
            self.id = self.texid(self.canvas)
            self.drawid()
        else:
            self.solver3d.Open_GL_draw(canvas3d)
            self.solver3d.update()

def main():
    pygame.init()

    width = 640
    height = 360
    canvas3d = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    done = False
    config = Config(width, height)

    while not done:
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for event in pygame.event.get():
            config.event(event)
            if event.type == pygame.QUIT:
                done = True

        config.update(canvas3d)
        pygame.display.flip()
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()