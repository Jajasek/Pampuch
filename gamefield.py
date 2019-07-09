import pygame_widgets

class Gamefield(pygame_widgets.Holder):
    def __init__(self, master, filename):
        super().__init__(master)

    def load_map(self, index):
