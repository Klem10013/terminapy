import screen
import time
import os

class ScreenManager:
    def __init__(self):
        self.current_screen = -1
        self.size = os.get_terminal_size()
        self.show_which_screen : bool = False
        self.screens = []

    def add_basic_screen(self):
        basic_screen = screen.Screen()
        self.screens.append(basic_screen)
        self.current_screen = len(self.screens)-1

    def add_screen(self,screen_instance: screen.Screen):
        self.screens.append(screen_instance)

    def show_which_screen(self):
        self.show_which_screen = True

    
    def hide_which_screen(self):
        self.show_which_screen = False

    def change_screen(self,indice : int):
        if 0 <= indice < len(self.screens):
            self.current_screen = indice
        else:
            raise IndexError

    def get_screen(self,indice : int):
        if 0 <= indice < len(self.screens):
            return self.screens[indice]
        else:
            raise IndexError

    def draw_screen_on_terminal(self):
        if self.current_screen != -1:
            screen = self.screens[self.current_screen]
            if screen.need_refresh(self.size):
                screen.refresh(self.size)
                screen_draw = screen.get_terminal_screen()
                os.sys.stdout.write(screen_draw)
                os.sys.stdout.flush()
        else:
            print("No screen to show",end='\r')

    def full_autonome(self,refresh_rate : float = 0.3):
        import autonomie as at
        at.start_worker(self.__full_workflow,refresh_rate)

    def __full_workflow(self,refresh_rate : float):
        actif = True
        while actif:
            try :
                self.size = os.get_terminal_size()
                self.draw_screen_on_terminal()
                time.sleep(refresh_rate)
            except KeyboardInterrupt:
                actif = False
