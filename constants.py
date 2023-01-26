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


from pygame_widgets.constants import USEREVENT
import pathlib
PATH = pathlib.Path(__file__).parent.absolute()
SQUARE_SIZE = 32
STEP = 8
CHAR_WALL = '#'
CHAR_POINT = '.'
CHAR_EMPTY = ' '
CHAR_MONSTER = 'X'
CHAR_PAMPUCH = 'P'
FPS = 16
# E_GAME_STARTED = USEREVENT
E_DEATH = USEREVENT + 1
E_GAME_FINISHED = USEREVENT + 2
E_STATE_CHANGED = USEREVENT + 3
INSPECTION = 2000
LABEL_RATIO = 18
QUEUE_SIZE = 4
LIVES = {'Original': 4, 'Custom': 3, None: 0}
STARTING_LEVEL = {'Original': 0, 'Custom': 0, None: None}
