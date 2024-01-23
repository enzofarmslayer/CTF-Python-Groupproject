import images
import pygame
import argparse
import json


class Map:
    """ An instance of Map is a blueprint for how the game map will look. """

    def __init__(self, width, height, boxes, start_positions, flag_position):
        """ Takes as argument the size of the map (width, height), an array with the boxes type,
        the start position of tanks (start_positions) and the position of the flag (flag_position).
        """
        self.width = width
        self.height = height
        self.boxes = boxes
        self.start_positions = start_positions
        self.flag_position = flag_position

    def rect(self):
        return pygame.Rect(0, 0, images.TILE_SIZE * self.width, images.TILE_SIZE * self.height)

    def boxAt(self, x, y):
        """ Return the type of the box at coordinates (x, y). """
        return self.boxes[y][x]


# Create the parser
parser = argparse.ArgumentParser(description="Fetch given JSON file and turn it into python code")
# Add an argument for the JSON file
parser.add_argument('--map', type=str, help='The JSON file to fetch')
parser.add_argument('--singleplayer', type=str, help='The JSON file to fetch')
parser.add_argument('--hot-multiplayer', type=str, help='The JSON file to fetch')

# Parse the arguments
args = parser.parse_args()

# Check if the --map argument is provided
if args.map:
    try:
        # Open the map file and print its contents
        with open(args.map, 'r') as file:
            json_string = file.read()
            map_string = json.loads(json_string)
            print(type(map_string))
    except FileNotFoundError:
        print(f"The file {args.map} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("No JSON file was provided.")

map0 = Map(map_string['width'], map_string['height'], map_string['boxes'], map_string['starting_positions'], map_string['flag_pos'])
