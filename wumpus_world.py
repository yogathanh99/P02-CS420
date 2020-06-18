#!/usr/bin/python3
from game_map import*
from misc import *
from agent import *
from wumpus import *

import sys,getopt
import copy

symbol = Symbol()
score = 0

#Don't let the agent move out side the map
def get_legal_actions(agent, Map):
    x = agent.location[0]
    y = agent.location[1]

    #reset the legal actions before striping the illegal
    agent.legal_actions = ["up","left","down","right"]
    if (x > 0):
        if (symbol.wall in Map.data[y][x-1]):
            agent.remove_actions("left")

    else:
        agent.remove_actions("left")

    if (x < Map.width -1):
        if (symbol.wall in Map.data[y][x+1]):
            agent.remove_actions("right")

    else:
        agent.remove_actions("right")

    if (y > 0):
        if (symbol.wall in Map.data[y-1][x]):
            agent.remove_actions("up")

    else:
        agent.remove_actions("up")

    if (y < Map.height - 1):
        if (symbol.wall in Map.data[y+1][x]):
            agent.remove_actions("down")

    else:
            agent.remove_actions("down")

def state_check(agents, global_map):
    x = agents.location[0]
    y = agents.location[1]

    # there is gold at agents's current location
    if symbol.gold in global_map.data[y][x]:
        result = agents.get_gold()
        global_map.remove_gold([x,y])
    
    # there is a wumpus or pit at agents's current location
    if (symbol.wumpus in global_map.data[y][x]):
        print("agents die")
        return True

    if (symbol.pit in global_map.data[y][x]):
        agents.agent_die()
        print("agents die")
        return True

    if (agents.finish == True):
        print("Agent has visited every room!")
        return True
    return False

    
def main(argv):
    #generate maps
    try:
      opts, args = getopt.getopt(argv,"hm:l:",["ifile="])
    except getopt.GetoptError:
      print ('test.py -m <Map>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
        print ('test.py -m <Map>')
        sys.exit()
      elif opt in ("-m", "--ifile"):
         wall = arg

    #generate agents location
    wallFile = "walls_" + wall + ".txt"


    score = 0
    # define a 10 X 10 map
    global_map = Map(12, 12)
    gold_pos=[]

    map_dimension = global_map.map_dimension()

    # initialize pacman and monster locations
    deadly = []
    agent=[]
    agents = []
    wall_pos=[]

    with open(wallFile, 'r',) as file:
        for y, line in enumerate(file):
            count=0
            for x, strs in enumerate(line):
                # COINS
                if strs == "G":
                    gold_pos.append([x-count+1,y])
                    count+=1
                # AGENT
                elif strs == "A":
                    agent = Agent([x-count+1,y-1],map_dimension)
                    agents=[agent]
                    count+=1
                # PIT
                elif strs=="P":
                    deadly.append(Pit([x-count+1,y]))
                    count+=1
                # WUMPUS
                elif strs=="W":
                    deadly.append(Wumpus([x-count+1,y]))
                    count+=1
                elif strs!=".":
                    count+=1
        

    gold_number = len(gold_pos)
    # add agents into the map
    global_map.load_agents(agents)

    #add deadly into the map
    global_map.load_deadly(deadly)

    # add gold into the map
    global_map.load_gold(gold_pos)
    
    # add wall into the map
    for y in range(0,11):
        for x in range(0,11):
            if x==0: 
                wall_pos.append([x,y])
            elif x==10: 
                wall_pos.append([x,y])
            elif y==0:
                wall_pos.append([x,y])
            elif y==10:
                wall_pos.append([x,y])
    global_map.load_wall(wall_pos)
    global_map.map_print()

    #state_check(agent, global_map)


    i = 150 # a variable just to make the loop stop, removing later

    finish = False

    finish = state_check(agent, global_map)

    while (True):
        
        #get_legal_actions(agent,global_map)

        agent.move(global_map)

    
        finish = state_check(agent, global_map)
        global_map.map_print()

        if finish:
            print ("The game finish in {} steps".format(150 - i))
            break

        i = i - 1
        if (i <= 0):
            print("Preemptive to end the game")
            break


if __name__ == "__main__":
    main(sys.argv[1:]) 