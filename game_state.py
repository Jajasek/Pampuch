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


import constants
import files
from shared_data import Shared_data


class Game_state(Shared_data):
    # noinspection PyAttributeOutsideInit
    def first_init(self, *args, **kwargs):
        self.mode = None  # can be 'Original', 'Test' or None
        self.lives = constants.LIVES[self.mode]
        self.level = constants.STARTING_LEVEL[self.mode]
        self.state = 'stopped'  # can be 'stopped', 'playing', 'win', 'death' or 'gameover'
        self.levels = files.number_of_levels(self.mode)
        self.pause = False
        self.points = 0
        self.points_level = 0
        self.goal = 0

    # noinspection PyAttributeOutsideInit
    def reset_state(self):
        self.lives = constants.LIVES[self.mode]
        self.level = constants.STARTING_LEVEL[self.mode]
        self.state = 'stopped'  # can be 'stopped', 'playing', 'win', 'death' or 'gameover'
        self.levels = files.number_of_levels(self.mode)
        self.points = 0
        self.points_level = 0
        self.goal = 0
