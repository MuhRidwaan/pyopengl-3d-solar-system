from OpenGL.GL import *
from OpenGL.GLU import *
from texture import load_texture
import math

textures = {}

def init_textures():
    files = [
        "sun.jpg","mercury.jpg","venus.jpg","earth.jpg","mars.jpg",
        "jupiter.jpg","saturn.jpg","uranus.jpg","neptune.jpg"
    ]
    for f in files:
        textures[f] = load_texture(f)

def draw_sphere(radius, texture):
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    glBindTexture(GL_TEXTURE_2D, textures[texture])
    gluSphere(quad, radius, 40, 40)
    gluDeleteQuadric(quad)

def draw_orbit(radius):
    glDisable(GL_LIGHTING)
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_LINE_LOOP)

    for i in range(120):
        theta = 2 * math.pi * i / 120
        x = math.cos(theta) * radius
        z = math.sin(theta) * radius
        glVertex3f(x, 0, z)

    glEnd()
    glEnable(GL_LIGHTING)
