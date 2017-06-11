blue = 1
green = 2
red = 4
orange = 13
yellow = 14
white = 15

class Cube():
    def __init__(self):
        self.white_face = Face(white, blue, red, green, orange)
        self.green_face = Face(green, white, red, yellow, orange)
        self.orange_face = Face(orange, white, green, yellow, blue)
        self.blue_face = Face(blue, white, orange, yellow, red)
        self.red_face = Face(red, white, blue, yellow, green)
        self.yellow_face = Face(yellow, green, red, blue, orange)

        self.faces = {}

        self.faces["white"] = self.white_face
        self.faces["green"] = self.green_face
        self.faces["orange"] = self.orange_face
        self.faces["blue"] = self.blue_face
        self.faces["red"] = self.red_face
        self.faces["yellow"] = self.yellow_face

    def rotate(self, face):
        self.faces[face].rotate()
        self.update(face)

    def update(self, face):
        if face == "white":
            self.blue_face.squares[0] = self.white_face.take("top")[::-1]
            self.red_face.squares[0] = self.white_face.take("right", "side_bot")[::-1]
            self.green_face.squares[0] = self.white_face.take("bottom")
            self.orange_face.squares[0] = self.white_face.take("left", "side_bot")

        elif face == "yellow":
            self.blue_face.squares[2] = self.yellow_face.take("bottom")[::-1]
            self.red_face.squares[2] = self.yellow_face.take("right", "side_bot")
            self.green_face.squares[2] = self.yellow_face.take("top")
            self.orange_face.squares[2] = self.yellow_face.take("left", "side_bot")[::-1]

        elif face == "green":
            self.white_face.squares[2] = self.green_face.take("top")
            self.yellow_face.squares[0] = self.green_face.take("bottom")
            self.red_face.sided("left", self.green_face.take("right"))
            self.orange_face.sided("right", self.green_face.take("left"))

        elif face == "orange":
            self.white_face.sided("left", self.orange_face.take("top"), "take")
            self.yellow_face.sided("left", self.orange_face.take("bottom")[::-1], "take")
            self.green_face.sided("left", self.orange_face.take("right"))
            self.blue_face.sided("right", self.orange_face.take("left"))

        elif face == "blue":
            self.white_face.squares[0] = self.blue_face.take("top")[::-1]
            self.yellow_face.squares[2] = self.blue_face.take("bottom")[::-1]
            self.orange_face.sided("left", self.blue_face.take("right")[::1])
            self.red_face.sided("right", self.blue_face.take("left"))

        elif face == "red":
            self.white_face.sided("right", self.red_face.take("top")[::-1], "take")
            self.yellow_face.sided("right", self.red_face.take("bottom"), "take")
            self.blue_face.sided("left", self.red_face.take("right"))
            self.green_face.sided("right", self.red_face.take("left"))

    def paint(self, face, new):
        f = self.faces[face]

        

        for y in range(len(f.squares)):
            row = f.squares[y]
            for x in range(len(row)):
                n = new[y][x]
                o = row[x]

                #print(row)

                o.col1 = n

        self.update(face)

class Face():
    def __init__(self, col, top, rigth, bottom, left):
        self.squares = [
            (Corner(col, top, left),    Edge(col, top),    Corner(col, top, rigth)   ),
            (Edge(col, left),           Center(col),       Edge(col, rigth)          ),
            (Corner(col, bottom, left), Edge(col, bottom), Corner(col, bottom, rigth))
            ]

        self.top = top
        self.right = rigth
        self.bottom = bottom
        self.left = left

    def rotate(self):
        row1 = self.squares[0]
        row2 = self.squares[1]
        row3 = self.squares[2]

        self.squares = [
            (row3[0].rotate(), row2[0], row1[0].rotate()),
            (row3[1],          row2[1], row1[1]         ),
            (row3[2].rotate(), row2[2], row1[2].rotate())
            ]
        
    def take(self, place, extra = "side"):
        new = ()

        row1 = self.squares[0]
        row2 = self.squares[1]
        row3 = self.squares[2]

        if place == "top":
            new = (row1[0].switch("up"), row1[1].switch(), row1[2].switch("up"))

        elif place == "right":
            new = (row1[2].switch(extra), row2[2].switch(), row3[2].switch(extra))

        elif place == "bottom":
            new = (row3[0].switch("up"), row3[1].switch(), row3[2].switch("up"))

        elif place == "left":
            new = (row1[0].switch(extra), row2[0].switch(), row3[0].switch(extra))

        return new

    def sided(self, side, tuple, extra = "none"):
        row1 = self.squares[0]
        row2 = self.squares[1]
        row3 = self.squares[2]

        new_row1 = ()
        new_row2 = ()
        new_row3 = ()

        if side == "right":
            new_row1 = (row1[0], row1[1], tuple[0].switch(extra))
            new_row2 = (row2[0], row2[1], tuple[1])
            new_row3 = (row3[0], row3[1], tuple[2].switch(extra))
        elif side == "left":
            new_row1 = (tuple[0].switch(extra), row1[1], row1[2])
            new_row2 = (tuple[1], row2[1], row2[2])
            new_row3 = (tuple[2].switch(extra), row3[1], row3[2])

        self.squares = [new_row1, new_row2, new_row3]

class Center():
    def __init__(self, col1):
        self.col1 = col1

class Edge():
    def __init__(self, col1, col2):
        self.col1 = col1
        self.col2 = col2

    def switch(self):
        return Edge(self.col2, self.col1)

class Corner():
    def __init__(self, col1, col2, col3):
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3

    def rotate(self):
        temp = self.col2
        self.col2 = self.col3
        self.col3 = temp
        return self
    
    def switch(self, dir):
        if dir == "up":
            return Corner(self.col2, self.col1, self.col3)
        elif dir == "side_bot":
            return Corner(self.col3, self.col1, self.col2)
        elif dir == "side":
            return Corner(self.col3, self.col2, self.col1)
        elif dir == "take":
            return Corner(self.col1, self.col3, self.col2)
        else:
            return self