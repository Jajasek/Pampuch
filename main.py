import pygame_widgets
import constants
from pygame_widgets.constants import *
from gamefield import Gamefield
from files import Textures, get_best, set_best, number_of_levels
from live_counter import Live_counter
from pygame import event
from shared_data import Game_state


def game_state_update(self, key, old_value, new_value):
    if old_value == new_value:
        return
    if key == 'state' and new_value != 'playing' and self.pause:
        self.pause = False
    if key == 'pause' and new_value and self.state != 'playing':
        self.__setattr__('pause', False, False)
        return
    if key in ['lives', 'pause', 'points', 'state']:
        event.post(event.Event(constants.E_STATE_CHANGED, key=key, old_value=old_value, new_value=new_value))
    if key == 'mode':
        self.level = constants.STARTING_LEVEL[new_value]
        self.levels = number_of_levels(new_value)


def restart(mode):
    global gamefield
    if gamefield is not None:
        gamefield.delete()
    event.get()
    counter.reset()
    gamefield = Gamefield(window)
    gamefield.start_game(mode)


def pause(e):
    if e.key == K_ESCAPE and game_state.state == 'playing':
        game_state.pause = not game_state.pause


Textures.load()
best_score = get_best()
game_state = Game_state()
Game_state.update = game_state_update
window = pygame_widgets.Window(flags=FULLSCREEN, bg_color=Textures.window, fps=constants.FPS)
window.add_handler(KEYDOWN, lambda e: restart(game_state.mode) if e.key == K_RETURN and
                   game_state.state in ['win', 'gameover'] else None, self_arg=False, delay=1)
window.add_handler(KEYDOWN, pause, self_arg=False)
window.add_handler(QUIT, lambda: set_best(best_score), self_arg=False, event_arg=False)
window.handlers[QUIT].reverse()
window.add_handler(constants.E_GAME_FINISHED, lambda: set_best(best_score), self_arg=False, event_arg=False)
button_exit = pygame_widgets.Button(window, (0, 18), (100, 17), text="Exit")
button_exit.add_handler(E_BUTTON_BUMPED, button_wrapper(window.quit))
counter = Live_counter(window, (0, 36))
label_score = pygame_widgets.Label(window, (0, 72), auto_res=True, font_color=THECOLORS['yellow'], bold=True,
                                   text="Score: 0")
label_best = pygame_widgets.Label(window, (0, 90), auto_res=True, font_color=THECOLORS['yellow'], bold=True,
                                  text=f"Best: {best_score}")
gamefield = None
# restart('Original')

while True:
    window.handle_events(*event.get())
    label_score.set(text=f"Score: {game_state.points}")
    if game_state.points > best_score:
        best_score = game_state.points
        label_best.set(text=f"Best: {best_score}")
    window.update_display()
    pygame_widgets.new_loop()
