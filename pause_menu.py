import pygame_widgets
from pygame import mouse
from shared_data import Game_state
from pygame_widgets.constants import *
from constants import PATH
from files import EditFile


class Pause_menu(pygame_widgets.Holder):
    def __init__(self, master, button_kwargs):
        super().__init__(master, (0, 0), master.surface.get_size(), color=(0, 0, 0, 128))
        self.game_state = Game_state()
        self.button_resume = pygame_widgets.Button(self, (710, 320), (500, 100), text="Resume", **button_kwargs)
        self.button_resume.add_handler(E_BUTTON_BUMPED, button_wrapper(self.button_resume_click))
        self.button_menu = pygame_widgets.Button(self, (710, 420), (500, 100), text="Main menu", **button_kwargs)
        self.button_restart = pygame_widgets.Button(self, (710, 520), (500, 100), text="Restart", **button_kwargs)
        self.button_restart.set(shortcut_key=K_RETURN)
        self.button_options = pygame_widgets.Button(self, (710, 670), (500, 100), text="Options", **button_kwargs)
        self.button_options.add_handler(E_BUTTON_BUMPED, button_wrapper(self.button_options_click))
        self.button_exit = pygame_widgets.Button(self, (710, 770), (500, 100), text="Exit", **button_kwargs)
        self.button_exit.add_handler(E_BUTTON_BUMPED, button_wrapper(master.quit))
        self.button_exit.set(shortcut_key=K_F4)
        self.disconnect()

    def button_resume_click(self):
        mouse.set_pos(self.master.surface.get_size())
        self.game_state.pause = False
        pygame_widgets.delayed_call(self.button_resume.set, appearance='normal')
        self.disconnect()

    def button_options_click(self):
        constedit = EditFile(f"{PATH}/constants.py")
        constedit.start()
        self.master.quit()

    @property
    def button_menu_click(self):
        return None

    @button_menu_click.setter
    def button_menu_click(self, value):
        self.button_menu.add_handler(E_BUTTON_BUMPED, button_wrapper(value), [self])

    @property
    def button_restart_click(self):
        return None

    @button_restart_click.setter
    def button_restart_click(self, value):
        self.button_restart.add_handler(E_BUTTON_BUMPED, button_wrapper(value), [self])

    def activate(self):
        self.game_state.pause = True
        self.reconnect()
        pass
