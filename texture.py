from OpenGL.GL import *
from PIL import Image
import os

def load_texture(filename):
 
    path = os.path.join("textures", filename)
    
    try:
        img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
    except IOError:
        print(f"ERROR: Tidak dapat memuat tekstur {filename}. Pastikan file ada di folder 'textures'.")
        return None

    data = img.convert("RGB").tobytes()
    
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    
    # Pengaturan agar tekstur bisa di-scale dengan halus
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    
    return tex