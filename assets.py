import os
import pygame

class AssetManager:
    def __init__(self):
        self.images = {}
        self.fonts = {}
        self.sounds = {}
        self.base_path = ''

    def set_base_path(self, path):
        self.base_path = path

    def load_image(self, name, path, scale=None, alpha=True):
        full = os.path.join(self.base_path, path)
        img = pygame.image.load(full)
        img = img.convert_alpha() if alpha else img.convert()
        if scale is not None:
            img = pygame.transform.scale(img, scale)
        self.images[name] = img
        return img

    def get_image(self, name):
        return self.images.get(name)

    def load_font(self, name, path=None, size=24):
        if path:
            font = pygame.font.Font(os.path.join(self.base_path, path), size)
        else:
            font = pygame.font.Font(None, size)
        self.fonts[name] = font
        return font

    def get_font(self, name):
        return self.fonts.get(name)

    def make_surface(self, w, h, color):
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill(color)
        return s

    def clear(self):
        self.images.clear()
        self.fonts.clear()
        self.sounds.clear()