from OpenGL.GL import *

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Material agar objek bereaksi terhadap cahaya tapi tetap mempertahankan warna tekstur
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Posisi cahaya (Matahari ada di 0,0,0)
    # 4th parameter 1.0 berarti Positional Light (bukan Directional)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])
    
    # Ambient: Cahaya dasar redup agar sisi gelap tidak hitam total
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    
    # Diffuse: Warna cahaya matahari (Putih Terang)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.2, 1.2, 1.2, 1.0])
    
    # Specular: Kilau pada planet
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])