from OpenGL.GL import *
from PIL import Image
import os

def load_texture(filename):
    path = os.path.join("textures", filename)
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGB").tobytes()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB,
        image.width, image.height,
        0, GL_RGB, GL_UNSIGNED_BYTE, img_data
    )

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id
