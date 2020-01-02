import subprocess
import threading
from os.path import exists

from MyLib.multidimensional_array import Multidimensional_array as Md_array
from pygame import image
from pygame_widgets.auxiliary.GIFimage import GIFImage
from pygame_widgets.constants import THECOLORS

from constants import PATH


def load_map(index, mode):
    if mode is None:
        return
    with open(f"{PATH}/levels/{mode}/{index}.txt", "r") as map_file:
        size = [int(l) for l in map_file.readline()[:-1].split(' ')]
        map_array = Md_array(size, [line[:-1] for line in map_file], ' ')
    return map_array


def number_of_levels(mode):
    if mode is None:
        return 0
    index = 0
    while True:
        if exists(f"{PATH}/levels/{mode}/{index}.txt"):
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
            cls.wall = image.load(f"{PATH}/Textures/Wall{(index // 3) % 3}.gif")
        cls.point = image.load(f"{PATH}/Textures/Point.gif")
        cls.empty = THECOLORS['black']
        cls.pampuch = GIFImage(f"{PATH}/Textures/Pampuch.gif", False)
        cls.dead = GIFImage(f"{PATH}/Textures/Death_0.gif", False)
        cls.monster = GIFImage(f"{PATH}/Textures/Monster.gif", False)


if __name__ == "__main__":
    map_ = load_map(0, 'Original')
    print(*[map_[None, i] for i in range(map_.get_dimensions()[1])], sep='\n')
