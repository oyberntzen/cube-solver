# Rubik's Cube Solver

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
    - [The Model (Model.py)](#the-model-(model.py))

---

## About

This is a project that I have been working on for some years. This repository includes:
- A rubik's cube model/simulation for calculating how the cube looks like when you make a move
- A rubik's cube solver that can calculate which moves that should be done to solve the cube
- A 3D representation of the rubik's cube that can visualize the moves that need to be done
- A camera program that can find out which colors that are on the cube faces

The program is made in python using [pygame](https://www.pygame.org/), [pyopengl](http://pyopengl.sourceforge.net/), [cv2](https://github.com/skvark/opencv-python), [numpy](http://www.numpy.org/) and [colormath](https://python-colormath.readthedocs.io/en/latest/)

---

## Installation

1. Install python 3 from https://www.python.org/downloads/
2. Install the dependencies with [pypi](https://pypi.org/). Run the commands in terminal:
    - `pip install numpy`
    - `pip install cv2`
    - `pip install colormath`
    - `pip install pygame`
    - `pip install pyopengl`
3. Clone the repository using `git clone https://github.com/oyberntzen/cube-solver.git` or you can download the zip
4. Now the Rubik's Cube Solver is installed and you can scroll down to see more information about how the different programs work

---

## Usage

### The model ([Model.py](https://github.com/oyberntzen/cube-solver/blob/master/Model.py))

This program is a simulation and it calculates how the Rubik's cube will look like if you make a move. Here is an example:
```python
import Model

cube = Model.Cube()

cube.rotate("green")
cube.rotate("yellow")
```