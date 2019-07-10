from constants import PATH
from multidimensional_array import Multidimensional_array as Md_array
from pygame_widgets.constants import THECOLORS


def load_map(index):
    with open(f"{PATH}/levels/{index}.txt", "r") as map_file:
        size = [int(l) for l in map_file.readline()[:-1].split(' ')]
        map_array = Md_array(size, [line[:-1] for line in map_file], ' ')
    return map_array


class Textures:
    wall = None
    point = None
    empty = None
    pampuch = None
    monster = None
    window = THECOLORS['black']

    def __init__(self):
        raise TypeError('class Textures cannot be instanced')

    @classmethod
    def load(cls, index):
        cls.wall = THECOLORS['gray50']
        cls.point = THECOLORS['salmon']
        cls.empty = THECOLORS['transparent']
        cls.pampuch = THECOLORS['yellow']
        cls.monster = THECOLORS['blue3']
        cls.window = THECOLORS['black']


if __name__ == "__main__":
    map = load_map(0)
    print(*[map[None, i] for i in range(map.get_dimensions()[1])], sep='\n')
