#  --------------------------------------------------------------------------------------------
#  --------------------------------------------------------------------------------------------
#  --------------------------------------------------------------------------------------------
# IMPORTS
import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader


#  --------------------------------------------------------------------------------------------
#  Create a class for the app
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
        self.shader = self.createShader("shaders/vertex.txt",
                                        "shaders/fragment.txt")
        glUseProgram(self.shader)
        self.triangle = Triangle()
        self.mainLoop()

    def createShader(self, vertexFilepath, fragmentFilepath):

        # with open will automatically close the file when this block ends. Allows reusability
        with open(vertexFilepath, 'r') as f:
            # f.readlines will dump all the contents of the file as a single string
            vertex_src = f.readlines()

        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER))

        return shader

    def mainLoop(self):

        running = True
        while (running):
            # check for events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            # refresh the screen
            glClear(GL_COLOR_BUFFER_BIT)

            # reset the self.shader. Best practice for when the program gets larger
            glUseProgram(self.shader)
            #  prepare VAO for drawing
            glBindVertexArray(self.triangle.vao)
            # Look inside VAO and read data to draw with
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)

            pg.display.flip()

            # timing
            self.clock.tick(60)
        self.quit()

    def quit(self):
        #  free the VBO and VAO
        self.triangle.destroy()
        # free the program (shader)
        glDeleteProgram(self.shader)
        pg.quit()


#  --------------------------------------------------------------------------------------------
# Make a tri class
class Triangle:

    def __init__(self):
        #  pass in x, y, z, r, g, b
        self.vertices = (-0.5, -0.5, 0, 1.0, 0.0, 0.0, 0.5, -0.5, 0, 0.0, 1.0,
                         0.0, 0.0, 0.5, 0, 0.0, 0.0, 1.0)

        # OpenGL needs a 32-bit float point decimal, otherwise OpenGL will not read the vertex data properly. Also won't generate any errors to tell you that it's not working. Allegedly.
        # Numpy will use 64-bit floating points by default
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 3

        # VAO =
        # VBO = vertex buffer object. A storage container
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices,
                     GL_STATIC_DRAW)
        # ------- DESCRIBE ATTRIBUTES IN VBO ------- #
        # Enable an attriubutes for position (0) and color (1, a few lines down):
        glEnableVertexAttribArray(0)
        # 0 is position; number of points in each attribute is 3 (for both XYZ and RGB); GL_FLOAT is the data type; declare whether OpenGL will need to do any work to normalize numbers (bool); stride is the number of bytes the program needs to move to get to the next position/color (24 because each vertex has 6 numbers and each number has 4 bytes); pointer is the offset of the first element in the array
        #  WHY CTYPES: function signature expects a void pointer, but no Python type works there, so ctypes save us
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        # Attribute for color:
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24,
                              ctypes.c_void_p(12))

    # Free the allocated memory on GPU when exiting the program
    def destroy(self):
        # Expects list of things to delete, so wrap in list type (even when only one item)
        glDeleteVertexArrays(1, (self.vao, ))
        glDeleteBuffers(1, (self.vbo, ))


#  --------------------------------------------------------------------------------------------
# entry point
if __name__ == "__main__":
    myApp = App()
