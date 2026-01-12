from OpenGL.GL import *

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Memastikan tekstur tetap terlihat jelas di bawah pencahayaan
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Posisi cahaya di tengah Matahari (0,0,0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])
    
    # 1. AMBIENT: Dibuat sedikit kebiruan agar sisi gelap planet 
    # terkesan memantulkan cahaya dari nebula/latar belakang.
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.05, 0.05, 0.1, 1.0])
    
    # 2. DIFFUSE: Cahaya matahari dibuat sedikit hangat (warna krem/putih gading) 
    # agar tidak terlalu "flat" putihnya.
    # glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.3, 1.25, 1.1, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.5, 1.5, 1.5, 1.0])
    
    # 3. SPECULAR: Memberikan efek pantulan cahaya pada permukaan planet yang licin (seperti air di Bumi)
    # glLightfv(GL_LIGHT0, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.02, 0.02, 0.05, 1.0])

    # 4. ATTENUATION (Opsional): Membuat cahaya meredup secara alami sesuai jarak
    # Semakin jauh planet, semakin redup cahayanya.
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.005)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0001)