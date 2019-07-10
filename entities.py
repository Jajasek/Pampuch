import pygame_widgets
import constants
import files
from exceptions import FileFormatError


class Entity(pygame_widgets.Image):
    play = False

    @classmethod
    def start(cls):
        cls.play = True

    @classmethod
    def stop(cls):
        cls.play = False

    def __init__(self, master, pos, image):
        super().__init__(master, [pos[i] * constants.SQUARE_SIZE for i in range(2)],
                         [constants.SQUARE_SIZE for _ in range(2)], image=image)
        self.direction = None


class Pampuch(Entity):
    _instanced = False

    def __init__(self, master, pos):
        if Pampuch._instanced or pos is None:
            raise FileFormatError('Pampuch must be instanced exactly once per level')
        Pampuch._instanced = True
        Entity.__init__(self, master, pos, files.Textures.pampuch)


class Monster(Entity):
    def __init__(self, master, pos):
        Entity.__init__(self, master, pos, files.Textures.monster)
