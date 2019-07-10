import pygame_widgets
import files
import constants
from multidimensional_array import Multidimensional_array as Md_array


class Gamefield(pygame_widgets.Holder):
    def __init__(self, master):
        super().__init__(master)
        self.level = 0
        self.map_widgets = None

    def load_map(self, index):
        files.Textures.load(index)
        map_strings = files.load_map(index)
        self.move_resize([(self.master.surface.get_size()[i] - (map_strings.get_dimensions()[i] *
                                                                constants.SQUARE_SIZE)) // 2 for i in range(2)],
                         0, [map_strings.get_dimensions()[i] * constants.SQUARE_SIZE for i in range(2)], False)
        self.map_widgets = Md_array(map_strings.get_dimensions())
        for pos, field in map_strings.enumerated:
            self.map_widgets[pos] = pygame_widgets.Image(self, [pos[i] * constants.SQUARE_SIZE for i in range(2)],
                                                         [constants.SQUARE_SIZE for _ in range(2)],
                                                         image=files.Textures.wall if field == constants.CHAR_WALL
                                                         else files.Textures.point)
            if field != constants.CHAR_WALL:
                self.map_widgets[pos].attr.img_empty = files.Textures.empty
