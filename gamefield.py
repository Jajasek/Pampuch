# Pampuch - a better version of Pacman
# Copyright (C) 2019  Jáchym Mierva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Jáchym Mierva
# jachym.mierva@gmail.com


import pygame_widgets
import entities
import files
import constants
import time
from exceptions import FileFormatError
from MyLib.multidimensional_array import Multidimensional_array as Md_array
from game_state import Game_state
from pygame_widgets.constants import KEYDOWN, K_ESCAPE, K_LSUPER
from pygame.time import set_timer
from pygame import event


class Gamefield(pygame_widgets.Holder):
    def __init__(self, master):
        super().__init__(master)
        self.game_state = Game_state()
        # self.game_state.first_init()
        self.map_widgets = None
        self.pampuch = None
        self.monsters = list()
        # self.add_handler(constants.E_GAME_STARTED, self._game_started, self_arg=False, event_arg=False)
        self.add_handler(KEYDOWN, lambda e: self._game_started() if e.key not in {K_ESCAPE, K_LSUPER} and not self.game_state.pause
                         else None, self_arg=False, event_arg=True)
        self.add_handler(constants.E_DEATH, self.restart, self_arg=False, event_arg=False)

    def _game_started(self):
        # set_timer(constants.E_GAME_STARTED, 0)
        # self.restart() if self.restarting else self.pause(False)
        if self.game_state.state == 'stopped':
            self.game_state.state = 'playing'

    def start_game(self, level=None):
        if level:
            self.game_state.level = level
        self.load_map(self.game_state.level)

    def load_map(self, index):
        self.pampuch = None
        self.monsters = list()
        self.game_state.goal = 0
        self.game_state.points_level = 0
        map_strings, texture_index = files.load_map(index, self.game_state.mode)
        files.Textures.load(texture_index)
        self.move_resize([(self.master.surface.get_size()[i] - (map_strings.get_dimensions()[i] *
                                                                constants.SQUARE_SIZE)) // 2 for i in range(2)],
                         1, [map_strings.get_dimensions()[i] * constants.SQUARE_SIZE for i in range(2)], False)
        self.map_widgets = Md_array(map_strings.get_dimensions())
        for pos, field in map_strings.enumerated:
            self.map_widgets[pos] = entities.Background(self, [pos[i] * constants.SQUARE_SIZE for i in range(2)],
                                                        [constants.SQUARE_SIZE for _ in range(2)], pos=pos)
            if field == constants.CHAR_WALL:
                self.map_widgets[pos].attr.type = 'wall'
                self.map_widgets[pos].set(image=files.Textures.wall, cursor=pygame_widgets.cursors.invisible)
            elif field in {constants.CHAR_EMPTY, constants.CHAR_PAMPUCH}:
                self.map_widgets[pos].attr.type = 'empty'
                self.map_widgets[pos].set(image=files.Textures.empty)
            else:
                self.map_widgets[pos].attr.img_empty = files.Textures.empty
                self.map_widgets[pos].attr.type = 'point'
                self.map_widgets[pos].set(image=files.Textures.point, cursor=pygame_widgets.cursors.invisible)
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
            self.pampuch.move_resize(self.pampuch.starting_position, 1)
            self.pampuch.direction = None
            self.pampuch.new_direction = list()
            for m in self.monsters:
                m.move_resize(m.starting_position, 1)
                m.direction = None
                m.direction_old = None
                m.cooldown = 0
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
        for child in self.children:
            child.delete()
        del self.children[:]
        self.map_widgets = None
        self.pampuch = None
        self.monsters = list()
        self.load_map(self.game_state.level)
