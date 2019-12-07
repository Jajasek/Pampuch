import pygame_widgets
import constants
import files
import time
_square = constants.SQUARE_SIZE + 4


class Live_counter(pygame_widgets.Holder):
    def __init__(self, master, topleft=(0, 0)):
        self.lives = 0
        self.points = list()
        super().__init__(master, topleft, (_square * self.lives, _square))
        self.gif = files.Textures.pampuch.copy()
        self.gif_death = files.Textures.dead.copy()
        self.skip = True
        self.add_handler(constants.E_STATE_CHANGED, self.actualise, self_arg=False, event_arg=True)
        self.add_handler(pygame_widgets.constants.E_LOOP_STARTED, self.next_frame, self_arg=False, event_arg=False)
        self.create_livepoints()

    def create_livepoints(self):
        self.move_resize(resize=(_square * self.lives, _square), resize_rel=False)
        self.points = [None] * self.lives
        for i in range(self.lives):
            self.points[i] = pygame_widgets.Image(self, ((i * _square) + 2, 2),
                                                  (constants.SQUARE_SIZE, constants.SQUARE_SIZE),
                                                  image=self.gif.frames[self.gif.cur][0])

    def next_frame(self):
        self.skip = not self.skip
        if self.skip:
            return
        self.gif.cur = (self.gif.cur + 1) % self.gif.length()
        frame = self.gif.cur
        for p in self.points[:self.lives]:
            p.set(image=self.gif.frames[frame][0])
            frame = (frame + 1) % self.gif.length()

    def actualise(self, event):
        if event.key != 'lives':
            return
        if self.lives < event.new_value:
            self.abandon_game()
            self.lives = event.new_value
            self.create_livepoints()
            return
        while self.lives > event.new_value and self.lives > 0:
            for i in range(self.gif_death.length()):
                self.points[self.lives - 1].set(image=self.gif_death.frames[i][0])
                self.master.update_display()
                time.sleep(3 / constants.FPS)
            self.lives -= 1

    def abandon_game(self):
        for livepoint in self.points:
            livepoint.delete()
        self.points = list()
        self.lives = 0
