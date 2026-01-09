from screen import Screen
import border

class Graph: 
    def __init__(self):
        pass

    def draw_screen(self,lines:int,columns:int) -> list[str]:
        return [" " * columns for _ in range(lines)]
    
    def add_data(self,*args, **kwargs):
        pass

    def overwrite_data(self,*args, **kwargs):
        pass

    def clear(self):
        pass

    def get_data(self):
        pass

    def copy(self):
        return Graph()

class Scatter(Graph):
    def __init__(self):
        self.scale = [" ", ".", ",","-","~",":",";","+","=","*","%","@","$","#"]
        self.scale_len = len(self.scale)
        self.max_data : list[float,float] = [1,1]
        self.data : list[tuple(float,float)] = []

    def get_data(self):
        return self.data

    def add_data(self,x :float,y :float) -> None:
        self.data.append((y,x))
        if x > self.max_data[1]:
            self.max_data[1] = x
        if y > self.max_data[0]:
            self.max_data[0] = y

    def add_multiple(self, data = list[tuple[float,float]]) -> None:
        for i in data:
            self.add_data(i[0],i[1])

    def clear(self):
        self.max_data = [0,0]
        self.data.clear()

    def copy(self):
        copy = Scatter()
        copy.data = self.data[:]
        return copy

    def draw_screen(self,lines:int,columns:int) -> list[str]:
        if lines == 0 or columns == 0:
            return [" " * columns for _ in range(lines)]
        max_on_one_square = 1
        screen = [ [" " for _ in range(columns)]  for _ in range(lines)]
        point = {}
        for i in self.data:
            y = int((i[0]/self.max_data[0])*(lines - 1))
            x = int((i[1]/self.max_data[1])*(columns - 1))
            if point.get((x,y)) is not None:
                point[(x,y)] += 1
            else:
                point[(x,y)] = 1
            if point[(x,y)] > max_on_one_square:
                max_on_one_square = point[(x,y)]
        for key,value in point.items():
            char_index = int((value/max_on_one_square)*(self.scale_len - 1))
            draw_char = self.scale[char_index]
            screen[key[1]][key[0]] = draw_char
        for i in range(len(screen)):
            screen[i] = "".join(screen[i])
        return screen


class Bar(Graph):
    def __init__(self,bar_name : list[str]):
        self.max_data = 1
        self.data : dict[str,float] = { name:0.0 for name in bar_name }

    def get_data(self):
        return self.data

    def add_data(self,name:str,value:float):
        if name in self.data:
            self.data[name] += value
        else:
            self.data[name] = value
        if value > self.max_data:
            self.max_data = value

    def overwrite_data(self,name:str,value:float):
        self.data[name] = value
        if value > self.max_data:
            self.max_data = value

    def clear(self):
        self.max_data = 0
        for key in self.data:
            self.data[key] = 0.0

    def copy(self):
        copy = Bar()
        copy.data = self.data[:]
        copy.max_data = self.max_data
        return copy

    def draw_screen(self,lines:int,columns:int) -> list[str]:
        l = len(self.data)
        if l == 0 or l*2>columns:
            return [" " * columns for _ in range(lines)]
        screen = []
        #Use to put the caption at the bottom
        lines = lines - 1
        max_value = self.max_data
        bar_width = columns // (l*2)
        rest = columns % (l*2)
        b2 = bar_width // 2
        for line in range(lines):
            row = " " * (rest//2)
            for name, value in self.data.items():
                bar_height = int((value / max_value) * lines) if (max_value > 0) else 0
                if lines - line <= bar_height:
                    row += " " * (b2+ bar_width%2) + "█" * bar_width + " " * b2
                else:
                    row += " " * (2 * bar_width)
            row += " " * (rest//2 + rest%2)
            screen.append(row)
        row = " " * (rest//2)
        for name in self.data.keys():
            if bar_width<len(name):
                name = name[0:bar_width-1]+"."
            name2 = (bar_width - len(name)) // 2
            name_mod = (bar_width - len(name)) % 2
            row += " " * ( b2 + bar_width%2) + " " * name2 + name + " " * (name2 + name_mod) + " " * b2
        row += " " * (rest//2 + rest%2)
        screen.append(row)

        return screen
    

class GraphScreen(Screen):
    def __init__(self,size=None,name:str="",ratio : tuple[float,float] = (1,1), border_style : border.BorderStyle = border.SQUARE_CORNER(), graph : Graph = Graph()):
        self.graph = graph
        self.data_changed : bool = False
        super().__init__(size,name,ratio,border_style)
    
    def need_refresh(self,size) -> bool:
        return self.data_changed or super().need_refresh(size)

    def refresh_done(self):
        super().refresh_done()

    def init_split_screen(self, ratio):
        return GraphScreen(self.size,"",ratio,self.border,self.graph)

    def add_data(self,*args, **kwargs):
        self.data_changed = True
        if self.split_screens is not None:
            self.split_screens[0].add_data(*args, **kwargs)
            self.split_screens[1].add_data(*args, **kwargs)
        else:
            self.graph.add_data(*args, **kwargs)

    def overwrite_data(self,*args, **kwargs):
        self.data_changed = True
        if self.split_screens is not None:
            self.split_screens[0].overwrite_data(*args, **kwargs)
            self.split_screens[1].overwrite_data(*args, **kwargs)
        else:
            self.graph.overwrite_data(*args, **kwargs)
    
    def clear(self):
        self.data_changed = True
        if self.split_screens is not None:
            self.split_screens[0].clear()
            self.split_screens[1].clear()
        else:
            self.graph.clear()

    def create_screen(self,no_top:bool = False,no_bot:bool = False,no_left:bool = False,no_right:bool = False,to_list:bool = False):
        screen = []
        if self.split_screens is None:
            number_line = self.size.lines - 2
            number_column = self.size.columns - 2
            graph_screen = self.graph.draw_screen(number_line,number_column)

            if not no_top:
                screen.append((self.border["hr"] if no_left else self.border["tl"]) + self.border["hr"] * number_column + (self.border["hr"] if no_right else self.border["tr"]))
            for i in range(len(graph_screen)):
                screen.append((" " if no_left else self.border["vr"]) + graph_screen[i] + (" " if no_right else self.border["vr"]))
            if not no_bot:
                screen.append((self.border["hr"] if no_left else self.border["bl"]) + self.border["hr"] * number_column + (self.border["hr"] if no_right else self.border["br"]))
            if to_list:
                return screen
            else:
                return self.join_char.join(screen)
        else:
            return super().create_screen(no_top,no_bot,no_left,no_right,to_list)

    def get_data(self):
        return self.graph.get_data()