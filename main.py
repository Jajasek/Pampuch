import pygame_widgets
import constants
from pygame_widgets.constants import *
from gamefield import Gamefield
from files import Textures, get_best, set_best, number_of_levels
from live_counter import Live_counter
from pygame import event
from shared_data import Game_state
from pygame_widgets.auxiliary import cursors


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
        self.lives = constants.LIVES[new_value]


def restart(mode):
    global gamefield
    if gamefield is not None:
        gamefield.delete()
    event.get()
    counter.abandon_game()
    gamefield = Gamefield(window)
    gamefield.start_game(mode)


def pause(e):
    if e.key == K_ESCAPE and game_state.state == 'playing':
        game_state.pause = not game_state.pause


def button_mode_click(self):
    restart(self.text)


def info(self, event_):
    if event_.key != 'state' or event_.new_value not in ['win', 'gameover']:
        return
    x, y = self.surface.get_size()
    window.children.remove(label_info)
    window.children.append(label_info)
    label_info.move_resize((0, (y - (x // constants.LABEL_RATIO)) // 2), 0, (x, x // constants.LABEL_RATIO), False)
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
window.handlers[QUIT].reverse()
window.add_handler(constants.E_GAME_FINISHED, lambda: set_best(best_score), self_arg=False, event_arg=False)
window.add_handler(constants.E_STATE_CHANGED, info, self_arg=True, event_arg=True)
button_exit = pygame_widgets.Button(window, (0, 18), (100, 17), text="Exit")
button_exit.add_handler(E_BUTTON_BUMPED, button_wrapper(window.quit))
# button_mode = pygame_widgets.Button(window, (0, 0), (100, 17), text='Switch mode')
# button_mode.add_handler(E_BUTTON_BUMPED, button_wrapper(switch_mode))

kwargs = Args(font_name='TrebuchetMS', font_size=50, bold=True, font_color=THECOLORS['white'],
              bg_normal=THECOLORS['transparent'], bg_mouseover=button_bg(THECOLORS['black'], THECOLORS['red'], 10),
              bg_pressed=button_bg(THECOLORS['black'], THECOLORS['red4'], 10),
              cursor_mouseover=pygame_widgets.auxiliary.cursors.hand,
              cursor_pressed=pygame_widgets.auxiliary.cursors.hand)[1]
main_menu_buttons = [pygame_widgets.Button(window, (710, 400), (500, 100), text="Original", **kwargs),
                     pygame_widgets.Button(window, (710, 500), (500, 100), text="Test", **kwargs),
                     ]
for button in main_menu_buttons:
    button.add_handler(E_BUTTON_BUMPED, button_wrapper(button_mode_click, self_arg=True))

counter = Live_counter(window, (0, 36))
label_info = pygame_widgets.Label(window, visible=False, font="trebuchet_ms", font_size=60, alignment_x=1,
                                  alignment_y=1, font_color=THECOLORS['white'], bold=True, italic=True,
                                  cursor=cursors.invisible)
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
