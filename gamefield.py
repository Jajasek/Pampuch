import pygame_widgets
import entities
import files
import constants
import time
from exceptions import FileFormatError
from MyLib.multidimensional_array import Multidimensional_array as Md_array
from shared_data import Game_state
from pygame_widgets.constants import THECOLORS, KEYDOWN
from pygame_widgets.auxiliary import cursors
from pygame.time import set_timer
from pygame import event


class Gamefield(pygame_widgets.Holder):
    def __init__(self, master):
        super().__init__(master)
        self.game_state = Game_state()
        self.game_state.first_init()
        self.map_widgets = None
        self.pampuch = None
        self.monsters = list()
        self.label_info = pygame_widgets.Label(self, visible=False, font="trebuchet_ms", font_size=60, alignment_x=1,
                                               alignment_y=1, font_color=THECOLORS['white'], bold=True, italic=True,
                                               cursor=cursors.invisible)
        # self.add_handler(constants.E_GAME_STARTED, self._game_started, self_arg=False, event_arg=False)
        self.add_handler(KEYDOWN, self._game_started, self_arg=False, event_arg=False)
        self.add_handler(constants.E_DEATH, self.restart, self_arg=False, event_arg=False)
        self.add_handler(constants.E_STATE_CHANGED, self.info, self_arg=False, event_arg=True)

    def _game_started(self):
        # set_timer(constants.E_GAME_STARTED, 0)
        # self.restart() if self.restarting else self.pause(False)
        if self.game_state.state == 'stopped':
            self.game_state.state = 'playing'

    def start_game(self, level=None):
        if level:
            self.game_state.level = level
        self.load_map(self.game_state.level)

    def info(self, e):
        if e.key != 'state' or e.new_value not in ['win', 'gameover']:
            return
        # self.game_finished = True
        # event.post(event.Event(constants.E_GAME_FINISHED, score=self.score, win=not death))
        x, y = self.master_rect.size
        self.label_info.move_resize((0, (y - (x // constants.LABEL_RATIO)) // 2), 0, (x, x // constants.LABEL_RATIO),
                                    False)
        self.label_info.set(background=files.Textures.label_win_bg if e.new_value == 'win' else files.Textures.label_lose_bg,
                            text="You have won!" if e.new_value == 'win' else "Game over", visible=True)

    def load_map(self, index):
        self.pampuch = None
        self.monsters = list()
        self.game_state.goal = 0
        self.game_state.points_level = 0
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
                self.game_state.goal += 1
            if field == constants.CHAR_PAMPUCH:
                if self.pampuch is not None:
                    raise FileFormatError('Pampuch must be instanced exactly once per level', level_index=index)
                self.pampuch = pos
            elif field == constants.CHAR_MONSTER:
                self.monsters.append(pos)
        if self.pampuch is None:
            raise FileFormatError('Pampuch must be instanced exactly once per level', level_index=index)
        self.pampuch = entities.Pampuch(self, self.pampuch)
        self.pampuch.attr.img_dead = files.Textures.dead.copy()
        for index, pos in enumerate(self.monsters):
            self.monsters[index] = entities.Monster(self, pos, self.pampuch)
        for m in self.monsters:
            others = self.monsters.copy()
            others.remove(m)
            m.colleagues = others
        self.children = self.children[1:] + self.children[:1]
        # self.pause(True)
        # set_timer(constants.E_GAME_STARTED, constants.INSPECTION)

    def death(self):
        # self.pause(True)
        # event.post(event.Event(constants.E_DEATH))
        set_timer(constants.E_DEATH, constants.INSPECTION)
        self.game_state.state = 'death'
        self.game_state.lives -= 1
        for i in range(self.pampuch.attr.img_dead.length()):
            self.pampuch.set(image=self.pampuch.attr.img_dead.frames[i][0])
            self.master.update_display()
            time.sleep(3 / constants.FPS)
        # self.restarting = True

    def restart(self):
        # self.restarting = False
        set_timer(constants.E_DEATH, 0)
        if self.game_state.lives >= 0:
            self.game_state.state = 'stopped'
            self.pampuch.reset_image()
            self.pampuch.move_resize(self.pampuch.starting_position, 0)
            self.pampuch.direction = None
            self.pampuch.new_direction = list()
            for m in self.monsters:
                m.move_resize(m.starting_position, 0)
                m.direction = None
            # set_timer(constants.E_GAME_STARTED, constants.INSPECTION)
            return
        self.game_state.state = 'gameover'
        # self.info()

    def level_completed(self):
        # self.pause(True)
        self.game_state.level += 1
        if self.game_state.level == self.game_state.levels:
            self.game_state.state = 'win'
            # self.info(False)
            return
        self.game_state.state = 'stopped'
        for child in self.children[:-1]:
            child.delete()
        del self.children[:-1]
        self.map_widgets = None
        self.pampuch = None
        self.monsters = list()
        self.load_map(self.game_state.level)
