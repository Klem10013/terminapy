#tr = "tr" #Top right
#hr = "hr" #Horizontal
#vr = "vr" #Vertical
#bl = "bl" #Bottom left
#br = "br" #Bottom right
#cl = "cl" #Cross left
#cc = "cc" #Cross center
#cr = "cr" #Cross right
#ct = "ct" #Cross top

class BorderStyle:
    STYLE : dict[str,str] = None
    def __getitem__(self, key):
        return self.STYLE[key]
class ROUNDED_CORNER(BorderStyle):
    STYLE : dict[str,str] = { "tl":"╭", "tr":"╮", "bl":"╰", "br":"╯", "hr":"─", "vr":"│", "cl":"├", "cc":"┼", "cr":"┤", "ct":"┬", "cb":"┴" }
class SQUARE_CORNER(BorderStyle):
    STYLE : dict[str,str] = { "tl":"┌", "tr":"┐", "bl":"└", "br":"┘", "hr":"─", "vr":"│", "cl":"├", "cc":"┼", "cr":"┤", "ct":"┬", "cb":"┴" }
class DOUBLE_LINE_CORNER(BorderStyle):
    STYLE : dict[str,str] = { "tl":"╔", "tr":"╗", "bl":"╚", "br":"╝", "hr":"═", "vr":"║", "cl":"╠", "cc":"╬", "cr":"╣", "ct":"╦", "cb":"╩" }