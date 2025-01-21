import pygame as pg
from OpenGL.GL import *
import numpy as np

class App: 

    def __init__(self):

        # initialize python
        pg.init()
        # create a window
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
        # this clock object will be used to control the framerate 
        self.clock = pg.time.Clock()
        # initialize opengl
        glClearColor(0.5, 0.5, 0.5, 1)
        self.mainLoop()

    def mainLoop(self):

        running = True
        while (running):
            # check for events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            # refresh the screen 
            glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()

            # timing
            self.clock.tick(60)
        self.quit()

    def quit(self):

        pg.quit()


# Make a tri class
class Triangle: 

    def __init__(self):
        #  pass in x, y, z, r, g, b 
        self.vertices = (
            -0.5, -0.5, 0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0, 0.0, 1.0, 0.0,
            0.0, 0.5, 0, 0.0, 0.0, 1.0
        )

        # OpenGL needs a 32-bit float point decimal, otherwise OpenGL will not read the vertex data properly. Also won't generate any errors to tell you that it's not working. Allegedly. Lol 
        # Numpy will use 64-bit floating points 
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 3

        # VAO = 
        # VBO = vertex buffer object. A storage container 
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)


# entry point
if __name__ == "__main__":
    myApp = App()