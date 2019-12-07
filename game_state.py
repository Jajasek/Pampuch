import constants
import files
from MyLib.shared_data import Shared_data


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
