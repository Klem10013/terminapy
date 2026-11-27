from ..screen import Screen
from .. import border
import textwrap


class TextScreen(Screen):
    def __init__(self,size=None,name:str="",ratio : tuple[float,float] = (1,1), border_style : border.BorderStyle = border.SQUARE_CORNER()):
        self.lines : list[str] = []
        self.line_changed : bool = False
        self.apply_change : list[(str,str)] = []
        super().__init__(size,name,ratio,border_style)

    def need_refresh(self,size) -> bool:
        return self.line_changed or super().need_refresh(size)

    def refresh_done(self):
        self.line_changed = False
        super().refresh_done()

    def clear(self):
        self.line_changed = True
        if self.split_screens is not None:
            self.split_screens[0].clear()
            self.split_screens[1].clear()
        else:
            self.lines.clear()

    def append(self,message:str):
        self.line_changed = True
        if self.split_screens is not None:
            self.split_screens[0].append(message)
            self.split_screens[1].append(message)
        else:
            self.lines.append(message.encode("unicode_escape").decode())

    def apply(self,regex:str,replacement:str):
        pass
        #self.apply_change.append((regex,replacement))
    
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

    def create_screen(self,no_top:bool = False,no_bot:bool = False,no_left:bool = False,no_right:bool = False,to_list:bool = False):
        screen = []
        if self.split_screens is None:
            number_line = self.size.lines - (2 - int(no_top) - int(no_bot))
            nb_line_display = 0
            line_idx = len(self.lines) - 1
            if not no_top:
                screen.append((self.border["hr"] if no_left else self.border["tl"]) + self.border["hr"] * (self.size.columns - 2) + (self.border["hr"] if no_right else self.border["tr"]))
            sc = []
            while nb_line_display < number_line and line_idx >= 0:
                lines = []
                line = self.lines[line_idx]
                for rep in self.apply_change:
                    line = line.replace(rep[0],rep[1])
                for line in line.split("\n"):
                    chunks = textwrap.wrap(line, width=self.size.columns - 3)
                    lines += chunks
                for i in range(len(lines)):
                    line = lines[-i - 1]
                    if nb_line_display >= number_line:
                        break
                    sc.append((" " if no_left else self.border["vr"]) + line + " " * (self.size.columns - 2 - len(line)) + (" " if no_right else self.border["vr"]))
                    nb_line_display += 1
                line_idx -= 1
            for _ in range(number_line-nb_line_display):
                screen.append((" " if no_left else self.border["vr"]) + " " * (self.size.columns - 2) + (" " if no_right else self.border["vr"]))
            sc.reverse()
            screen += sc
            if not no_bot:
                screen.append((self.border["hr"] if no_left else self.border["bl"]) + self.border["hr"] * (self.size.columns - 2) + (self.border["hr"] if no_right else self.border["br"]))
            if to_list:
                return screen
            else:
                return self.join_char.join(screen)
        else:
            return super().create_screen(no_top,no_bot,no_left,no_right,to_list)