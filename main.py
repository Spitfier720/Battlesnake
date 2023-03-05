import random
import typing

NAME = "aeiou"

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": NAME,  # TODO: Your Battlesnake Username
        "color": "#DE73FF",  # TODO: Choose color
        "head": "gamer",  # TODO: Choose head
        "tail": "mouse",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(gameState: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(gameState: typing.Dict):
    print("GAME OVER\n")

#Helper function to make the grid and its respective items
def makeGrid(w, h, g):
    grid = []
    
    for x in range(w):
        row = []
        
        for y in range(h):
            row.append(".")

        grid.append(row)

    for x in g["board"]["food"]:
        grid[h - x["y"] - 1][x["x"]] = "F"

    #Make sure not to add the tail.
    for x in g["board"]["snakes"]:
        for y in range(len(x["body"]) - 1):
            if(y == 0):
                grid[h - x["body"][y]["y"] - 1][x["body"][y]["x"]] = "H"

            elif(grid[h - x["body"][y]["y"] - 1][x["body"][y]["x"]] == "."):
                grid[h - x["body"][y]["y"] - 1][x["body"][y]["x"]] = "S"
    
    return grid

#Finding the optimal move depending on a number of factors.
def findMove(g, w, t, h, d):
    dirToCoordChange = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }
    
    maxCount = 0
    bestDirs = []
    
    for i in dirToCoordChange:
        x, y = h["x"] + dirToCoordChange[i][1], t - h["y"] - 1 + dirToCoordChange[i][0]

        #Preventing disadvantageous head to heads.
        hthb = False
        
        for j in d["board"]["snakes"]:
            if(j["id"] == NAME):
                continue
            
            ox, oy = j["body"][0]["x"], j["body"][0]["y"]

            if(abs(h["x"] - ox) + abs(h["y"] - oy) == 1 and len(d["you"]["body"]) <= len(j["body"])):
                hthb = True
                break

        if(hthb):
            continue
            
        count = 0

        
        while(0 <= x < w and 0 <= y < t and (g[y][x] == "." or g[y][x] == "F")):
            #Prioritize food when health goes below a critical point
            if(d["you"]["health"] <= 40 and g[y][x] == "F"):
                return i
            
            x += dirToCoordChange[i][1]
            y += dirToCoordChange[i][0]
            count += 1

        #Update or recreate the list of best moves too randomly choose from.
        if(count == maxCount):
            bestDirs.append(i)

        elif(count > maxCount):
            bestDirs = [i]
            maxCount = count

    return random.choice(bestDirs)
        
#Pretty printing our 2d list.
def toString(g):
    for x in g:
        for y in x:
            print(y, end = " ")

        print()
    
# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data

#Using floodfill
def move(gameState: typing.Dict) -> typing.Dict:
    boardWidth = gameState['board']['width']
    boardHeight = gameState['board']['height']
    myHead = gameState["you"]["body"][0]

    grid = makeGrid(boardWidth, boardHeight, gameState)

    bestMove = findMove(grid, boardWidth, boardHeight, myHead, gameState)
    
    return {"move": bestMove}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
