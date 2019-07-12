import pygame_widgets
import constants
from pygame_widgets.constants import *
from gamefield import Gamefield
from files import Textures
from live_counter import Live_counter


Textures.load()
window = pygame_widgets.Window(flags=FULLSCREEN, bg_color=Textures.window, fps=constants.FPS)
label_fps = pygame_widgets.Label(window, auto_res=True, font_color=THECOLORS['yellow'], bold=True)
button_exit = pygame_widgets.Button(window, (0, 18), (100, 17), text="Exit")
button_exit.add_handler(E_BUTTON_BUMPED, button_wrapper(window.quit))
counter = Live_counter(window, (0, 36))
gamefield = Gamefield(window)
gamefield.start_game(0)

while True:
    window.handle_events(*pygame_widgets.pygame.event.get())
    label_fps.set(text=f"fps: {window.get_fps()} {label_fps.my_surf.get_size()}")
    window.update_display()
    pygame_widgets.new_loop()
