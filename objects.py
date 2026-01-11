from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from texture import load_texture
import math
import random

textures = {}
quadric = None
star_positions = []

def init_resources():
    """ Memuat semua resource (texture & setup quadric) """
    global quadric
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    
    # Load textures
    texture_files = ["sun.jpg", "mercury.jpg", "venus.jpg", "earth.jpg", "mars.jpg",
                     "jupiter.jpg", "saturn.jpg", "uranus.jpg", "neptune.jpg"]
    
    print("Loading Textures...")
    for f in texture_files:
        textures[f] = load_texture(f)
        
    # Generate random stars
    for _ in range(200):
        x = random.uniform(-50, 50)
        y = random.uniform(-30, 30)
        z = random.uniform(-50, -10)
        star_positions.append((x, y, z))

def draw_stars():
    """ Menggambar latar belakang bintang sederhana """
    glDisable(GL_LIGHTING)
    glPointSize(1.5)
    glColor3f(1, 1, 1)
    glBegin(GL_POINTS)
    for pos in star_positions:
        glVertex3fv(pos)
    glEnd()
    glEnable(GL_LIGHTING)

def draw_sphere(radius, texture_name):
    """ Menggambar planet/matahari dengan tekstur """
    if texture_name in textures and textures[texture_name]:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textures[texture_name])
        glColor3f(1, 1, 1) 
    else:
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.5, 0.5, 0.5) 
        
    gluSphere(quadric, radius, 40, 40)
    glDisable(GL_TEXTURE_2D)

def draw_orbit(r):
    """ Menggambar garis lintasan orbit """
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glColor4f(0.3, 0.3, 0.3, 0.5)
    glBegin(GL_LINE_LOOP)
    segments = 100
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        x = r * math.cos(theta)
        z = r * math.sin(theta)
        glVertex3f(x, 0, z)
    glEnd()
    glEnable(GL_LIGHTING)

def draw_selection_ring(r):
    """ Lingkaran cyan saat planet di-hover """
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST) 
    glColor3f(0.0, 1.0, 1.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    segments = 40
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        x = (r + 0.2) * math.cos(theta)
        y = (r + 0.2) * math.sin(theta)
        glVertex3f(x, y, 0)
    glEnd()
    glLineWidth(1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

# ================= UI / HUD SYSTEM =================

def begin_2d(w, h):
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def end_2d():
    glDisable(GL_BLEND)
    
    # PERBAIKAN: Pastikan kita berada di mode MODELVIEW sebelum pop
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    
    # Kembalikan ke ModelView untuk render scene 3D berikutnya
    glMatrixMode(GL_MODELVIEW)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def draw_text(x, y, text, color=(1, 1, 1), font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for c in text:
        glutBitmapCharacter(font, ord(c))

def draw_text_wrapped(x, y, text, max_width_px, line_height=20, color=(0.8, 0.8, 0.8)):
    """ 
    Render text dengan wrapping otomatis yang lebih akurat.
    """
    words = text.split(" ")
    line = ""
    current_y = y
    
    # PERBAIKAN: Gunakan lebar font yang lebih akurat (9px untuk 9_BY_15)
    # Ditambah sedikit buffer (0.5) agar tidak terlalu mepet pinggir
    char_width = 9.5 
    
    for word in words:
        test_line = line + word + " "
        # Cek apakah panjang baris melebihi batas lebar panel
        if len(test_line) * char_width > max_width_px:
            draw_text(x, current_y, line, color, GLUT_BITMAP_9_BY_15)
            line = word + " "
            current_y -= line_height
        else:
            line = test_line
            
    # Gambar sisa baris terakhir
    draw_text(x, current_y, line, color, GLUT_BITMAP_9_BY_15)

def draw_hud_panel(x, y, w, h, title=""):
    """ Menggambar Panel Info dengan style kaca gelap + border """
    glColor4f(0.05, 0.05, 0.1, 0.90) 
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()

    if title:
        header_h = 35
        glColor4f(0.0, 0.5, 0.6, 0.6) 
        glBegin(GL_QUADS)
        glVertex2f(x, y + h - header_h)
        glVertex2f(x + w, y + h - header_h)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()
        draw_text(x + 15, y + h - 25, title.upper(), (1, 1, 1), GLUT_BITMAP_HELVETICA_18)

    glLineWidth(2)
    glColor4f(0.0, 1.0, 1.0, 0.5)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()
    glLineWidth(1)

def draw_3d_planet_preview(x, y, w, h, texture_name, angle):
    """
    MENGGAMBAR PLANET 3D ASLI DI DALAM HUD 2D.
    """
    prev_viewport = glGetIntegerv(GL_VIEWPORT)

    # Set Viewport Khusus
    glViewport(int(x), int(y), int(w), int(h))

    # Masuk ke Mode Proyeksi 3D
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    # PERBAIKAN: Gunakan FOV 30 agar distorsi lebih minim dan planet terlihat 'solid'
    gluPerspective(30, w/h, 0.1, 100.0)

    # Masuk ke Mode ModelView
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # PERBAIKAN: Mundurkan kamera sedikit (z=5.0) agar planet tidak terlalu penuh sesak di viewport
    gluLookAt(0, 0, 5.0,  0, 0, 0,  0, 1, 0)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    
    glClear(GL_DEPTH_BUFFER_BIT)

    # Gambar Planet
    glPushMatrix()
    # Rotasi planet
    glRotatef(angle * 50, 0, 1, 0) 
    glRotatef(-20, 1, 0, 0)
    
    draw_sphere(1.2, texture_name)
    glPopMatrix()

    # Restore State
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    # Restore Viewport Asli
    glViewport(prev_viewport[0], prev_viewport[1], prev_viewport[2], prev_viewport[3])
    
    # Gambar Border di sekitar planet
    glDisable(GL_TEXTURE_2D)
    glColor4f(0, 1, 1, 0.5)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x+w, y)
    glVertex2f(x+w, y+h)
    glVertex2f(x, y+h)
    glEnd()
    glLineWidth(1)