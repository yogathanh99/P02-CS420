#!/usr/local/bin/python3
import copy
import pygame

from misc import *
from settings import *

class Map:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.symbol = Symbol()

        #GENERATE AN OPEN EMPTY MAP
        #this should be the map loading stage
        empty_list = []
        self.data = [[ empty_list for y in range(height)] for x in range(width)]#initialize the map data[y-coordinate][x-coordinate]
        
        # this is for agents to check if it's scan the whole map yet
        self.checked = [[0 for y in range(height)] for x in range(width)]
        self.screen=pygame.display.set_mode((WIDTH, HEIGHT))
        self.cellWidth = MAZE_WIDTH // COLS
        self.cellHeight = MAZE_HEIGHT // ROWS

    # update all the agents new location
    def update(self, agents_location, agents_new_coordinate, agent_symbol):

        x = agents_location[0]
        y = agents_location[1]

        new_x = agents_new_coordinate[0]
        new_y = agents_new_coordinate[1]

        # do not update when the room has pit or wumpus
        if(self.symbol.wumpus in self.data[y][x]):
            return

        if(self.symbol.pit in self.data[y][x]):
            return
        
        if (agent_symbol == self.symbol.wumpus) or (agent_symbol == self.symbol.pit):
            self.data[y][x] = [agent_symbol]
            return 

        # removing the agent from the old location
        try:
            self.data[y][x].remove(agent_symbol)
            if len(self.data[y][x]) == 0:
                self.data[y][x] = copy.deepcopy([])

        except ValueError:
            pass
        #update agent's new location
        l = copy.deepcopy(self.data[new_y][new_x])
        l.append(agent_symbol)
        self.data[new_y][new_x] = copy.deepcopy(l)

    def map_print(self):
        #print (self.data)
        # for y in range(self.height):
        #     print(self.data[y])
            

        # print ("\n")
        self.screen.fill(BLACK)
        for y in range(self.height):
            for x in range(self.width):
                if self.symbol.agent in self.data[y][x]:
                    pygame.draw.circle(self.screen, PLAYER_COLOR,
                        (int(x*self.cellWidth) + self.cellWidth//2 + TOP_BOTTOM_BUFFER//2, int(y*self.cellHeight) + self.cellHeight//2 + TOP_BOTTOM_BUFFER//2), self.cellWidth//2-2)
                elif self.symbol.pit in self.data[y][x]:
                    pygame.draw.rect(self.screen, GREEN, (x*self.cellWidth + TOP_BOTTOM_BUFFER//2, 
                        y*self.cellHeight + TOP_BOTTOM_BUFFER//2, self.cellWidth//2, self.cellHeight//2))
                elif self.symbol.gold in self.data[y][x]:
                    pygame.draw.circle(self.screen, YELLOW, (int(
                        x*self.cellWidth) + self.cellWidth//2 + TOP_BOTTOM_BUFFER//2, int(y*self.cellHeight) + self.cellHeight//2 + TOP_BOTTOM_BUFFER//2), 5)
                elif self.symbol.wumpus in self.data[y][x]:
                    pygame.draw.rect(self.screen, RED, (x*self.cellWidth + TOP_BOTTOM_BUFFER//2, 
                        y*self.cellHeight + TOP_BOTTOM_BUFFER//2, self.cellWidth, self.cellHeight))
                elif self.symbol.wall in self.data[y][x]:
                    pygame.draw.rect(self.screen, (52, 82, 235), (x*self.cellWidth + TOP_BOTTOM_BUFFER//2, 
                        y*self.cellHeight + TOP_BOTTOM_BUFFER//2, self.cellWidth, self.cellHeight))
        pygame.display.update()
        pygame.time.delay(300)
        print ("\n")
    def view_a_possition(self,possition):
        x = possition[0]
        y = possition[1]
        out = self.data[y][x]
        return out

    def map_dimension(self):
        return [self.width, self.height]

    def load_gold(self, golds):
        for i in golds:
            self.update(i,i,self.symbol.gold)

    def load_wall(self, walls):
        for i in walls:
            self.update(i,i,self.symbol.wall)

    def load_agents(self, agents):
        for a in agents:
            self.update(a.location, a.location, a.my_symbol)

    def remove_gold(self, gold_location):
        x = gold_location[0]
        y = gold_location[1]

        try:
            self.data[y][x].remove(self.symbol.gold)
        except:
            pass


    def load_deadly(self, deadly):
        for i in deadly:
            self.update(i.location,i.location, i.my_symbol)
            #update the surounding with it's signal
            pos = get_surounding(i.location)
            for coordinate in pos:
                self.update(coordinate,coordinate, i.my_signal)

