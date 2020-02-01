import sys, os, json
from functools import reduce
from os import system, name, sys
assert sys.version_info >= (3,7), "This script requires at least Python 3.7"

# load the location JSON file
game_file = 'locations.json'

# fancy function to clear the terminal for a new game
def clear(): 
  
    # clear terminal for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # clear terminal for mac and linux
    else: 
        _ = system('clear') 

def load_files():
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, game_file)) as json_file: game = json.load(json_file)
        return game
    except:
        print("There was a problem reading either the game or item file.")
        os._exit(1)

# function shows the current world,
# according to what the location json describes
def draw_world(game, current_location):
    # retrieve the room properties from json file such as name, description, items, etc...
    location_properties = game[current_location]

    # print room name and its associated description
    #print(f"You are in the {location_properties['name']}")
    print(location_properties["name"])
    print(location_properties['desc'])

# returns the input of the user
# inputs are uppercased and stripped to be compatible with json
def get_input():
    response = input(">>>")
    response = response.strip().upper()
    return response

def update_room(game, current_location, response):
    location_properties = game[current_location]

    #reduce(lambda a,b: a['target'] if (a['target'] == response) else b['target'], location_properties['exits'])

    for exits_in_current_room in location_properties['exits']:
        if response == exits_in_current_room['exit']:
            return exits_in_current_room['target']
    
    return current_location


def main():

    current_location = 'START'

    game = load_files()

    while True:
        # render and show the current room to the player
        clear()
        draw_world(game, current_location)

        # get a response from the user
        response = get_input()
        
        # change the current to where the user wants to go
        current_location = update_room(game, current_location, response)

        # if the current room is the end, ask to play again
        if(game[current_location]['name'] == 'this is the end'):
            clear()
            print("You escaped the monster!")
            response = input("Play again? Y/N").lower().strip()
            if response == "no" or response == "n":
                break
            # if the users want to play again, reset the current room to START
            current_location = 'START'
        
        # if the current is the death room, kill the player and ask to restart the game
        if game[current_location]['name'] == 'MAIN FLOOR ELEVATOR':
            clear()
            print("You sprint for the elevator and press the door close. The necrotizing monster hears the elevator bell ring and leaps towards the elevator. Its right arm squeezes through the elevator door but the doors snap it off.")
            print("You hear thuds and movements around the elevator...")
            print("Liquid drips on your neck as you look up to see the hidious monster.")
            print("-----GAME OVER-----")
            response = input("Try again? Y/N").lower().strip()
            if response == "no" or response == "n":
                break
            # if the users want to play again, reset the current room to START
            current_location = 'START'
print("->HOW TO PLAY: each room has 2 exits. To go back, type BACK. To go forward into another room, type its name (indicated by capital letters).\n\n")
input("Understood?")
main()
print("Thanks for playing")
