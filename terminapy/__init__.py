from main import ScreenManager
from screen import Screen
from screenType.textScreen import TextScreen
from screenType.graphScreen import GraphScreen, Graph, Bar, Scatter
from border import *

#As python is an interpreted language no library will be importer at runtime so if you want tu use this lib but you do not have
#some dependencies you can still use the other part of the library without problem
#like ScreenManager.full_autonome will only import Thread from threading only if you call this function so if you do not have threading installed your python
#Does not support this lib you can still use the rest of the library without problem

#In the code some element are not well typed to avoid using unecessary imports

#And some imports are done inside functions (again to avoid importing unecessary modules)
#like in ScreenManager.full_autonome where autonomie is imported inside the function