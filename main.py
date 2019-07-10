import pygame_widgets
from pygame_widgets.constants import *
from gamefield import Gamefield
from files import Textures

Window = pygame_widgets.Window(flags=FULLSCREEN, bg_color=Textures.window)
Gamefield = Gamefield(Window)
Gamefield.load_map(0)

while True:
    Window.handle_events(*pygame_widgets.pygame.event.get())
    Window.update_display()
