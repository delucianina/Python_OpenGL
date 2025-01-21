import pygame as pg
from OpenGL.GL import *

class Aoo: 

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
                if (event.type == pg.quit):
                    running = False
            # refresh the screen 
            glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()

            # timing
            self.clock.tick(60)