import pygame_widgets
import constants
import files
from exceptions import FileFormatError


class Entity(pygame_widgets.Image):
    play = False

    @classmethod
    def start(cls):
        cls.play = True

    @classmethod
    def stop(cls):
        cls.play = False

    def __init__(self, master, pos, image):
        self.starting_position = [pos[i] * constants.SQUARE_SIZE for i in range(2)]
        super().__init__(master, self.starting_position, [constants.SQUARE_SIZE for _ in range(2)], image=image)
        self.direction = None  # from 0 to 3, 0 = right, cc
        self._move_mappings = {0: (constants.STEP, 0),
                               1: (0, constants.STEP),
                               2: (-constants.STEP, 0),
                               3: (0, -constants.STEP)}
        self.add_handler(pygame_widgets.constants.E_LOOP_STARTED, self.step, self_arg=False, event_arg=False)

    def step(self):
        if self.direction is not None:
            self.move_resize(self._move_mappings[self.direction])
            for square in self.surroundings():
                if square.attr.type == 'wall' and self.master_rect.colliderect(square.master_rect):
                    self.move_resize(self._move_mappings[(self.direction + 2) % 4])
                    self.direction = None
                    return False
            return True

    def surroundings(self):
        coordinates = [None, None]
        topleft = list(self.master_rect.topleft)
        for i in range(2):
            if topleft[i] % constants.SQUARE_SIZE == 0:
                topleft[i] = topleft[i] // constants.SQUARE_SIZE
                coordinates[i] = slice(topleft[i] - 1, topleft[i] + 2)
            else:
                topleft[i] = topleft[i] // constants.SQUARE_SIZE
                coordinates[i] = slice(topleft[i], topleft[i] + 2)
        return self.master.map_widgets[coordinates]


class Pampuch(Entity):
    _instanced = False

    def __init__(self, master, pos):
        if Pampuch._instanced or pos is None:
            raise FileFormatError('Pampuch must be instanced exactly once per level')
        Pampuch._instanced = True
        Entity.__init__(self, master, pos, files.Textures.pampuch)
        self.new_direction = None
        self.points = 0
        self.add_handler(pygame_widgets.constants.KEYDOWN, self.change_direction, self_arg=False)
        self.add_handler(pygame_widgets.constants.E_LOOP_STARTED, self.apply_changes, self_arg=False, event_arg=False)
        self.add_handler(pygame_widgets.constants.E_LOOP_STARTED, self.point, self_arg=False, event_arg=False)
        self.handlers[pygame_widgets.constants.E_LOOP_STARTED].reverse()

    def change_direction(self, event):
        if event.key == pygame_widgets.constants.K_d:
            self.new_direction = 0
        elif event.key == pygame_widgets.constants.K_s:
            self.new_direction = 1
        elif event.key == pygame_widgets.constants.K_a:
            self.new_direction = 2
        elif event.key == pygame_widgets.constants.K_w:
            self.new_direction = 3
        elif event.key == pygame_widgets.constants.K_SPACE:
            self.new_direction = None

    def apply_changes(self):
        topleft = self.master_rect.topleft[:]
        for i in range(2):
            if topleft[i] % constants.SQUARE_SIZE:
                return
        current = self.direction
        self.direction = self.new_direction
        out = self.step()
        if out:
            self.move_resize(self._move_mappings[(self.direction + 2) % 4])
        elif out is False:
            self.direction = current

    def point(self):
        for square in self.surroundings():
            if square.attr.type == 'point' and abs(self.master_rect.topleft[0] -
                                                   square.master_rect.topleft[0]) <= constants.STEP \
                    and abs(self.master_rect.topleft[1] - square.master_rect.topleft[1]) <= constants.STEP:
                self.points += 1
                square.attr.type = 'empty'
                square.set(image=square.attr.img_empty)


class Monster(Entity):
    def __init__(self, master, pos):
        Entity.__init__(self, master, pos, files.Textures.monster)
