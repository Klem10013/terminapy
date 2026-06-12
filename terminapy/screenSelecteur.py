from .screenType.screenTypeEnum import ScreenTypeEnum as scType
from .screen import Screen
from .screenType import *

def get_screen_type(screen_type : scType):
    if screen_type == scType.BASIC:
        return Screen()
    elif screen_type == scType.GRAPH:
        return GraphScreen()
    elif screen_type == scType.TEXT:
        return TextScreen()
    else:
        raise ValueError("Invalid screen type")