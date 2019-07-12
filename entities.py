import pygame_widgets
import constants
import files
from exceptions import FileFormatError
from random import choice
from pygame import transform
from pygame_widgets.auxiliary import cursors


def left(direction):
    return (direction + 1) % 4


def leftall(direction):
    return tuple([left(direction + f) for f in [-0.5, 0, 0.5]])


def right(direction):
    return (direction - 1) % 4


def rightall(direction):
    return tuple([right(direction + f) for f in [-0.5, 0, 0.5]])


class Entity(pygame_widgets.Image):
    def __init__(self, master, pos, image):
        self.starting_position = [pos[i] * constants.SQUARE_SIZE for i in range(2)]
        self.gif = image
        super().__init__(master, self.starting_position, [constants.SQUARE_SIZE for _ in range(2)],
                         image=image.frames[image.cur][0], cursor=cursors.invisible)
        self.direction = None  # from 0 to 3, 0 = right, cc
        self.ignored = None
        self.paused = False
        self._move_mappings = {0: (constants.STEP, 0),
                               1: (0, -constants.STEP),
                               2: (-constants.STEP, 0),
                               3: (0, constants.STEP)}
        self.add_handler(pygame_widgets.constants.E_LOOP_STARTED, self.step, self_arg=False, event_arg=False)

    def pause(self, value=None):
        if value is None:
            return self.paused
        self.paused = bool(value)

    def step(self, stop=True):
        if self.direction is not None and not self.paused:
            self.move_resize(self._move_mappings[self.direction])
            for square in self.surroundings():
                if square == self.ignored:
                    continue
                if square.attr.type == 'wall' and self.master_rect.colliderect(square.master_rect):
                    intersection = self.master_rect.clip(square.master_rect)
                    if intersection.size == (constants.STEP, constants.STEP):
                        self.ignored = square
                        continue
                    self.move_resize(self._move_mappings[(self.direction + 2) % 4])
                    if stop:
                        self.stop()
                    return False
            if isinstance(self, Monster):
                for monster in self.colleagues:
                    if self.master_rect.colliderect(monster.master_rect):
                        self.move_resize(self._move_mappings[(self.direction + 2) % 4])
                        if stop:
                            self.stop()
                        return False
            if self.ignored:
                self.check_ignored()
            if stop:
                self.next_image()
            return True

    def check_ignored(self):
        if not self.master_rect.colliderect(self.ignored.master_rect):
            self.ignored = None
            return
        x, y = [self.ignored.master_rect.topleft[i] - self.master_rect.topleft[i] for i in range(2)]
        if self.direction % 2:
            if abs(x) == constants.STEP * 3 and not y:
                dir_ = -(x // abs(x))
                self.move_resize((dir_ * constants.STEP, 0))
                self.ignored = None
        else:
            if abs(y) == constants.STEP * 3 and not x:
                dir_ = -(y // abs(y))
                self.move_resize((0, dir_ * constants.STEP))
                self.ignored = None

    def next_image(self):
        self.gif.cur = (self.gif.cur + 1) % self.gif.length()
        self.set(image=self.gif.frames[self.gif.cur][0])

    def try_step(self, direction):
        current = self.direction
        self.direction = direction
        output = Entity.step(self, False)
        if output:
            self.move_resize(self._move_mappings[(self.direction + 2) % 4])
            self.direction = current
            return True
        self.direction = current
        return False

    def stop(self):
        self.direction = None

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

    @property
    def position(self):
        return self.master_rect.topleft


class Pampuch(Entity):
    def __init__(self, master, pos):
        if pos is None:
            raise FileFormatError('Pampuch must be instanced exactly once per level')
        Entity.__init__(self, master, pos, files.Textures.pampuch.copy())
        self.new_direction = list()
        self.points = 0
        self.add_handler(pygame_widgets.constants.KEYDOWN, self.change_direction, self_arg=False)
        self.add_handler(pygame_widgets.constants.E_LOOP_STARTED, self.apply_changes, self_arg=False, event_arg=False)
        self.add_handler(pygame_widgets.constants.E_LOOP_STARTED, self.point, self_arg=False, event_arg=False)
        self.handlers[pygame_widgets.constants.E_LOOP_STARTED].reverse()

    def change_direction(self, event):
        if len(self.new_direction) > constants.QUEUE_SIZE:
            return
        if event.key == pygame_widgets.constants.K_d:
            self.new_direction.append(0)
        elif event.key == pygame_widgets.constants.K_w:
            self.new_direction.append(1)
        elif event.key == pygame_widgets.constants.K_a:
            self.new_direction.append(2)
        elif event.key == pygame_widgets.constants.K_s:
            self.new_direction.append(3)
        elif event.key == pygame_widgets.constants.K_LSHIFT:
            self.new_direction = [None]
        elif event.key == pygame_widgets.constants.K_SPACE:
            self.new_direction = list()

    def next_image(self):
        self.gif.cur = (self.gif.cur + 1) % self.gif.length()
        image = self.gif.frames[self.gif.cur][0]
        if self.direction in [1, 2]:
            image = transform.flip(image, True, False)
        if self.direction in [1, 3]:
            image = transform.rotate(image, -90)
        self.set(image=image)

    def reset_image(self):
        self.gif.reset()
        self.set(image=self.gif.frames[self.gif.cur][0])

    def apply_changes(self):
        while True:
            print(self.new_direction, self.direction)
            if not self.new_direction:
                return
            if self.new_direction[0] == self.direction:
                self.new_direction.pop(0)
            elif self.new_direction[0] != self.direction:
                break
        for x in self.master_rect.topleft:
            if x % constants.SQUARE_SIZE:
                return
        if self.new_direction[0] is None or self.try_step(self.new_direction[0]):
            self.direction = self.new_direction.pop(0)
        elif self.direction is None and not self.paused:
            self.new_direction.pop(0)
            self.apply_changes()

    def point(self):
        for square in self.surroundings():
            if square.attr.type == 'point' and self.master_rect.topleft == square.master_rect.topleft:
                self.points += 1
                self.master.score += 1
                square.attr.type = 'empty'
                square.set(image=square.attr.img_empty)
                if self.points == self.master.goal:
                    self.master.level_completed()


class Monster(Entity):
    def __init__(self, master, pos, target):
        Entity.__init__(self, master, pos, files.Textures.monster.copy())
        self.target = target
        self.direction_old = None
        self.cooldown = 0
        self.colleagues = None

    def check(self):
        intersection = self.master_rect.clip(self.target.master_rect).size
        for l in intersection:
            if l < 2 * constants.STEP:
                return
        self.master.death()

    def step(self, stop=True):
        if self.paused:
            return
        self.check()
        if self.cooldown:
            self.cooldown -= 1
            self.direction = self.find_direction()
            if self.direction is None:
                self.cooldown = 0
        else:
            if self.direction is None:
                self.direction = self.find_direction()
                if self.direction is not None:
                    self.cooldown = 4
                return
            output = Entity.step(self, stop)
            if output is not None:
                self.direction_old = self.direction
            return output

    def stop(self):
        self.direction = self.find_direction()
        if self.direction is None:
            self.direction_old = None
        else:
            self.cooldown = 1

    def target_relative(self):
        relative_xy = [0, 0]
        relative = -1
        for i in range(2):
            if self.position[i] - self.target.position[i] > constants.SQUARE_SIZE - constants.STEP:
                relative_xy[i] = -1
            elif self.target.position[i] - self.position[i] > constants.SQUARE_SIZE - constants.STEP:
                relative_xy[i] = 1
        x, y = relative_xy
        if x > 0:
            relative = 0
        if y < 0:
            relative = 1
        if x < 0:
            relative = 2
        if y > 0:
            relative = 3
        if (x > 0) and (y < 0):
            relative = 0.5
        if (x < 0) and (y < 0):
            relative = 1.5
        if (x < 0) and (y > 0):
            relative = 2.5
        if (x > 0) and (y > 0):
            relative = 3.5
        return relative

    def open_directions(self):
        output = [None] * 4
        for direction in range(4):
            output[direction] = self.try_step(direction)
        return output

    def find_direction(self):
        open_directions = self.open_directions()
        target_relative = self.target_relative()
        if self.direction_old is None:
            if isinstance(target_relative, int):
                if open_directions[target_relative]:
                    return target_relative
                if open_directions[left(target_relative)] and open_directions[right(target_relative)]:
                    return None
                if open_directions[left(target_relative)]:
                    return left(target_relative)
                if open_directions[right(target_relative)]:
                    return right(target_relative)
                return None
            possible = [int(target_relative + 0.5) % 4, int(target_relative - 0.5)]
            for p in possible:
                if not open_directions[p]:
                    possible.remove(p)
            if possible:
                return choice(possible)
            return None
        if open_directions[self.direction_old]:
            return self.direction_old
        if target_relative == self.direction_old:
            if open_directions[left(self.direction_old)] and not open_directions[right(self.direction_old)]:
                return left(self.direction_old)
            if not open_directions[left(self.direction_old)] and open_directions[right(self.direction_old)]:
                return right(self.direction_old)
            return None
        if target_relative == left(left(self.direction_old)):
            if open_directions[left(self.direction_old)] and open_directions[right(self.direction_old)]:
                return choice([left, right])(self.direction_old)
            if open_directions[left(left(self.direction_old))]:
                return left(left(self.direction_old))
            if open_directions[left(self.direction_old)]:
                return left(self.direction_old)
            if open_directions[right(self.direction_old)]:
                return right(self.direction_old)
            return None
        if target_relative in leftall(self.direction_old):
            if open_directions[left(self.direction_old)]:
                return left(self.direction_old)
            if target_relative == left(self.direction_old - 0.5):
                return None
            if open_directions[left(left(self.direction_old))]:
                return left(left(self.direction_old))
            return None
        if target_relative in rightall(self.direction_old):
            if open_directions[right(self.direction_old)]:
                return right(self.direction_old)
            if target_relative == right(self.direction_old + 0.5):
                return None
            if open_directions[left(left(self.direction_old))]:
                return left(left(self.direction_old))
            return None
