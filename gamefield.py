import pygame_widgets
import entities
import files
import constants
from exceptions import FileFormatError
from multidimensional_array import Multidimensional_array as Md_array
from pygame_widgets.constants import THECOLORS
from pygame_widgets.auxiliary import cursors
from pygame.time import set_timer
from pygame import event


class Gamefield(pygame_widgets.Holder):
    def __init__(self, master):
        super().__init__(master)
        self.lives = constants.LIVES
        self.levels = files.number_of_levels()
        self.level = 0
        self.goal = 0
        self.map_widgets = None
        self.pampuch = None
        self.monsters = list()
        self.restarting = False
        self.label_info = pygame_widgets.Label(self, visible=False, font="trebuchet_ms", font_size=60, alignment_x=1,
                                               alignment_y=1, font_color=THECOLORS['white'], bold=True, italic=True,
                                               cursor=cursors.invisible)
        self.add_handler(constants.E_GAME_STARTED, self._game_started, self_arg=False, event_arg=False)

    def _game_started(self):
        set_timer(constants.E_GAME_STARTED, 0)
        self.restart() if self.restarting else self.pause(False)

    def start_game(self, level):
        self.level = level
        self.load_map(level)

    def info(self, death=True):
        x, y = self.master_rect.size
        self.label_info.move_resize((0, (y - (x // constants.LABEL_RATIO)) // 2), 0, (x, x // constants.LABEL_RATIO),
                                    False)
        self.label_info.set(background=files.Textures.label_lose_bg if death else files.Textures.label_win_bg,
                            text="Game over" if death else "You have won!", visible=True)

    def load_map(self, index):
        self.pampuch = None
        self.monsters = list()
        self.goal = 0
        files.Textures.load(index)
        map_strings = files.load_map(index)
        self.move_resize([(self.master.surface.get_size()[i] - (map_strings.get_dimensions()[i] *
                                                                constants.SQUARE_SIZE)) // 2 for i in range(2)],
                         0, [map_strings.get_dimensions()[i] * constants.SQUARE_SIZE for i in range(2)], False)
        self.map_widgets = Md_array(map_strings.get_dimensions())
        for pos, field in map_strings.enumerated:
            self.map_widgets[pos] = pygame_widgets.Image(self, [pos[i] * constants.SQUARE_SIZE for i in range(2)],
                                                         [constants.SQUARE_SIZE for _ in range(2)],
                                                         cursor=cursors.invisible)
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
                self.goal += 1
            if field == constants.CHAR_PAMPUCH:
                if self.pampuch is not None:
                    raise FileFormatError('Pampuch must be instanced exactly once per level', level_index=index)
                self.pampuch = pos
            elif field == constants.CHAR_MONSTER:
                self.monsters.append(pos)
        try:
            self.pampuch = entities.Pampuch(self, self.pampuch)
        except FileFormatError as error:
            error.level_index = index
            raise error
        else:
            self.pampuch.attr.img_dead = files.Textures.dead
        for index, pos in enumerate(self.monsters):
            self.monsters[index] = entities.Monster(self, pos, self.pampuch)
        for m in self.monsters:
            others = self.monsters.copy()
            others.remove(m)
            m.colleagues = others
        self.children = self.children[1:] + self.children[:1]
        self.pause(True)
        set_timer(constants.E_GAME_STARTED, constants.INSPECTION)

    def pause(self, value=None):
        if value is None:
            return self.pampuch.pause
        for e in self.monsters + [self.pampuch]:
            e.pause(value)

    def death(self):
        self.pause(True)
        event.post(event.Event(constants.E_DEATH))
        self.pampuch.set(image=self.pampuch.attr.img_dead)
        self.restarting = True
        set_timer(constants.E_GAME_STARTED, constants.INSPECTION)

    def restart(self):
        self.restarting = False
        self.lives -= 1
        if self.lives:
            self.pampuch.reset_image()
            self.pampuch.move_resize(self.pampuch.starting_position, 0)
            self.pampuch.direction = None
            for m in self.monsters:
                m.move_resize(m.starting_position, 0)
                m.direction = None
            set_timer(constants.E_GAME_STARTED, constants.INSPECTION)
            return
        self.info()

    def level_completed(self):
        self.pause(True)
        self.level += 1
        if self.level == self.levels:
            self.info(False)
            return
        for child in self.children[:-1]:
            child.delete()
        del self.children[:-1]
        self.map_widgets = None
        self.pampuch = None
        self.monsters = list()
        self.load_map(self.level)
