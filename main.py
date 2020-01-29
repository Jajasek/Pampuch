import pygame_widgets
import constants
from pygame_widgets.constants import *
from gamefield import Gamefield
from files import Textures, get_best, set_best, EditFile
from live_counter import Live_counter
import pygame
from game_state import Game_state
from pause_menu import Pause_menu
from pygame_widgets.auxiliary import cursors


def game_state_update(self, key, old_value, new_value):
    if old_value == new_value:
        return
    # if key == 'state' and new_value != 'playing' and self.pause:
    #     self.pause = False
    # if key == 'pause' and new_value and self.state != 'playing':
    #     self.__setattr__('pause', False, False)
    #     return
    if key in ['lives', 'pause', 'points', 'state', 'mode']:
        pygame.event.post(pygame.event.Event(constants.E_STATE_CHANGED, key=key, old_value=old_value,
                                             new_value=new_value))
    if key == 'mode':
        """self.level = constants.STARTING_LEVEL[new_value]
        self.levels = number_of_levels(new_value)
        self.lives = constants.LIVES[new_value]
        self.points = 0"""
        self.reset_state()


def restart(mode):
    global gamefield
    if gamefield is not None:
        gamefield.delete()
    pygame.event.get()
    counter.abandon_game()
    label_info.set(visible=False)
    game_state.state = 'stopped'
    game_state.mode = None
    game_state.mode = mode
    for button in main_menu_buttons:
        button.disconnect()
    gamefield = Gamefield(window)
    gamefield.start_game()


def pause(e):
    if e.key == K_ESCAPE and game_state.mode is not None:
        if pause_menu.connected:
            pause_menu.button_resume_click()
        else:
            pause_menu.activate()


def button_mode_click(self):
    pygame.mouse.set_pos((window.surface.get_size()[0], 0))
    restart(self.text)


def button_options_click():
    constedit = EditFile(f"{constants.PATH}/constants.py")
    constedit.start()
    window.quit()


def pause_button_menu_click(self):
    self.game_state.pause = False
    self.game_state.mode = None
    global gamefield
    if gamefield is not None:
        gamefield.delete()
    counter.abandon_game()
    label_info.set(visible=False)
    for button in main_menu_buttons:
        button.reconnect()
    pygame_widgets.delayed_call(self.button_menu.set, appearance='normal')
    self.disconnect()


def pause_button_restart_click(self):
    pygame.mouse.set_pos((window.surface.get_size()[0], 0))
    self.game_state.pause = False
    label_info.set(visible=False)
    restart(self.game_state.mode)
    pygame_widgets.delayed_call(self.button_restart.set, appearance='normal')
    self.disconnect()


def info(self, event_):
    if event_.key != 'state' or event_.new_value not in ['win', 'gameover']:
        return
    x, y = self.surface.get_size()
    window.children.remove(label_info)
    if pause_menu.connected:
        window.children.insert(-1, label_info)
    else:
        window.children.append(label_info)
    label_info.move_resize((0, (y - (x // constants.LABEL_RATIO)) // 2), 1, (x, x // constants.LABEL_RATIO), False)
    label_info.set(
        background=Textures.label_win_bg if event_.new_value == 'win' else Textures.label_lose_bg,
        text="You have won!" if event_.new_value == 'win' else "Game over", visible=True)


Textures.load()
best_score = get_best()
game_state = Game_state()
Game_state.update = game_state_update
window = pygame_widgets.Window(flags=FULLSCREEN, bg_color=Textures.window, fps=constants.FPS)
window.add_handler(KEYDOWN, lambda e: restart(game_state.mode) if e.key == K_RETURN and
                   game_state.state in ['win', 'gameover'] else None, self_arg=False, delay=1)
window.add_handler(KEYDOWN, pause, self_arg=False)
window.add_handler(QUIT, lambda: set_best(best_score), self_arg=False, event_arg=False)
# window.add_handler(constants.E_STATE_CHANGED,
#                    lambda e: restart(None) if e.key == 'mode' and e.new_value is None else None, self_arg=False)
window.handlers[QUIT].reverse()
window.add_handler(constants.E_GAME_FINISHED, lambda: set_best(best_score), self_arg=False, event_arg=False)
window.add_handler(constants.E_STATE_CHANGED, info, self_arg=True, event_arg=True)
# button_exit = pygame_widgets.Button(window, (0, 18), (100, 17), text="Exit")
# button_exit.add_handler(E_BUTTON_BUMPED, button_wrapper(window.quit))

BUTTON_KWARGS = Args(font_name='TrebuchetMS', font_size=50, bold=True, font_color=THECOLORS['white'],
                     bg_normal=THECOLORS['transparent'],
                     bg_mouseover=button_bg(THECOLORS['transparent'], THECOLORS['red'], 10),
                     bg_pressed=button_bg(THECOLORS['transparent'], THECOLORS['red4'], 10),
                     cursor_mouseover=pygame_widgets.auxiliary.cursors.hand,
                     cursor_pressed=pygame_widgets.auxiliary.cursors.hand)[1]
main_menu_buttons = [pygame_widgets.Button(window, (710, 350), (500, 100), text="Original", **BUTTON_KWARGS),
                     pygame_widgets.Button(window, (710, 450), (500, 100), text="Test", **BUTTON_KWARGS),
                     pygame_widgets.Button(window, (710, 600), (500, 100), text="Options", **BUTTON_KWARGS),
                     pygame_widgets.Button(window, (710, 700), (500, 100), text="Exit", **BUTTON_KWARGS),
                     ]
for button in main_menu_buttons[:-2]:
    button.add_handler(E_BUTTON_BUMPED, button_wrapper(button_mode_click, self_arg=True))
main_menu_buttons[-2].add_handler(E_BUTTON_BUMPED, button_wrapper(button_options_click))
main_menu_buttons[-1].add_handler(E_BUTTON_BUMPED, button_wrapper(window.quit))

counter = Live_counter(window, (0, 36))
label_info = pygame_widgets.Label(window, visible=False, font="trebuchet_ms", font_size=60, alignment_x=1,
                                  alignment_y=1, font_color=THECOLORS['white'], bold=True, italic=True)
label_score = pygame_widgets.Label(window, (0, 72), auto_res=True, font_color=THECOLORS['yellow'], bold=True,
                                   text="Score: 0")
label_best = pygame_widgets.Label(window, (0, 90), auto_res=True, font_color=THECOLORS['yellow'], bold=True,
                                  text=f"Best: {best_score}")
pause_menu = Pause_menu(window, BUTTON_KWARGS)
pause_menu.button_menu_click = pause_button_menu_click
pause_menu.button_restart_click = pause_button_restart_click
gamefield = None

while True:
    # window.handle_events(*event.get())
    for event in pygame.event.get():
        if event.type == ACTIVEEVENT and event.state in (2, 7) and game_state.mode is not None and game_state.state == 'playing':
            pause_menu.activate()
        else:
            if event.type == KEYDOWN:
                print(event)
            window.handle_event(event)
    label_score.set(text=f"Score: {game_state.points}")
    if game_state.points > best_score:
        best_score = game_state.points
        label_best.set(text=f"Best: {best_score}")
    window.update_display()
    pygame_widgets.new_loop()
