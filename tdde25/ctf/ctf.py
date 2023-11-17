""" Main file for the game.
"""
import pygame
from pygame.locals import *
from pygame.color import *
import pymunk

# ----- Initialisation ----- #

# -- Initialise the display
pygame.init()
pygame.display.set_mode()

# -- Initialise the clock
clock = pygame.time.Clock()

# -- Initialise the physics engine
space = pymunk.Space()
space.gravity = (0.0, 0.0)
space.damping = 0.1  # Adds friction to the ground for all objects

# -- Import from the ctf framework
# The framework needs to be imported after initialisation of pygame
import ai
import images
import gameobjects
import maps

# -- Constants
FRAMERATE = 50

# -- Variables
#   Define the current level
current_map = maps.map0
#   List of all game objects
game_objects_list = []
tanks_list = []
ai_list = []

# -- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)

#-- Generate the background
background = pygame.Surface(screen.get_size())

#   Copy the grass tile all over the level area
for x in range(0, current_map.width):
    for y in range(0,  current_map.height):
        # The call to the function "blit" will copy the image
        # contained in "images.grass" into the "background"
        # image at the coordinates given as the second argument
        background.blit(images.grass,  (x*images.TILE_SIZE, y*images.TILE_SIZE))


#-- Create the boxes
for x in range(0, current_map.width):
    for y in range(0,  current_map.height):
        # Get the type of boxes
        box_type  = current_map.boxAt(x, y)
        # If the box type is not 0 (aka grass tile), create a box
        if(box_type != 0):
            # Create a "Box" using the box_type, aswell as the x,y coordinates,
            # and the pymunk space
            box = gameobjects.get_box_with_type(x, y, box_type, space)
            game_objects_list.append(box)


#-- Create the tanks
# Loop over the starting poistion
for i in range(0, len(current_map.start_positions)):
    # Get the starting position of the tank "i"
    pos = current_map.start_positions[i]
    # Create the tank, images.tanks contains the image representing the tank
    tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space)
    # Create the ai and add it to the ai list
    if i > 0:
        ai_tank = ai.Ai(tank, game_objects_list, tanks_list, space, current_map)
        ai_list.append(ai_tank)
    # Add the tank to the list of tanks
    tanks_list.append(tank)


# <INSERT CREATE FLAG>

flag = gameobjects.Flag(current_map.flag_position[0], current_map.flag_position[1])
game_objects_list.append(flag)

# Add bases

for i in range(0, len(current_map.start_positions)):
    # Get the starting position of the base "i"
    pos = current_map.start_positions[i]
    # Create the base, images.bases contains the image representing the base
    base = gameobjects.GameVisibleObject(pos[0], pos[1], images.bases[i])
    # Add the base to the list of bases
    game_objects_list.append(base)

# ----- Main Loop -----#

# -- Control whether the game run
running = True

skip_update = 0

action_map = {
    K_UP: {
        KEYDOWN: tanks_list[0].accelerate,
        KEYUP: tanks_list[0].stop_moving
    },
    K_DOWN: {
        KEYDOWN: tanks_list[0].decelerate,
         KEYUP: tanks_list[0].stop_moving
    },
    K_LEFT: {
        KEYDOWN: tanks_list[0].turn_left,
        KEYUP: tanks_list[0].stop_turning
    },
    K_RIGHT: {
        KEYDOWN: tanks_list[0].turn_right,
        KEYUP: tanks_list[0].stop_turning
    }
}

action_map2 = {
    K_w: {
        KEYDOWN: tanks_list[1].accelerate,
        KEYUP: tanks_list[1].stop_moving
    },
    K_s: {
        KEYDOWN: tanks_list[1].decelerate,
        KEYUP: tanks_list[1].stop_moving
    },
    K_a: {
        KEYDOWN: tanks_list[1].turn_left,
        KEYUP: tanks_list[1].stop_turning
    },
    K_d: {
        KEYDOWN: tanks_list[1].turn_right,
        KEYUP: tanks_list[1].stop_turning
    }
}

    # Edges for game map
edges = [
    pymunk.Segment(space.static_body, (0,0), (current_map.width, 0), (0.0)),
    pymunk.Segment(space.static_body, (0,0), (0, current_map.height), (0.0)),
    pymunk.Segment(space.static_body, (current_map.width, 0), (current_map.width, current_map.height), (0.0)),
    pymunk.Segment(space.static_body, (0, current_map.height), (current_map.width, current_map.height), (0.0))
]
space.add(*edges)

for edge in edges:
    edge.collision_type = 4

# Collistions
def collision_bullet_tank(arb, space, data):

    bullet = arb.shapes[0].parent
    tank = arb.shapes[1].parent
    
    if bullet.shooter == tank: 
        return False
    
    if bullet in game_objects_list:
        game_objects_list.remove(bullet)
        space.remove(arb.shapes[0], arb.shapes[0].body)
    if tank in tanks_list:
        # tanks_list.remove(tank)
        # space.remove(arb.shapes[1], arb.shapes[1].body)
        # tanks_list.append(tank)
        # space.add(arb.shapes[1], arb.shapes[1].body)
        tank.respawn(flag)
    
    return False

def collision_bullet_box(arb, space, data):

    bullet = arb.shapes[0].parent
    box = arb.shapes[1].parent

    if box in game_objects_list and box.destructable:
        game_objects_list.remove(box)
        space.remove(arb.shapes[1], arb.shapes[1].body)
    if bullet in game_objects_list:
        game_objects_list.remove(bullet)
        space.remove(arb.shapes[0], arb.shapes[0].body)

    return False

def collision_bullet_border(arb, space, data):
    bullet = arb.shapes[0].parent

    if bullet in game_objects_list:
        game_objects_list.remove(bullet)
        space.remove(arb.shapes[0], arb.shapes[0].body)

    return False


handler = space.add_collision_handler(1, 2)
handler.pre_solve = collision_bullet_tank
handler = space.add_collision_handler(1, 3)
handler.pre_solve = collision_bullet_box
handler = space.add_collision_handler(1, 4)
handler.pre_solve = collision_bullet_border


    # Edges for game map
edges = [
    pymunk.Segment(space.static_body, (0,0), (current_map.width, 0), (0.0)),
    pymunk.Segment(space.static_body, (0,0), (0, current_map.height), (0.0)),
    pymunk.Segment(space.static_body, (current_map.width, 0), (current_map.width, current_map.height), (0.0)),
    pymunk.Segment(space.static_body, (0, current_map.height), (current_map.width, current_map.height), (0.0))
]
space.add(*edges)

while running:
    # -- Handle the events
    for event in pygame.event.get():
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the window) or if the user press the escape key.

        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        elif event.type in [KEYDOWN, KEYUP] and event.key in action_map and event.type in action_map[event.key]:
            action_map[event.key][event.type]()
        elif event.type == KEYDOWN and event.key == K_SPACE and tank.can_shoot == True:
            tank.can_shoot = False
            game_objects_list.append(tanks_list[0].shoot(space))

        elif event.type in [KEYDOWN, KEYUP] and event.key in action_map2 and event.type in action_map2[event.key]:
            action_map2[event.key][event.type]()
        elif event.type == KEYDOWN and event.key == K_o:
            game_objects_list.append(tanks_list[1].shoot(space))
            


    # -- Update physics
    if skip_update == 0:
        # Loop over all the game objects and update their speed in function of their
        # acceleration.
        for obj in game_objects_list:
            obj.update()

        skip_update = 2
    else:
        skip_update -= 1

    for obj in tanks_list:
        obj.update()

    #   Check collisions and update the objects position

    space.step(1 / FRAMERATE)

    #   Check if tank in in range to capture the flag
    for tank in tanks_list:
        tank.try_grab_flag(flag)
        if tank.has_won():
            running = False

    #   Checks if a tank has the flag if true change the position of the flag to that tank
    for tank in tanks_list:
        tank.post_update()


    #   Update object that depends on an other object position (for instance a flag)
    for obj in game_objects_list:
        obj.post_update()

    # -- Update Display

    # Display the background on the screen
    screen.blit(background, (0, 0))


    # Update the display of the game objects on the screen
    for obj in game_objects_list:
        obj.update_screen(screen)

    # Update the display of the tanks on the screen
    for tank in tanks_list:
        tank.update_screen(screen)

    # Updating ai
    for tank_ai in ai_list:
        tank_ai.decide()

    #   Redisplay the entire screen (see double buffer technique)
    pygame.display.flip()

    #   Control the game framerate
    clock.tick(FRAMERATE)

# borders = []
# borders.append ()
# borders.append ()
# borders.append ()
# borders.append ()
# space.add.borders
