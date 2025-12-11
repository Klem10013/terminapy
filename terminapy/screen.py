
import os
import time
import math
import border

def round_down(x):
    fr = math.floor(x)
    if x-fr > 0.5:
        return math.ceil(x)
    return fr 



class Screen:
    def __init__(self,size=None,name:str="",ratio : tuple[float,float] = (1,1), border_style : border.BorderStyle = border.SQUARE_CORNER()):
        if name != "":
            name = f"[ {name} ]"
        self.name = name
        self.ratio = ratio
        self.border = border_style
        self.launched = False
        self.lines : list[str] = []
        self.line_changed = False
        self.screen_changed = False
        self.split_screens : tuple[Screen,Screen,str] = None
        self.size_old = None
        self.size = size
        self.join_char = ""
        self.apply_change : list[(str,str)] = []
        if self.size != None:
            self.change_size(size)

    def full_autonome(self):
        self.launched = True

    def set_border_style(self,style : border.BorderStyle):
        self.screen_changed = True
        self.border = style
        if self.split_screens is not None:
            self.split_screens[0].set_border_style(style)
            self.split_screens[1].set_border_style(style)

    def split_horizontally(self,ratio : float):
        if self.split_screens is None:
            self.split_screens = Screen(self.size,"",(1,ratio),self.border),Screen(self.size,"",(1,1-ratio),self.border),"h"
        else:
            raise RuntimeError("Screen is already split")

    def split_vertically(self,ratio : float):
        if self.split_screens is None:
            self.split_screens = Screen(self.size,"",(ratio,1),self.border),Screen(self.size,"",(1-ratio,1),self.border),"v"
        else:
            raise RuntimeError("Screen is already split")

    def apply(self,regex:str,replacement:str):
        self.apply_change.append((regex,replacement))
    
    def change_size(self,size,cut=None,sp=""):
        rc = round_down(size.columns*self.ratio[0])
        rl = round_down(size.lines  *self.ratio[1])
        if cut is not None:
            if sp == "v" and cut[0]+rc == size.columns:
                rc = round_down(size.columns*self.ratio[0]-1)
            if sp == "h" and cut[1]+rl == size.lines:
                rl = round_down(size.lines  *self.ratio[1]-1)
        self.size = os.terminal_size((rc,rl))
        if self.split_screens != None:
            res1 = self.split_screens[0].change_size(self.size)
            self.split_screens[1].change_size(self.size,res1,self.split_screens[2])
        return (rc,rl)

    def change_lines(self,lines : list[str],copy: bool = True):
        self.line_changed = True
        self.lines.clear()
        if self.split_screens is not None:
            self.split_screens[0].change_lines(lines,copy)
            self.split_screens[1].change_lines(lines,copy)
        else:
            if copy:
                self.lines = lines.copy()
            else:
                self.lines = lines
    
    def append(self,message:str):
        self.line_changed = True
        if self.split_screens is not None:
            self.split_screens[0].append(message)
            self.split_screens[1].append(message)
        else:
            self.lines.append(message)
    
    def clear(self):
        self.line_changed = True
        if self.split_screens is not None:
            self.split_screens[0].clear()
            self.split_screens[1].clear()
        else:
            self.lines.clear()

    def rewrite_last_line(self,message:str):
        self.line_changed = True
        if self.split_screens is not None:
            self.split_screens[0].rewrite_last_line(message)
            self.split_screens[1].rewrite_last_line(message)
        else:
            if len(self.lines) == 0:
                self.lines.append(message)
            else:
                self.lines[-1] = message

    def get_screen(self,indice : int):
        if 0 <= indice < 2:
            return self.split_screens[indice]
        else:
            raise IndexError

    def get_terminal_screen(self):
        return self.__create_screen()

    def __create_screen(self,no_top : bool = False, no_bot : bool = False,no_left : bool = False, no_right : bool = False , to_list : bool = False) -> str:
        if self.size is None:
            return "BAD SIZE"
        screen = []
        number_line = self.size.lines - (2 - int(no_top) - int(no_bot))
        if self.split_screens == None:
            if not no_top:
                screen.append((self.border["hr"] if no_left else self.border["tl"]) + self.border["hr"] * (self.size.columns - 2) + (self.border["hr"] if no_right else self.border["tr"]))
            for i in range(number_line):
                line = ""
                if (number_line - i) <= len(self.lines):
                    line = self.lines[len(self.lines) - (number_line - i)]
                    for rep in self.apply_change:
                        line = line.replace(rep[0],rep[1])
                    if len(line) > self.size.columns - 2:
                        line = line[:self.size.columns - 5] + "..."
                screen.append((" " if no_left else self.border["vr"]) + line + " " * (self.size.columns - 2 - len(line)) + (" " if no_right else self.border["vr"]))
            if not no_bot:
                screen.append((self.border["hr"] if no_left else self.border["bl"]) + self.border["hr"] * (self.size.columns - 2) + (self.border["hr"] if no_right else self.border["br"]))
            if to_list:
                return screen
            else:
                return self.join_char.join(screen)
        screen1 = self.split_screens[0]
        screen2 = self.split_screens[1]
        if self.split_screens[2] == "h":
            top_screen_str = screen1.__create_screen(no_top,True, no_left, no_right,True)
            bottom_screen_str = screen2.__create_screen(True,no_bot,no_left, no_right,True)
            screen += top_screen_str
            li = (self.border["hr"] if no_left else self.border["cl"])
            for i in range(1,self.size.columns - 1):
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
            left_screen_str = screen1.__create_screen(no_top,no_bot, no_left, True , True)
            right_screen_str = screen2.__create_screen(no_top, no_bot, True,no_right, True)
            screen.append(left_screen_str[0] + (self.border["vr"] if no_top else self.border["ct"]) + right_screen_str[0])
            if len(left_screen_str) != len(right_screen_str):
                raise ValueError("Left and Right screen have different heights")
            for i in range(1,len(left_screen_str)-1):
                md = self.border["vr"]
                if left_screen_str[i][-1] == self.border["hr"] and right_screen_str[i][0] == self.border["hr"]:
                    md = self.border["cc"]
                elif left_screen_str[i][-1] == self.border["hr"] and right_screen_str[i][0] != self.border["hr"]:
                    md = self.border["cr"]
                elif left_screen_str[i][-1] != self.border["hr"] and right_screen_str[i][0] == self.border["hr"]:
                    md = self.border["cl"]
                screen.append(left_screen_str[i] + md + right_screen_str[i])
            screen.append(left_screen_str[-1] + (self.border["vr"] if no_bot else self.border["cb"]) + right_screen_str[-1])

        if to_list:
            return screen

        return self.join_char.join(screen)

    def need_refresh(self,size) -> bool:
        return size != self.size or self.line_changed or self.screen_changed or (self.split_screens is not None and (self.split_screens[0].need_refresh(size) or self.split_screens[1].need_refresh(size)))

    def refresh(self,size):
        self.change_size(size)
        self.refresh_done()

    def refresh_done(self):
        self.line_changed = False
        self.screen_changed = False
        if self.split_screens is not None:
            self.split_screens[0].refresh_done()
            self.split_screens[1].refresh_done()


    #def need_refresh(self,main_fraim:bool = False) -> bool:
    #    size = os.get_terminal_size()
    #    if main_fraim and self.size_old != size:
    #        self.size_old = size
    #        self.change_size(size)
    #        return True
    #    if self.line_changed or self.screen_changed:
    #        self.line_changed = False
    #        self.screen_changed = False
    #        return True
    #    return False if self.split_screens is None else (self.get_screen(1).need_refresh() or self.get_screen(0).need_refresh())
#
#    def __draw_screen_on_terminal(self):
#        if self.need_refresh(True):
#            os.sys.stdout.write("\r"+self.get_terminal_screen())
#            os.sys.stdout.flush()
#
#    def draw_screen_on_terminal(self):
#        if not self.launched:
#            self.__draw_screen_on_terminal()
#        else:
#            raise RuntimeError("Screen is launched in autonome mode, cannot draw manually")