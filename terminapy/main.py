import screen
import time

class ScreenManager:
    def __init__(self):
        self.current_screen = -1
        self.screens = []

    def add_basic_screen(self):
        basic_screen = screen.Screen()
        self.screens.append(basic_screen)
        self.current_screen = len(self.screens)-1

    def add_screen(self,screen_instance: screen.Screen):
        self.screens.append(screen_instance)

    def get_screen(self,indice : int):
        if 0 <= indice < len(self.screens):
            return self.screens[indice]
        else:
            raise IndexError

    def full_autonome(self,refresh_rate : float = 0.3):
        import autonomie as at
        at.start_worker(self.__full_workflow,refresh_rate)

    def __draw_screen_on_terminal(self):
        if self.current_screen != -1:
            self.screens[self.current_screen].draw_screen_on_terminal()
            
    def __full_workflow(self,refresh_rate : float):
        actif = True
        while actif:
            try :
                self.__draw_screen_on_terminal()
                time.sleep(refresh_rate)
            except KeyboardInterrupt:
                actif = False
