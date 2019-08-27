import constants
import files


class Shared_data:
    instances = list()

    def __init__(self):
        if self.instances:
            for name, value in self.instances[0].__dict__.items():
                object.__setattr__(self, name, value)
        else:
            self.first_init()
        self.instances.append(self)

    def first_init(self, *args, **kwargs):
        pass

    def delete(self):
        self.instances.remove(self)

    def __setattr__(self, key, value):
        for instance in self.instances:
            object.__setattr__(instance, key, value)


class Game_state(Shared_data):
    def __init__(self):
        super().__init__()

    # noinspection PyAttributeOutsideInit
    def first_init(self, *args, **kwargs):
        self.lives = constants.LIVES
        self.level = constants.STARTING_LEVEL
        self.pause = False
        self.points = 0
        self.points_level = 0
        self.goal = 0
        self.levels = files.number_of_levels()
        self.state = 'stopped'
