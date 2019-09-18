import constants
import files


class Shared_data:
    instances = list()

    def __init__(self):
        if self.instances:
            for name, value in self.instances[0].__dict__.items():
                object.__setattr__(self, name, value)
            self.instances.append(self)
        else:
            self.instances.append(self)
            self.first_init()

    def first_init(self, *args, **kwargs):
        pass

    def _update(self, key, old_value, new_value):
        pass

    @property
    def update(self):
        return self._update

    @update.setter
    def update(self, value):
        self._update = value

    def delete(self):
        self.instances.remove(self)

    def __setattr__(self, key, value):
        old = getattr(self, key, None)
        for instance in self.instances:
            object.__setattr__(instance, key, value)
        self.update(key, old, value)


class Game_state(Shared_data):
    # noinspection PyAttributeOutsideInit
    def first_init(self, *args, **kwargs):
        self.lives = constants.LIVES
        self.level = constants.STARTING_LEVEL
        self.pause = False
        self.points = 0
        self.points_level = 0
        self.goal = 0
        self.levels = files.number_of_levels()
        self.state = 'stopped'  # can be 'stopped', 'playing', 'win', 'death' or 'gameover'
