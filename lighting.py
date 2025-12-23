from OpenGL.GL import *

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    light_position = [0, 0, 0, 1]
    light_ambient  = [0.2, 0.2, 0.2, 1]
    light_diffuse  = [1, 1, 1, 1]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
