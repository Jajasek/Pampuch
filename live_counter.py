import pygame_widgets
import constants
import files
_square = constants.SQUARE_SIZE + 4


class Live_counter(pygame_widgets.Holder):
    def __init__(self, master, topleft=(0, 0)):
        self.lives = constants.LIVES
        super().__init__(master, topleft, (_square * self.lives, _square))
        self.points = [None] * self.lives
        self.gif = files.Textures.pampuch.copy()
        self.skip = True
        for i in range(self.lives):
            self.points[i] = pygame_widgets.Image(self, ((i * _square) + 2, 2),
                                                  (constants.SQUARE_SIZE, constants.SQUARE_SIZE),
                                                  image=self.gif.frames[self.gif.cur][0])
        self.add_handler(constants.E_DEATH, self.decrease, self_arg=False, event_arg=False)
        self.add_handler(pygame_widgets.constants.E_LOOP_STARTED, self.next_frame, self_arg=False, event_arg=False)

    def next_frame(self):
        self.skip = not self.skip
        if self.skip:
            return
        self.gif.cur = (self.gif.cur + 1) % self.gif.length()
        frame = self.gif.cur
        for p in self.points:
            if p.visible:
                p.set(image=self.gif.frames[frame][0])
                frame = (frame + 1) % self.gif.length()

    def decrease(self):
        self.points[self.lives - 1].set(visible=False)
        self.lives -= 1

    def reset(self):
        for p in self.points:
            p.set(visible=True)
