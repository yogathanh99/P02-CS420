#!/usr/local/bin/python3.7
from misc import *
from random import seed
from random import randint
from game_map import *

import copy

class Deadly:
    def __init__ (self, location):
        self.location = location
        self.symbol = Symbol()
    
class Wumpus(Deadly):
    def __init__ (self, location):
        super().__init__(location) 
        self.my_symbol = self.symbol.wumpus
        self.my_signal = self.symbol.stench

class Pit(Deadly):
    def __init__(self, location):
        super().__init__(location)
        self.my_symbol = self.symbol.pit
        self.my_signal = self.symbol.breeze

class Wall(Deadly):
    def __init__(self, location):
        super().__init__(location)
        self.my_symbol = self.symbol.wall