""" This file contains function and classes for the Artificial Intelligence used in the game.
"""
import maps
import math
import random
from collections import defaultdict, deque

import pymunk
from pymunk import Vec2d
import gameobjects

current_map = maps.map0

# NOTE: use only 'map0' during development!

MIN_ANGLE_DIF = math.radians(8)   # 3 degrees, a bit more than we can turn each tick


def angle_between_vectors(vec1, vec2):
    """ Since Vec2d operates in a cartesian coordinate space we have to
        convert the resulting vector to get the correct angle for our space.
    """
    vec = vec1 - vec2
    vec = vec.perpendicular()
    return vec.angle


def periodic_difference_of_angles(angle1, angle2):
    """ Compute the difference between two angles.
    """
    angle1 = ((angle1 + math.pi) % (2 * math.pi)) - math.pi
    angle2 = ((angle2 + math.pi) % (2 * math.pi)) - math.pi

    diff = angle2 - angle1

    if diff > math.pi:
        diff -= 2 * math.pi
    elif diff < -math.pi:
        diff += 2 * math.pi

    return diff


def periodic_difference_of_angles1(angle1, angle2):
    """ Compute the difference between two angles.
    """
    return (angle1 % (2 * math.pi)) - (angle2 % (2 * math.pi))


class Ai:
    """ A simple ai that finds the shortest path to the target using
    a breadth first search. Also capable of shooting other tanks and or wooden
    boxes. """

    def __init__(self, tank, game_objects_list, tanks_list, space, currentmap):
        self.tank = tank
        self.game_objects_list = game_objects_list
        self.tanks_list = tanks_list
        self.space = space
        self.currentmap = currentmap
        self.flag = None
        self.max_x = currentmap.width - 1
        self.max_y = currentmap.height - 1

        self.path = deque()
        self.move_cycle = self.move_cycle_gen()
        self.update_grid_pos()
        self.next_coord = None
        self.prev_coord = 10

    def update_grid_pos(self):
        """ This should only be called in the beginning, or at the end of a move_cycle. """
        self.grid_pos = self.get_tile_of_position(self.tank.body.position)

    def decide(self):
        """ Main decision function that gets called on every tick of the game.
        """
        next(self.move_cycle)
        self.maybe_shoot()

    def maybe_shoot(self):
        """ Makes a raycast query in front of the tank. If another tank
            or a wooden box is found, then we shoot.
        """
        distance = 0.2
        mid = self.tank.body.position
        angle = self.tank.body.angle + math.pi / 2

        start_y = mid[1] + distance + math.sin(angle)
        start_x = mid[0] + distance + math.cos(angle)
        end_y = mid[1] + 9 * math.sin(angle)
        end_x = mid[0] + 9 * math.cos(angle)

        start = (start_x, start_y)
        end = (end_x, end_y)

        ray = self.space.segment_query_first(start, end, 0, pymunk.ShapeFilter())
        if not ray:
            return
        res = ray.shape
        if isinstance(res, pymunk.Segment):
            return
        if isinstance(res.parent, gameobjects.Tank) and self.tank.can_shoot is True:
            self.tank.can_shoot = False
            self.game_objects_list.append(self.tank.shoot(self.space))
        if isinstance(res.parent, gameobjects.Box):
            if res.parent.destructable and self.tank.can_shoot is True:
                self.tank.can_shoot = False
                self.game_objects_list.append(self.tank.shoot(self.space))

        pass  # To be implemented

    def move_cycle_gen(self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """

        while True:
            shortest_path = self.find_shortest_path()
            if not shortest_path:
                yield
                continue
            # if self.grid_pos == self.get_tile_of_position(self.tank.start_position):
            #     shortest_path.popleft()
            next_coord = shortest_path.popleft()

            yield
            if self.tank.has_respawned is True:
                self.update_grid_pos()
                self.tank.stop_moving()
                shortest_path = self.find_shortest_path()
                if not shortest_path:
                    next_coord = self.tank.body.position
                else:
                    next_coord = shortest_path.popleft()
                    self.tank.has_respawned = False
            self.turn(next_coord)
            while not self.correct_angle(next_coord):
                yield
            self.accelerate()
            while not self.correct_pos(next_coord) and self.tank.has_respawned is False:
                yield

    def find_shortest_path(self):
        """ A simple Breadth First Search using integer coordinates as our nodes.
            Edges are calculated as we go, using an external function.
        """
        queue = deque()
        visited = set()
        paths = defaultdict()

        # insert our source node into the queue
        queue.appendleft(self.grid_pos)
        visited.add(self.grid_pos)
        # while queue is not empty:
        while len(queue) >= 1:
            tile_neighbors = self.get_tile_neighbors(queue[0])
            if queue[0] == self.get_target_tile():
                # paths[queue[0]] = queue[0]
                break
            for i in tile_neighbors:
                if i not in visited:
                    queue.append(i)
                    visited.add(i)
                    paths[i] = queue[0]
            queue.popleft()

        shortest_path = []
        default = self.get_target_tile()
        shortest_path.append(default)
        while True:
            if not paths:
                break
            if default not in paths:
                break
            add = paths[default]
            shortest_path.append(add)
            default = add
            if add == self.grid_pos:
                break
        shortest_path.pop()
        shortest_path.reverse()

        new_shortest_path = [tuple(value + 0.5 for value in tup) for tup in shortest_path]
        self.path = deque(new_shortest_path)
        return deque(new_shortest_path)

    def get_target_tile(self):
        """ Returns position of the flag if we don't have it. If we do have the flag,
            return the position of our home base.
        """
        if self.tank.flag is not None:
            x, y = self.tank.start_position
        else:
            self.get_flag()  # Ensure that we have initialized it.
            x, y = self.flag.x, self.flag.y
        return Vec2d(int(x), int(y))

    def get_flag(self):
        """ This has to be called to get the flag, since we don't know
            where it is when the Ai object is initialized.
        """
        if self.flag is None:
            # Find the flag in the game objects list
            for obj in self.game_objects_list:
                if isinstance(obj, gameobjects.Flag):
                    self.flag = obj
                    break
        return self.flag

    def get_tile_of_position(self, position_vector):
        """ Converts and returns the float position of our tank to an integer position. """
        x, y = position_vector
        return Vec2d(int(x), int(y))

    def get_tile_neighbors(self, coord_vec):
        """ Returns all bordering grid squares of the input coordinate.
            A bordering square is only considered accessible if it is grass
            or a wooden box.
        """
        x_coords = coord_vec[0]
        y_coords = coord_vec[1]

        neighbors = [(x_coords + 1, y_coords), (x_coords - 1, y_coords), (x_coords, y_coords + 1), (x_coords, y_coords - 1)]  # Find the coordinates of the tiles' four neighbors

        result = filter(self.filter_tile_neighbors, neighbors)  # This is your filter object
        result_list = list(result)  # Convert filter object to a list

        return result_list

    def filter_tile_neighbors(self, coord):
        """ Used to filter the tile to check if it is a neighbor of the tank.
        """
        x_coords = coord[0]
        y_coords = coord[1]
        if x_coords < current_map.width and x_coords >= 0 and y_coords < current_map.height and y_coords >= 0:
            if self.currentmap.boxes[y_coords][x_coords] == 1:
                return False
            else:
                return True

    def turn(self, next_coord):
        desired_angle = angle_between_vectors(self.tank.body.position, next_coord)
        angle_diff = periodic_difference_of_angles(self.tank.body.angle, desired_angle)

        if angle_diff < MIN_ANGLE_DIF and angle_diff >= 0 or angle_diff > MIN_ANGLE_DIF and angle_diff <= 0:
            return True
        else:
            if angle_diff > 0:
                self.tank.turn_right()
            else:
                self.tank.turn_left()
        return False

    def correct_pos(self, next_coord):
        desired_pos = next_coord
        current_pos = self.tank.body.position

        if (desired_pos - current_pos).length > self.prev_coord:
            self.update_grid_pos()
            self.tank.stop_moving()
            self.prev_coord = 10
            return True
        else:
            self.prev_coord = (desired_pos - current_pos).length
            return False

    def correct_angle(self, next_coord):
        desired_angle = angle_between_vectors(self.tank.body.position, next_coord)
        angle_diff = periodic_difference_of_angles(self.tank.body.angle, desired_angle)

        if angle_diff < MIN_ANGLE_DIF and angle_diff >= 0 or angle_diff > MIN_ANGLE_DIF and angle_diff <= 0:
            self.tank.stop_turning()
            return True
        elif -angle_diff < MIN_ANGLE_DIF and -angle_diff >= 0 or -angle_diff > MIN_ANGLE_DIF and -angle_diff <= 0:
            self.tank.stop_turning()
            return True
        else:
            return False

    def accelerate(self):
        self.tank.accelerate()
        return
