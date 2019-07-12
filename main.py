import pygame_widgets
import constants
from pygame_widgets.constants import *
from gamefield import Gamefield
from files import Textures, get_best, set_best
from live_counter import Live_counter


def restart():
    global gamefield
    counter.reset()
    gamefield = Gamefield(window)
    gamefield.start_game(0)


Textures.load()
best_score = get_best()
window = pygame_widgets.Window(flags=FULLSCREEN, bg_color=Textures.window, fps=constants.FPS)
window.add_handler(KEYDOWN, lambda e: restart() if e.key == K_RETURN and gamefield.game_finished else None,
                   self_arg=False)
window.add_handler(QUIT, lambda: set_best(best_score), self_arg=False, event_arg=False)
window.handlers[QUIT].reverse()
window.add_handler(constants.E_GAME_FINISHED, lambda: set_best(best_score), self_arg=False, event_arg=False)
label_fps = pygame_widgets.Label(window, auto_res=True, font_color=THECOLORS['yellow'], bold=True)
button_exit = pygame_widgets.Button(window, (0, 18), (100, 17), text="Exit")
button_exit.add_handler(E_BUTTON_BUMPED, button_wrapper(window.quit))
counter = Live_counter(window, (0, 36))
label_score = pygame_widgets.Label(window, (0, 72), auto_res=True, font_color=THECOLORS['yellow'], bold=True,
                                   text="Score: 0")
label_best = pygame_widgets.Label(window, (0, 90), auto_res=True, font_color=THECOLORS['yellow'], bold=True,
                                  text=f"Best: {best_score}")
gamefield = None
restart()

while True:
    window.handle_events(*pygame_widgets.pygame.event.get())
    label_fps.set(text=f"fps: {window.get_fps()} {label_fps.my_surf.get_size()}")
    label_score.set(text=f"Score: {gamefield.score}")
    if gamefield.score > best_score:
        best_score = gamefield.score
        label_best.set(text=f"Best: {best_score}")
    window.update_display()
    pygame_widgets.new_loop()
