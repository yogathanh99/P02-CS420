#!/usr/local/bin/python3.7

class Symbol:
    def __init__(self):
        self.agent = "A"
        self.pit = "P"
        self.gold = "G"
        self.wumpus = "W"
        self.empty = " "
        self.breeze = "B"
        self.stench = "S"
        self.wall = "%"
        self.flag_pit = "!p"
        self.flag_wumpus = "!w"
        self.safe = "@"
        self.visited = "V"
def manhattandistance(possition, destination):
    return abs(possition[0] - destination[0] ) + abs( possition[1] - destination[1] )

def unique_sort_list(my_list):
    unique = []
    for i in my_list:
        if i not in unique:
            unique.append(i)

def get_surounding(possition, direction=["left","right","up","down"], width = 10, height=10):
    pos = []
    x = possition[0]
    y = possition[1]

    if ("left" in direction):
#        print("left in direction")
        #if (x > 0):
        if (x > 1):
            left = [x-1,y]
            pos.append(left)

    if ("right" in direction):
#        print("right in direction")
        #if (x < width-1):
        if(x< width-1):
            right = [x+1,y]
            pos.append(right)

    if ("up" in direction):
#       print("up in direction")
        # if (y > 0):
        if (y>1):
            top = [x,y-1]
            pos.append(top)

    if ("down" in direction):
#        print("down in direction")
        # if (y < height - 1):
        if (y<height-1):
            down = [x,y+1]
            pos.append(down)

    #print (pos)
    return pos