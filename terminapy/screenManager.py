from .screen import Screen
from .screenType.screenTypeEnum import ScreenTypeEnum as scType
from .screenSelecteur import get_screen_type
import time
import os
import sys

class ScreenManager:
    def __init__(self, ScreenType : scType = scType.BASIC, existing_screen : Screen = None):
        self.size = os.get_terminal_size()
        self.ANSI = self.is_ansi() 
        if existing_screen is not None:
            self.screen = existing_screen
        else:
            self.screen : Screen = get_screen_type(ScreenType)

    def is_ansi(self):
        if os.environ.get("TERM") == "dumb":
            return False
        if not sys.stdout.isatty():
            return False
        if sys.platform == "win32":
            return False
        return True

    def split_vertically(self,left : scType, right : scType, ratio:float = 0.5):
        left = get_screen_type(left)
        right = get_screen_type(right)
        self.screen.split_vertically(ratio = ratio, screen_left=left,screen_right=right)
        return left,right
    
    def split_horizontally(self,top : scType, bottom : scType, ratio:float = 0.5):
        top = get_screen_type(top)
        bottom = get_screen_type(bottom)
        self.screen.split_horizontally(ratio=ratio,screen_top=top,screen_bottom=bottom)
        return top,bottom

    def draw_screen_on_terminal(self):
        self.size = os.get_terminal_size()
        if self.screen.need_refresh(self.size):
            self.screen.refresh(self.size)
            screen_draw = self.screen.get_string_screen()
            if self.is_ansi:
                sys.stdout.write("\033[H\033[?25l"+screen_draw)
            else:
                sys.stdout.write("\n"+screen_draw)
            os.sys.stdout.flush()

    def full_autonome(self,refresh_rate : float = 0.3):
        from . import autonomie as at
        at.start_worker(self.__full_workflow,refresh_rate)

    def __full_workflow(self,refresh_rate : float):
        actif = True

        while actif:
            try :
                self.draw_screen_on_terminal()
                time.sleep(refresh_rate)
            except KeyboardInterrupt:
                actif = False
