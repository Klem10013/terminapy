#standard lib
import os
import math

#my import 
from . import border


def round_down(x):
    fr = math.floor(x)
    if x - fr > 0.5:
        return math.ceil(x)
    return fr

"""
This Class is use as the base for all screen version it can not be use to display anything only the screen border.
"""
class Screen:
    def __init__(self, size=None, name: str = "", ratio: tuple[float, float] = (1, 1),
                 border_style: border.BorderStyle = border.SQUARE_CORNER()):
        if name != "":
            name = f"[ {name} ]"
        self.name = name
        self.ratio = ratio
        self.border = border_style
        self.screen_changed = False
        self.split_screens: tuple[Screen, Screen, str] = None
        self.size_old = None
        self.size = size
        self.join_char = ""
        if self.size is not None:
            self.change_size(size)

    def set_border_style(self, style: border.BorderStyle):
        self.screen_changed = True
        self.border = style
        if self.split_screens is not None:
            self.split_screens[0].set_border_style(style)
            self.split_screens[1].set_border_style(style)

    def split_horizontally(self, ratio: float, screen_top = None, screen_bottom = None):
        if screen_top is None:
            screen_top = self
        if screen_bottom is None:
            screen_bottom = self
        if self.split_screens is None:
            self.screen_changed = True
            screen1 = self.init_split_screen(screen_top,(ratio,1))
            screen2 = self.init_split_screen(screen_bottom,(1 - ratio,1))
            self.split_screens = screen1, screen2, "h"
            return screen1,screen2
        else:
            raise RuntimeError("Screen is already split")

    def split_vertically(self, ratio: float, screen_left = None, screen_right = None):
        if screen_left is None:
            screen_left = self
        if screen_right is None:
            screen_right = self
        if self.split_screens is None:
            self.screen_changed = True
            screen1 = self.init_split_screen(screen_left,(ratio,1))
            screen2 = self.init_split_screen(screen_right,(1 - ratio,1))
            self.split_screens = screen1, screen2, "v"
            return screen1,screen2
        else:
            raise RuntimeError("Screen is already split")

    def init_split_screen(self, screen, ratio: tuple[float, float]):
        screen.size = self.size
        screen.ratio = ratio
        screen.border = self.border
        return screen

    def change_size(self, size, cut=None, sp=""):
        if size.columns == 0 or size.lines == 0:
            return None
        rc = round_down(size.columns * self.ratio[0])
        rl = round_down(size.lines * self.ratio[1])
        if cut is not None:
            if sp == "v" and cut[0] + rc == size.columns:
                rc = round_down(size.columns * self.ratio[0] - 1)
            if sp == "h" and cut[1] + rl == size.lines:
                rl = round_down(size.lines * self.ratio[1] - 1)
        self.size = os.terminal_size((rc, rl))
        if self.split_screens != None:
            res1 = self.split_screens[0].change_size(self.size)
            self.split_screens[1].change_size(self.size, res1, self.split_screens[2])
        return (rc, rl)

    """
    return the left screen if left is True, else return the right screen. If the screen is not split, return self
    """
    def get_screen(self, left: bool = True) -> "Screen":
        if self.split_screens is None:
            raise ValueError("Screen is not split")
        if left:
            return self.split_screens[0]
        else:
            return self.split_screens[1]

    def get_string_screen(self):
        return self.create_screen()

    def create_screen(self, no_top: bool = False, no_bot: bool = False, no_left: bool = False, no_right: bool = False,
                      to_list: bool = False) -> str:
        if self.size is None:
            return "BAD SIZE"
        screen = []
        if self.split_screens is None:
            if not no_top:
                screen.append((self.border["hr"] if no_left else self.border["tl"]) + self.border["hr"] * (
                            self.size.columns - 2) + (self.border["hr"] if no_right else self.border["tr"]))
            for i in range(self.size.lines - (2 - int(no_top) - int(no_bot))):
                screen.append((" " if no_left else self.border["vr"]) + " " * (self.size.columns - 2) + (
                    " " if no_right else self.border["vr"]))
            if not no_bot:
                screen.append((self.border["hr"] if no_left else self.border["bl"]) + self.border["hr"] * (
                            self.size.columns - 2) + (self.border["hr"] if no_right else self.border["br"]))
        else:
            screen1 = self.split_screens[0]
            screen2 = self.split_screens[1]
            if self.split_screens[2] == "h":
                top_screen_str = screen1.create_screen(no_top, True, no_left, no_right, True)
                bottom_screen_str = screen2.create_screen(True, no_bot, no_left, no_right, True)
                screen += top_screen_str
                li = (self.border["hr"] if no_left else self.border["cl"])
                for i in range(1, self.size.columns - 1):
                    if top_screen_str[-1][i] == self.border["vr"] and bottom_screen_str[0][i] == self.border["vr"]:
                        li += self.border["cc"]
                    elif top_screen_str[-1][i] == self.border["vr"] and bottom_screen_str[0][i] != self.border["vr"]:
                        li += self.border["cb"]
                    elif top_screen_str[-1][i] != self.border["vr"] and bottom_screen_str[0][i] == self.border["vr"]:
                        li += self.border["ct"]
                    else:
                        li += self.border["hr"]
                li += (self.border["hr"] if no_right else self.border["cr"])
                screen.append(li)
                screen += bottom_screen_str

            if self.split_screens[2] == "v":
                left_screen_str = screen1.create_screen(no_top, no_bot, no_left, True, True)
                right_screen_str = screen2.create_screen(no_top, no_bot, True, no_right, True)
                screen.append(
                    left_screen_str[0] + (self.border["vr"] if no_top else self.border["ct"]) + right_screen_str[0])
                if len(left_screen_str) != len(right_screen_str):
                    raise ValueError("Left and Right screen have different heights")
                for i in range(1, len(left_screen_str) - 1):
                    md = self.border["vr"]
                    if left_screen_str[i][-1] == self.border["hr"] and right_screen_str[i][0] == self.border["hr"]:
                        md = self.border["cc"]
                    elif left_screen_str[i][-1] == self.border["hr"] and right_screen_str[i][0] != self.border["hr"]:
                        md = self.border["cr"]
                    elif left_screen_str[i][-1] != self.border["hr"] and right_screen_str[i][0] == self.border["hr"]:
                        md = self.border["cl"]
                    screen.append(left_screen_str[i] + md + right_screen_str[i])
                screen.append(
                    left_screen_str[-1] + (self.border["vr"] if no_bot else self.border["cb"]) + right_screen_str[-1])

        if to_list:
            return screen
        return self.join_char.join(screen)

    def need_refresh(self, size) -> bool:
        return (self.size is None or
                (size is not None and
                    (size.columns != self.size.columns or size.lines != self.size.lines)
                )or
                self.screen_changed
                or
                (self.split_screens is not None and (
                        self.split_screens[0].need_refresh(None) or self.split_screens[1].need_refresh(None))))

    def refresh(self, size):
        self.change_size(size)
        self.refresh_done()

    def refresh_done(self):
        self.screen_changed = False
        if self.split_screens is not None:
            self.split_screens[0].refresh_done()
            self.split_screens[1].refresh_done()
