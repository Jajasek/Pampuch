from constants import PATH
from multidimensional_array import Multidimensional_array as Md_array
from pygame_widgets.constants import THECOLORS
from pygame_widgets.auxiliary.GIFimage import GIFImage
from pygame import image
from os.path import exists


def load_map(index):
    with open(f"{PATH}/levels/{index}.txt", "r") as map_file:
        size = [int(l) for l in map_file.readline()[:-1].split(' ')]
        map_array = Md_array(size, [line[:-1] for line in map_file], ' ')
    return map_array


def number_of_levels():
    index = 0
    while True:
        if exists(f"{PATH}/levels/{index}.txt"):
            index += 1
        else:
            return index


def get_best():
    try:
        with open("D:/Jáchym/Programování/Python/Pampuch/best.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0


def set_best(value):
    with open("D:/Jáchym/Programování/Python/Pampuch/best.txt", "w") as file:
        print(value, end='', file=file)


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
        cls.wall = image.load(f"{PATH}/Textures/Wall.gif")
        cls.point = image.load(f"{PATH}/Textures/Point.gif")
        cls.empty = THECOLORS['black']
        cls.pampuch = GIFImage(f"{PATH}/Textures/Pampuch.gif", False)
        cls.dead = THECOLORS['red3']
        cls.monster = GIFImage(f"{PATH}/Textures/Monster.gif", False)


if __name__ == "__main__":
    map = load_map(0)
    print(*[map[None, i] for i in range(map.get_dimensions()[1])], sep='\n')
