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


import subprocess
import threading
from os.path import exists

from multidimensional_array import Multidimensional_array as Md_array
from pygame import image
from GIFimage import GIFImage
from pygame_widgets.constants import THECOLORS

from constants import PATH


def load_map(index, mode):
    if mode is None:
        return
    with open(f"{PATH}/Levels/{mode}/{index}.lvl", "r") as map_file:
        meta = [int(l) for l in map_file.readline()[:-1].split(' ')]
        map_array = Md_array(meta[:2], [line[:-1] for line in map_file], ' ')
    return map_array, meta[2]


def number_of_levels(mode):
    if mode is None:
        return 0
    index = 0
    while True:
        if exists(f"{PATH}/Levels/{mode}/{index}.lvl"):
            index += 1
        else:
            return index


def get_best():
    try:
        with open(f"{PATH}/best.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0


def set_best(value):
    with open(f"{PATH}/best.txt", "w") as file:
        print(value, end='', file=file)


class EditFile(threading.Thread):
    def __init__(self, file):
        super().__init__()
        self.file = file
        self.setDaemon(True)

    def run(self):
        subprocess.run(['notepad.exe', self.file])


class Textures:
    wall = None
    point = None
    empty = None
    pampuch = None
    dead = None
    monster = None
    window = THECOLORS['black']
    label_win_bg = THECOLORS['green3']
    label_lose_bg = THECOLORS['red2']

    def __init__(self):
        raise TypeError('class Textures cannot be instanced')

    @classmethod
    def load(cls, index=None):
        if index is not None:
            cls.wall = image.load(f"{PATH}/Textures/Wall{index}.gif")
        cls.point = image.load(f"{PATH}/Textures/Point.gif")
        cls.empty = THECOLORS['black']
        cls.pampuch = GIFImage(f"{PATH}/Textures/Pampuch.gif", False)
        cls.dead = GIFImage(f"{PATH}/Textures/Death_0.gif", False)
        cls.monster = GIFImage(f"{PATH}/Textures/Monster.gif", False)
