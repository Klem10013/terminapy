import os
import select
import sys
import termios
import tty
import codecs
import atexit
import signal


from enum import Enum
from collections.abc import Callable
from ..screen import Screen
from .. import border

class InputType(str,Enum):
    Cbreak  = "Cbreak"
    Raw     = "Raw"


class InputScreen(Screen):

    def __init__(self,
                size=None,
                name:str="",
                ratio : tuple[float,float] = (1,1), 
                border_style : border.BorderStyle = border.SQUARE_CORNER(),
                submit : Callable[[str],None] = None,
                clean_on_submit : bool = True,
                quit : Callable[[],None] = None,
                is_cbreak : bool = True,
                timeout : float = 0.03,
                cursor : str = "█",
                prompt : str = ">",
                skip_escape_char : bool = True,):
        self.clean_on_submit = clean_on_submit
        self.timeout = timeout
        self.submit  = submit
        self.quit    = quit
        self.data    = ""
        self.data_changed : bool = False

        #init all input params
        self.fd = sys.stdin.fileno()
        self.old_flags = termios.tcgetattr(self.fd)
        self.decoder = codecs.getincrementaldecoder("utf-8")("ignore")
        self._restores = False

        self.escape = -1 if skip_escape_char else 0
        self.cursor = cursor
        self.prompt = prompt

        atexit.register(self.close)
        self._install_signal_handlers()
        self._install_excepthook()


        if is_cbreak:
            tty.setcbreak(self.fd)
        else:
            tty.setraw(self.fd)



        super().__init__(size,name,ratio,border_style)


    def _install_signal_handlers(self):
        def handler(signum, frame):
            self.close()
            signal.signal(signum, signal.SIG_DFL)
            os.kill(os.getpid(), signum)

        for sig in (signal.SIGTERM, signal.SIGHUP):
            try:
                signal.signal(sig, handler)
            except (ValueError, OSError):
                pass  # pas dans le thread principal

    def _install_excepthook(self):
        previous = sys.excepthook

        def hook(exc_type, exc, tb):
            self.close()          # restaure AVANT d'afficher le traceback
            previous(exc_type, exc, tb)

        sys.excepthook = hook

    def close(self):
        if self._restores:
            return
        self._restores = True
        try:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_flags)
        except termios.error:
            pass
        try:
            # réaffiche le curseur
            sys.stdout.write("\x1b[?25h")
            sys.stdout.flush()
        except Exception:
            pass

    def _read(self, timeout: float) -> list[str]:
        if not select.select([self.fd], [], [], timeout)[0]:
            return []
        return list(self.decoder.decode(os.read(self.fd, 1024)))

    def handle_key(self, ch: str, submit : Callable[[str],None] = None ):
        """Traite une touche. Retourne False pour quitter."""
        if self.escape > 0:  # on ignore les séquences du type ESC [ A
            if self.escape == 1:
                self.escape = 2 if ch in "[O" else 0
            elif "@" <= ch <= "~":
                self.escape = 0
            return
 
        if self.escape != -1 and ch == "\x1b":
            self.escape = 1
        elif ch in ("\x03", "\x04"):  # Ctrl+C / Ctrl+D
            if self.quit is not None:
                self.quit()
            else:
                raise KeyboardInterrupt
        elif ch in ("\r", "\n"):
            if submit is not None:
                submit(self.data)
            if (self.clean_on_submit):
                self.data = ""
        elif ch in ("\x7f", "\x08"):  # retour arrière
            self.data = self.data[:-1]
        elif ch == "\x15":  # Ctrl+U
            self.data = ""
        elif ch.isprintable():
            self.data += ch

    def need_refresh(self, size) ->  bool:
        return self.data_changed or super().need_refresh(size)

    def refresh_done(self):
        self.data_changed = False
        return super().refresh_done()

    def get_input(self,submit : Callable[[str],None] = None) -> str:
        submit = self.submit if submit is None else submit
        for ch in self._read(self.timeout):
            self.handle_key(ch,submit)
            self.data_changed = True
        return self.data

    def force_submit(self):
        self.submit(self.data)
        self.data_changed = True
        if (self.clean_on_submit):
            self.data = ""

    def clear(self):
        self.data_changed = True
        if self.split_screens is not None:
            self.split_screens[0].clear()
            self.split_screens[1].clear()
        else:
            self.data = ""

    def get_data(self):
        return self.data

    def create_screen(self,no_top:bool = False,no_bot:bool = False,no_left:bool = False,no_right:bool = False,to_list:bool = False):
        screen = []
        if self.split_screens is None:
            number_line = self.size.lines - (2 - int(no_top) - int(no_bot))
            number_column = self.size.columns - 2
            if not no_top:
                screen.append((self.border["hr"] if no_left else self.border["tl"]) + self.border["hr"] * number_column + (self.border["hr"] if no_right else self.border["tr"]))
            for i in range(number_line):
                line = ""
                if i == number_line//2:
                    line = self.prompt + self.data[::] + self.cursor
                    if len(line) > self.size.columns - 2:
                        line = line[:self.size.columns - 5] + "..."
                screen.append((" " if no_left else self.border["vr"]) + line + " " * (self.size.columns - 2 - len(line)) + (" " if no_right else self.border["vr"]))
            if not no_bot:
                screen.append((self.border["hr"] if no_left else self.border["bl"]) + self.border["hr"] * number_column + (self.border["hr"] if no_right else self.border["br"]))

            if to_list:
                return screen
            else:
                return self.join_char.join(screen)
        else:
            return super().create_screen(no_top,no_bot,no_left,no_right,to_list)


