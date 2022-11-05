# Bashir is smarter than me, credit him
#False
# import json
import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Basphir & Micheel",  # TODO: Your Battlesnake Username
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


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(gameState: typing.Dict) -> typing.Dict:
    # with open("gameData.json", "w") as f:
    #     json.dump(dict(gameState), f, indent = 4, ensure_ascii = False)
	
    isSafeMove = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }
    
    # We've included code to prevent your Battlesnake from moving backwards
    myHead = gameState["you"]["body"][0]  # Coordinates of your head

    upCoords = {"x": myHead["x"], "y": myHead["y"] + 1}
    rightCoords = {"x": myHead["x"] + 1, "y": myHead["y"]}
    downCoords = {"x": myHead["x"], "y": myHead["y"] - 1}
    leftCoords = {"x": myHead["x"] - 1, "y": myHead["y"]}

    boardWidth = gameState['board']['width']
    boardHeight = gameState['board']['height']
    
    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    if (gameState["you"]["health"] < 40):
        food = gameState['board']['food']

        shortestDist = 99999999
        closestCoords = {}
        for coords in food:
            distAway = abs(myHead["x"] - coords["x"]) - abs(myHead["y"] - coords["y"])
            if(distAway < shortestDist and distAway < 4):
                closestCoords = {"x": coords["x"], "y": coords["y"]}

        if (closestCoords["x"] > myHead["x"]):
            isSafeMove["right"] = True
        elif (closestCoords["x"] < myHead["x"]):
            isSafeMove["left"] = True
        if (closestCoords["y"] > myHead["y"]):
            isSafeMove["up"] = True
        elif (closestCoords["y"] < myHead["y"]):
            isSafeMove["down"] = True
    
    #Step 2 & 3 combined, working on not running into self + others
    #allSnakes is a list of dicts that contains bad x-y pairs that MUST be avoided

    #allSnakes should include:
        #body parts of all snakes, including ourselves
        #DONT include tails of all snakes
        #include next move possibilities of all opponent snakes
    allSnakes = []
    for snake in gameState['board']['snakes']:
        for i in range(len(snake["body"]) - 1):
            allSnakes.append(snake["body"][i])
        if snake["name"] != "Basphir & Micheel":
            #add an extra items for each opponent to allSnakes
            allSnakes.append({"x": snake["body"][0]["x"] + 1, "y": snake["body"][0]["y"]})
            allSnakes.append({"x": snake["body"][0]["x"] - 1, "y": snake["body"][0]["y"]})
            allSnakes.append({"x": snake["body"][0]["x"], "y": snake["body"][0]["y"] + 1})
            allSnakes.append({"x": snake["body"][0]["x"], "y": snake["body"][0]["y"] - 1})
            allSnakes.append({"x": snake["body"][0]["x"] + 2, "y": snake["body"][0]["y"]})
            allSnakes.append({"x": snake["body"][0]["x"] -2 , "y": snake["body"][0]["y"]})
            allSnakes.append({"x": snake["body"][0]["x"], "y": snake["body"][0]["y"] + 2})
            allSnakes.append({"x": snake["body"][0]["x"], "y": snake["body"][0]["y"] - 2})
        # else:
        #     if snake["body"][0]["x"] + 1 >= boardWidth or {"x": snake["body"][0]["x"] + 1, "y": snake["body"][0]["y"]} in snake["body"]:
        #         allSnakes.append({"x": snake["body"][0]["x"] + 1, "y": snake["body"][0]["y"]})
        #     if snake["body"][0]["x"] - 1 <= 0 or {"x": snake["body"][0]["x"] + 1, "y": snake["body"][0]["y"]} in snake["body"]:
        #         allSnakes.append({"x": snake["body"][0]["x"] - 1, "y": snake["body"][0]["y"]})
        #     if snake["body"][0]["y"] + 1 >= boardHeight or {"x": snake["body"][0]["x"] + 1, "y": snake["body"][0]["y"]} in snake["body"]:
        #         allSnakes.append({"x": snake["body"][0]["x"], "y": snake["body"][0]["y"] + 1})
        #     if snake["body"][0]["y"] - 1 <= 0 or {"x": snake["body"][0]["x"] + 1, "y": snake["body"][0]["y"]} in snake["body"]:
        #         allSnakes.append({"x": snake["body"][0]["x"], "y": snake["body"][0]["y"] - 1})
            

    for coords in allSnakes:
        if(upCoords["x"] == coords["x"] and upCoords["y"] == coords["y"]):
            isSafeMove["up"] = False
        
        if(rightCoords["x"] == coords["x"] and rightCoords["y"] == coords["y"]):
            isSafeMove["right"] = False

        if(downCoords["x"] == coords["x"] and downCoords["y"] == coords["y"]):
            isSafeMove["down"] = False

        if(leftCoords["x"] == coords["x"] and leftCoords["y"] == coords["y"]):
            isSafeMove["left"] = False

    #Preventing Battlesnake from moving out of bounds
    if(myHead["x"] <= 0):
        isSafeMove["left"] = False
        
    elif(myHead["x"] >= boardWidth - 1):
        isSafeMove["right"] = False
        
    if(myHead["y"] <= 0):
        isSafeMove["down"] = False
        
    elif(myHead["y"] >= boardHeight - 1):
        isSafeMove["up"] = False
    
    # Are there any safe moves left?
    safeMoves = []
    for x in isSafeMove:
        if(isSafeMove[x]):
            safeMoves.append(x)

    if(not safeMoves): #edit later
        print(f"MOVE {gameState['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    nextMove = random.choice(safeMoves)

    print(f"MOVE {gameState['turn']}: {nextMove}")
    return {"move": nextMove}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
