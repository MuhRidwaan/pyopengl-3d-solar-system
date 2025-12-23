from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from lighting import setup_lighting
from objects import draw_sphere, init_textures, draw_orbit
from config import PLANETS

angle = 0.0

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    setup_lighting()
    init_textures()

def display():
    global angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(0, 10, 30,
              0, 0, 0,
              0, 1, 0)

    # ===== Matahari =====
    glPushMatrix()
    draw_sphere(2, "sun.jpg")
    glPopMatrix()

    # ===== Orbit =====
    for planet in PLANETS:
        draw_orbit(planet["distance"])

    # ===== Planet =====
    for planet in PLANETS:
        glPushMatrix()
        glRotatef(angle * planet["speed"], 0, 1, 0)
        glTranslatef(planet["distance"], 0, 0)
        draw_sphere(planet["radius"], planet["texture"])
        glPopMatrix()

    # 🔑 angle NAIK SEKALI PER FRAME
    angle += 0.03

    # 🔑 swap buffer SEKALI DI AKHIR
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / max(h, 1), 1, 100)
    glMatrixMode(GL_MODELVIEW)

def idle():
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Animasi 3D Tata Surya - PyOpenGL")

    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
