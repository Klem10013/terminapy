class ScreenTypeEnum(object):

    BASIC = "BASIC_SCREEN"
    TEXT  = "TEXT_SCREEN"
    GRAPH = "GRAPH_SCREEN"
    INPUT = "INPUT_SCREEN"

    @staticmethod
    def BASIC_m():
        return ScreenTypeEnum("BASIC_SCREEN")
    @staticmethod
    def TEXT_m():
        return ScreenTypeEnum("TEXT_SCREEN")
    @staticmethod
    def GRAPH_m():
        return ScreenTypeEnum("GRAPH_SCREEN")
    @staticmethod
    def INPUT_m():
        return ScreenTypeEnum("INPUT_SCREEN")

    def __init__(self,value):
        self.value = value

    def __eq__(self,other):
        if isinstance(other,ScreenTypeEnum):
            return self.value == other.value
        return False
        

ScreenTypeEnum.BASIC = ScreenTypeEnum("BASIC_SCREEN")
ScreenTypeEnum.TEXT  = ScreenTypeEnum("TEXT_SCREEN")
ScreenTypeEnum.GRAPH = ScreenTypeEnum("GRAPH_SCREEN")
ScreenTypeEnum.INPUT = ScreenTypeEnum("INPUT_SCREEN")