#!/usr/bin/python3

from misc import *
from game_map import *

from random import seed
from random import randint        

class Agent:
    def __init__ (self, location, map_dimension):
        self.location = location # a list [x,y], agent current location

        #agents personal map since it can't see the whole world
        self.map = Map(map_dimension[0], map_dimension[1])
        self.legal_actions = ["up","down","left","right"]        
        
        self.symbol = Symbol()
        self.my_symbol = self.symbol.agent

        self.previous = [] #this contains agents previous location, this will help it not to visit back the location when it's possible
        self.signal = [] #the signal in the current room

        self.goal = []
        self.finish = False

        # use for logical inference
        self.breeze_room = []
        self.stench_room = []
        self.deadly = []
        self.flaged_pit = []
        self.flaged_wumpus = []

        self.score = 0

    def get_gold(self):
        self.score = self.score + 100


    def update(self, new_location):
        self.previous = copy.deepcopy(self.location) #update the previous
        self.location = copy.deepcopy(new_location)

    # when the agent enters a room with a signal or no signal at all
    # it will flag surrounding area to remember that there's a pit or a wumpus nearby
    # or mark surounding as safe to proceed
    def flag_surrounding(self, signal):
        pos = copy.deepcopy(get_surounding(self.location))
        x = self.location[0]
        y = self.location[1]
        # mark the current position as safe
        self.map.data[y][x] = [self.symbol.safe]     
        self.map.data[y][x].append(self.symbol.visited)
        #print(pos)
        
        if (self.symbol.breeze == signal):
            print("Cold")
            flag = self.symbol.flag_pit
        
        elif (self.symbol.stench == signal):
            print("Stench")
            flag = self.symbol.flag_wumpus
        

        else:
            flag = self.symbol.safe

            for p in pos:
                x = p[0]
                y = p[1]
                l = [flag] #empty every flags that marked in that room
                # if the room was marked as visited, we don't want to empty that mark
                if (self.symbol.visited in self.map.data[y][x]):
                    l.append(self.symbol.visited)

                self.map.data[y][x] = copy.deepcopy(l)

            return

        for p in pos:
            x = p[0]
            y = p[1]
            #if the position is already marked as safe, we don't want to flag it
            if (self.symbol.safe in self.map.data[y][x]):
                continue
            else:
                l = copy.deepcopy(self.map.data[y][x])
                l.append(flag)
                self.map.data[y][x] = copy.deepcopy(l)

    def current_position_check(self, global_map):
        x = self.location[0]
        y = self.location[1]
        self.signal = [] #empty the previous room signal 
        flag = 0
        # sensing the surounding based on the current room signal
        sense = global_map.view_a_possition(self.location)
        #print(sense)
        print("Agent's location: {}".format(self.location))

        if (self.symbol.stench in sense):
            self.flag_surrounding(self.symbol.stench)
            flag = 1
            self.signal.append(self.symbol.stench)
            if self.location not in self.stench_room:
                self.stench_room.append([self.location[0],self.location[1]])

        if (self.symbol.breeze in sense):
            self.flag_surrounding(self.symbol.breeze)
            flag = 1
            self.signal.append(self.symbol.breeze)
            
            if self.location not in self.breeze_room:
                self.breeze_room.append([self.location[0],self.location[1]])

        if(flag == 0): #there is no deadly signal in the current room
            self.flag_surrounding(self.symbol.safe)
        

    def query_surounding_rooms(self, room_pos, signal):
        # if the current room has a signal and all surounding room is safe except for 1 room
        # then we can pin point that room as the deadly room
        pos = copy.deepcopy(get_surounding(room_pos))

        deadly_x = -1
        deadly_y = -1
        count = len(pos)
        for p in pos:
            x = p[0]
            y = p[1]
            if (self.symbol.safe in self.map.data[y][x]):
                count = count - 1
            else:
                deadly_x = x
                deadly_y = y
        
        if (count == 1):
            #mark the room as wumpus or pit
            x = room_pos[0]
            y = room_pos[1]
            deadly = [deadly_x,deadly_y]

            if (deadly not in self.deadly):
                if (signal == self.symbol.stench):
                    self.map.update(deadly,deadly,self.symbol.wumpus)
                    self.deadly.append(deadly)
                    print("There is a wumpus at {}".format(deadly))

                if (signal == self.symbol.breeze):
                    self.map.update(deadly,deadly,self.symbol.pit)
                    self.deadly.append(deadly)

                    print("There is a pit at {}".format(deadly))
                
    def query_flaged_room(self, room_pos):
        # if a room is flaged and all of it's surrounding rooms are safe
        # then we can 100% sure that the room is flaged correctly
        pos = copy.deepcopy(get_surounding(room_pos))

        count = len(pos)
        for p in pos:
            x = p[0]
            y = p[1]
            if (self.symbol.safe in self.map.data[y][x]):
                count = count - 1
        
            else:
                return
        
        if (count == 0):
            #mark the room as wumpus or pit
            x = room_pos[0]
            y = room_pos[1]
            deadly = [x,y]
            if (deadly not in self.deadly):
                if (self.symbol.flag_wumpus in self.map.data[y][x]):
                    self.map.update(deadly,deadly,self.symbol.wumpus)
                    self.deadly.append(deadly)
                    print("There is a wumpus at {}".format(deadly))

                elif (self.symbol.flag_pit in self.map.data[y][x]):
                    self.map.update(deadly,deadly,self.symbol.pit)
                    self.deadly.append(deadly)
                    print("There is a pit at {}".format(deadly))
                
        

    def find_best_move(self): 
        move = []
        not_visited = []
        pos = copy.deepcopy(get_surounding(self.location))

        count = len(pos)

        for p in pos:
            x = p[0]
            y = p[1]
            if (self.symbol.safe in self.map.data[y][x]):
                move.append(p)

                if (self.symbol.visited not in self.map.data[y][x]):
                    not_visited.append(p)
        
                else:
                    count = count - 1

        # prioritize to vist an unvisted room
        if (len(not_visited) >= 1):
            self.goal = [] # empty the goal
            return not_visited

        if count == 0: #agents has visited all the surounding room
            self.generate_a_goal()
            print("Generating a goal: {}".format(self.goal))
            
            move_to_goal = copy.deepcopy(self.moving_towards_the_goal())
            return move_to_goal

        return move

    def move(self,global_map):
        print("score: {}".format(self.score))
        self.current_position_check(global_map)
        for s in self.signal:
            self.query_surounding_rooms(self.location,s)
        print("*"*4)
        # self.map.map_print()

        best_moves = copy.deepcopy(self.find_best_move())

        self.room_inference()

        if self.finish == True:
            print("The game finish")
            return


        if (len(best_moves) > 1):
            # remove the move that make agent go back to it's last position
            if (self.previous in best_moves):
                best_moves.remove(self.previous)
        
        if len(best_moves) > 1:
            new_location = copy.deepcopy(self.random_move(best_moves))
        else:
            new_location = best_moves[0]
        global_map.update(self.location,new_location,self.symbol.agent)
    
        self.update(new_location)


    def random_move(self, moves):
        value = randint(0,len(moves)-1)
        return moves[value]

# if the agents has visited all of it's surounding room
# then we will make the agent to visit the closet safe-unvisited room 
    def generate_a_goal(self,radius = 3,recursive = 0):
        goals_pos = []
        #x = self.location[0]
        #y = self.location[1]

        shortest = 9999
        for y in range(self.location[1] - radius, self.location[1] + radius +1 ,1):
            if (y<1 or y >= self.map.height):
                continue
            
            for x in range(self.location[0]-radius, self.location[0] +radius + 1, 1):
                if (x<1 or x >= self.map.width) :
                    continue

                tmp = manhattandistance(self.location, [x,y])
                if (self.symbol.visited not in self.map.data[y][x]):
                    if (self.symbol.safe in self.map.data[y][x]): 
                        if (tmp < shortest):
                            goals_pos = [x,y]
                    
        
        if len(goals_pos) == 0: #increase the radius if there is no goal found!
            if recursive == 0:
                self.generate_a_goal(10,1)
            else:
                self.finish = True
        else:
            self.goal = copy.deepcopy(goals_pos)

    # this function will only be invoke when agent has visited all the surrounding rooms
    # it will guid the agents to the direction of the goal 
    def moving_towards_the_goal(self):
        if len(self.goal) == 0: # agent currently has no goal
            return

        direction = []
        # calculating the direction that agents need to head in orders to get to the goal
        x_goal = self.goal[0]
        y_goal = self.goal[1]

        x = self.location[0]
        y = self.location[1]

        if (x_goal < x): # need to go to the left
            direction.append("left")

        elif (x_goal > x):
            direction.append("right")

        if (y_goal < y): # need to go up
            direction.append("up")

        elif (y_goal > y): # need to go down
            direction.append("down")

        print(direction)
        move = copy.deepcopy(get_surounding(self.location,direction))
        print(move)
        return move

    def room_inference(self):
        for r in self.breeze_room:
            self.query_surounding_rooms(r,self.symbol.breeze)
        for r in self.stench_room:
            self.query_surounding_rooms(r,self.symbol.stench)

        for r in self.flaged_pit:
            self.query_flaged_room(r)
        for r in self.flaged_wumpus:
            self.query_flaged_room(r)
        
    def agent_die(self):
        self.score = self.score - 10000
        print("Agent die!")