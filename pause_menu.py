# Pampuch - a better version of Pacman
# Copyright (C) 2019  Jáchym Mierva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Jáchym Mierva
# jachym.mierva@gmail.com


import pygame_widgets
from pygame import mouse
from pygame_widgets.constants import *

from constants import PATH
from files import EditFile
from game_state import Game_state


class Pause_menu(pygame_widgets.Holder):
    def __init__(self, master, button_kwargs):
        super().__init__(master, (0, 0), master.surface.get_size(), color=(0, 0, 0, 128))
        self.game_state = Game_state()
        self.button_resume = pygame_widgets.Button(self, (710, 320), (500, 100), text="Resume", **button_kwargs)
        self.button_resume.add_handler(E_BUTTON_BUMPED, button_wrapper(self.button_resume_click))
        self.button_resume.set(shortcut_key=K_SPACE)
        self.button_menu = pygame_widgets.Button(self, (710, 420), (500, 100), text="Main menu", **button_kwargs)
        self.button_menu.set(shortcut_key=K_m)
        self.button_restart = pygame_widgets.Button(self, (710, 520), (500, 100), text="Restart", **button_kwargs)
        self.button_restart.set(shortcut_key=K_RETURN)
        self.button_options = pygame_widgets.Button(self, (710, 670), (500, 100), text="Options", **button_kwargs)
        self.button_options.add_handler(E_BUTTON_BUMPED, button_wrapper(self.button_options_click))
        self.button_exit = pygame_widgets.Button(self, (710, 770), (500, 100), text="Exit", **button_kwargs)
        self.button_exit.add_handler(E_BUTTON_BUMPED, button_wrapper(master.quit))
        self.button_exit.set(shortcut_key=K_F4)
        self.disconnect()

    def button_resume_click(self):
        mouse.set_pos((self.master.surface.get_size()[0], 0))
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
