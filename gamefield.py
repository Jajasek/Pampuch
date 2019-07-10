import pygame_widgets
import entities
import files
import constants
from exceptions import FileFormatError
from multidimensional_array import Multidimensional_array as Md_array


class Gamefield(pygame_widgets.Holder):
    def __init__(self, master):
        super().__init__(master)
        self.level = 0
        self.goal = 0
        self.map_widgets = None
        self.pampuch = None
        self.monsters = list()

    def load_map(self, index):
        files.Textures.load(index)
        map_strings = files.load_map(index)
        self.move_resize([(self.master.surface.get_size()[i] - (map_strings.get_dimensions()[i] *
                                                                constants.SQUARE_SIZE)) // 2 for i in range(2)],
                         0, [map_strings.get_dimensions()[i] * constants.SQUARE_SIZE for i in range(2)], False)
        self.map_widgets = Md_array(map_strings.get_dimensions())
        for pos, field in map_strings.enumerated:
            self.map_widgets[pos] = pygame_widgets.Image(self, [pos[i] * constants.SQUARE_SIZE for i in range(2)],
                                                         [constants.SQUARE_SIZE for _ in range(2)])
            if field == constants.CHAR_WALL:
                self.map_widgets[pos].attr.type = 'wall'
                self.map_widgets[pos].set(image=files.Textures.wall)
            elif field == constants.CHAR_EMPTY:
                self.map_widgets[pos].attr.type = 'empty'
                self.map_widgets[pos].set(image=files.Textures.empty)
            else:
                self.map_widgets[pos].attr.img_empty = files.Textures.empty
                self.map_widgets[pos].attr.type = 'point'
                self.map_widgets[pos].set(image=files.Textures.point)
            if field == constants.CHAR_PAMPUCH:
                self.pampuch = pos
            elif field == constants.CHAR_MONSTER:
                self.monsters.append(pos)
        try:
            self.pampuch = entities.Pampuch(self, self.pampuch)
        except FileFormatError as error:
            error.level_index = index
            raise error
        for index, pos in enumerate(self.monsters):
            self.monsters[index] = entities.Monster(self, pos)
