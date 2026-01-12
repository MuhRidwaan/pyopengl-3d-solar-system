from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from lighting import setup_lighting
from objects import *
from config import PLANETS
import math

# ========== GLOBAL ==========
WIDTH, HEIGHT = 1024, 768
DEBUG = False 

# Kamera
camX, camY, camZ = 0, 20, 45 
yaw, pitch = 0, -30 

# State Animasi
angle = 0.0
paused = False
speed_scale = 0.5 

# Interaksi
hovered_planet = None
selected_planet = None 

# Mouse Control
mouseX, mouseY = 0, 0
mouseRotate = False
lastMouseX, lastMouseY = 0, 0

# ===========================

def init():
    glClearColor(0.02, 0.02, 0.05, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    
    setup_lighting()
    init_resources() 

def camera():
    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)
    
    lx = math.sin(rad_yaw) * math.cos(rad_pitch)
    ly = math.sin(rad_pitch)
    lz = -math.cos(rad_yaw) * math.cos(rad_pitch)
    
    gluLookAt(camX, camY, camZ,
              camX + lx, camY + ly, camZ + lz,
              0, 1, 0)

def project_planet_pos(x, y, z):
    model = glGetDoublev(GL_MODELVIEW_MATRIX)
    proj  = glGetDoublev(GL_PROJECTION_MATRIX)
    view  = glGetIntegerv(GL_VIEWPORT)
    
    try:
        sx, sy, sz = gluProject(x, y, z, model, proj, view)
        return sx, view[3] - sy
    except:
        return -100, -100

def display():
    global angle, hovered_planet

    # 1. Clear Buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # 2. Render Background Layer (Tanpa Depth Buffer)
    # Urutan: Nebula -> Gradient Background -> Stars
    draw_nebula()
    draw_background()
    draw_stars()  # Aktifkan kembali bintangnya
    
    glDisable(GL_BLEND)
    
    # 3. Setup Kamera 3D
    glLoadIdentity()
    camera()
    
    # 4. Render Matahari (Pusat Cahaya)
    glPushMatrix()
    glDisable(GL_LIGHTING) # Matahari tidak butuh lighting karena dia sumbernya
    glRotatef(angle * 5, 0, 1, 0) # Matahari berputar pelan
    draw_sphere(2.5, "sun.jpg")
    if 'draw_sun_glow' in globals(): draw_sun_glow() # Panggil jika ada di objects.py
    glEnable(GL_LIGHTING)
    glPopMatrix()

    # Posisikan lampu tepat di tengah matahari (0,0,0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])

    hovered_planet = None
    
    # 5. Render Planet dan Satelit
    for p in PLANETS:
        draw_orbit(p["distance"])
        
        glPushMatrix()
        
        # Posisi Orbit
        curr_angle = angle * p["speed"]
        px = math.cos(curr_angle) * p["distance"]
        pz = math.sin(curr_angle) * p["distance"]
        glTranslatef(px, 0, pz)

        # Simpan state untuk planet agar rotasi sendiri tidak mempengaruhi bulan
        glPushMatrix()
        glRotatef(angle * 20, 0, 1, 0)
        
        # Tambahkan efek Atmosfer (Visual upgrade)
        if p["name"] == "Earth" and 'draw_atmosphere' in globals():
            draw_atmosphere(p["radius"], (0.3, 0.5, 1.0))
            
        draw_sphere(p["radius"], p["texture"])
        glPopMatrix()

        # Render Satelit (Bulan)
        if "moons" in p and p["moons"]:
            for moon in p["moons"]:
                glPushMatrix()
                moon_angle = angle * moon["speed"]
                mx = math.cos(moon_angle) * moon["distance"]
                mz = math.sin(moon_angle) * moon["distance"]
                glTranslatef(mx, 0, mz)
                glRotatef(angle * 10, 0, 1, 0)
                draw_sphere(moon["radius"], moon["texture"])
                glPopMatrix()

        # Spesial: Cincin Saturnus
        if p["name"].lower() == "saturn":
            glPushMatrix()
            glRotatef(20, 1, 0, 0) # Miringkan cincin sedikit agar estetik
            draw_saturn_rings(
                inner_radius=p["radius"] * 1.4,
                outer_radius=p["radius"] * 2.2
            )
            glPopMatrix()
        
        # Deteksi Mouse (Hover)
        screen_x, screen_y = project_planet_pos(0, 0, 0)
        dist = math.hypot(screen_x - mouseX, screen_y - mouseY)
        
        if dist < 25: 
            hovered_planet = p
            # Selection ring diputar agar horizontal terhadap planet
            glPushMatrix()
            glRotatef(90, 1, 0, 0)
            draw_selection_ring(p["radius"])
            glPopMatrix()

        glPopMatrix()

    if not paused:
        angle += 0.01 * speed_scale 

    # 6. Render UI / HUD Layer (2D)
    begin_2d(WIDTH, HEIGHT)

    # --- Panel Guide ---
    draw_hud_panel(15, 20, 350, 120, "")
    draw_text(30, 100, "MISSION CONTROL", (0, 1, 1), GLUT_BITMAP_HELVETICA_18)
    draw_text(30, 75, "[W A S D] : Fly Navigation", (0.9, 0.9, 0.9), GLUT_BITMAP_9_BY_15)
    draw_text(30, 55, "[Q / E]   : Altitude Up/Down", (0.9, 0.9, 0.9), GLUT_BITMAP_9_BY_15)
    draw_text(30, 35, "[Mouse]   : Look Around (Middle)", (0.9, 0.9, 0.9), GLUT_BITMAP_9_BY_15)
    
    # --- Status System ---
    speed_text = f"SPEED: {speed_scale:.1f}x"
    color_speed = (0, 1, 0) if not paused else (1, 0, 0)
    status_x = WIDTH - 220
    draw_text(status_x, 60, f"SYSTEM: {'PAUSED' if paused else 'ACTIVE'}", color_speed, GLUT_BITMAP_9_BY_15)
    draw_text(status_x, 40, "[SPACE] : Toggle Pause", (0.7, 0.7, 0.7), GLUT_BITMAP_9_BY_15)
    draw_text(status_x, 20, f"[+ / -] : {speed_text}", (1, 1, 0), GLUT_BITMAP_9_BY_15)

    # Label Hover
    if hovered_planet and not selected_planet:
        draw_text(mouseX + 15, HEIGHT - mouseY - 5, hovered_planet['name'], (1, 1, 0))

    # --- Popup Info Planet ---
    if selected_planet:
        panel_w, panel_h = 450, 320 
        panel_x, panel_y = (WIDTH - panel_w) // 2, (HEIGHT - panel_h) // 2
        
        draw_hud_panel(panel_x, panel_y, panel_w, panel_h, selected_planet["name"])
        
        # Planet Preview 3D
        preview_size = 130 
        preview_x = panel_x + 30
        preview_y = panel_y + panel_h - preview_size - 60 
        draw_3d_planet_preview(preview_x, preview_y, preview_size, preview_size, 
                               selected_planet["texture"], angle * 0.5)

        # Stats
        text_x = panel_x + preview_size + 50
        start_y = panel_y + panel_h - 75
        draw_text(text_x, start_y, f"Radius   : {selected_planet['radius']} units", (0.7, 1.0, 1.0), GLUT_BITMAP_9_BY_15)
        draw_text(text_x, start_y - 25, f"Distance : {selected_planet['distance']} M km", (0.7, 1.0, 1.0), GLUT_BITMAP_9_BY_15)
        draw_text(text_x, start_y - 50, f"Speed    : {selected_planet['speed']} km/s", (0.7, 1.0, 1.0), GLUT_BITMAP_9_BY_15)
        
        # Line & Description
        separator_y = panel_y + 120
        glColor4f(1, 1, 1, 0.2)
        glBegin(GL_LINES)
        glVertex2f(panel_x + 30, separator_y); glVertex2f(panel_x + panel_w - 30, separator_y)
        glEnd()
        
        draw_text_wrapped(panel_x + 30, separator_y - 25, selected_planet["info"], panel_w - 60)
        draw_text(panel_x + 30, panel_y + 15, "[ESC] Close Data Stream", (1, 0.4, 0.4), GLUT_BITMAP_9_BY_15)

    end_2d()
    glutSwapBuffers()

def keyboard(key, x, y):
    global camX, camY, camZ, paused, speed_scale, selected_planet
    move_speed = 1.0
    
    if key == b'w': camZ -= move_speed
    if key == b's': camZ += move_speed
    if key == b'a': camX -= move_speed
    if key == b'd': camX += move_speed
    if key == b'q': camY += move_speed
    if key == b'e': camY -= move_speed
    
    if key == b' ': paused = not paused
    if key == b'\x1b': selected_planet = None 
    
    if key == b'+' or key == b'=': 
        speed_scale = min(5.0, speed_scale + 0.1)
    if key == b'-' or key == b'_': 
        speed_scale = max(0.0, speed_scale - 0.1)

def mouse_click(button, state, x, y):
    global mouseRotate, selected_planet, lastMouseX, lastMouseY
    
    if button == GLUT_MIDDLE_BUTTON:
        mouseRotate = (state == GLUT_DOWN)
        lastMouseX, lastMouseY = x, y
        
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if hovered_planet:
            selected_planet = hovered_planet
        else:
            selected_planet = None

def mouse_motion(x, y):
    global mouseX, mouseY, yaw, pitch, lastMouseX, lastMouseY
    
    mouseX = x
    mouseY = y 
    
    if mouseRotate:
        dx = x - lastMouseX
        dy = y - lastMouseY
        
        yaw += dx * 0.2
        pitch -= dy * 0.2
        pitch = max(-89, min(89, pitch))
        
        lastMouseX, lastMouseY = x, y

def passive_motion(x, y):
    global mouseX, mouseY
    mouseX = x
    mouseY = y

def reshape(w, h):
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / max(h, 1), 1, 200)
    glMatrixMode(GL_MODELVIEW)

def idle():
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"3D Solar System - Modern HUD Edition")
    
    init()
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse_click)
    glutMotionFunc(mouse_motion)
    glutPassiveMotionFunc(passive_motion)
    glutIdleFunc(idle)
    
    glutMainLoop()

if __name__ == "__main__":
    main()