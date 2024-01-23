""" This module contains support for the different game objects: tank, boxes... """
import math
import pygame
import pymunk
import images
import copy

DEBUG = False  # Change this to set it in debug mode


def physics_to_display(x):
    """ Convert coordinates in the physic engine into the display coordinates """
    return x * images.TILE_SIZE


class GameObject:
    """ Mostly handles visual aspects (pygame) of an object.
        Subclasses need to implement two functions:
        - screen_position
        - screen_orientation """

    def __init__(self, sprite):
        self.sprite = sprite

    def update(self):
        """ Placeholder, supposed to be implemented in a subclass.
            Update the current state of the object after a tick. """
        return

    def post_update(self):
        """ Implemented in a subclass. Updates that depend on other objects. """
        return

    def update_screen(self, screen):
        """ Updates the visual part of the game. """
        sprite = self.sprite

        p = self.screen_position()
        sprite = pygame.transform.rotate(sprite, self.screen_orientation())

        offset = pymunk.Vec2d(*sprite.get_size()) / 2.
        p = p - offset
        screen.blit(sprite, p)


class GamePhysicsObject(GameObject):
    """ Extends GameObject for objects with physical interaction. """

    def __init__(self, x, y, orientation, sprite, space, movable):
        """ Initialize GamePhysicsObject with position, orientation, sprite, space, and movability. """
        super().__init__(sprite)

        half_width = 0.5 * self.sprite.get_width() / images.TILE_SIZE
        half_height = 0.5 * self.sprite.get_height() / images.TILE_SIZE

        points = [[-half_width, -half_height],
                  [-half_width, half_height],
                  [half_width, half_height],
                  [half_width, -half_height]]
        self.points = points

        if movable:
            mass = 10
            moment = pymunk.moment_for_poly(mass, points)
            self.body = pymunk.Body(mass, moment)
        else:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)

        self.body.position = x, y
        self.body.angle = math.radians(orientation)
        self.shape = pymunk.Poly(self.body, points)
        self.shape.parent = self
        self.shape.friction = 0.5
        self.shape.elasticity = 0.1

        space.add(self.body, self.shape)

    def screen_position(self):
        """ Convert body's position in physics engine to screen coordinates. """
        return physics_to_display(self.body.position)

    def screen_orientation(self):
        """ Get angle for screen orientation. """
        return -math.degrees(self.body.angle)

    def update_screen(self, screen):
        super().update_screen(screen)
        if DEBUG:
            ps = [self.body.position + p for p in self.points]
            ps = [physics_to_display(p) for p in ps]
            ps += [ps[0]]
            pygame.draw.lines(screen, pygame.color.THECOLORS["red"], False, ps, 1)


def clamp(min_max, value):
    """ Helper function to bound a value within a specific interval. """
    return min(max(-min_max, value), min_max)


class Tank(GamePhysicsObject):
    """ Tank specific functionalities. """

    ACCELERATION = 1.2
    NORMAL_MAX_SPEED = 1.5
    FLAG_MAX_SPEED = NORMAL_MAX_SPEED * 0.75
    AI_VEL_MUL = 1.3

    def __init__(self, x, y, orientation, sprite, space, ai):
        super().__init__(x, y, orientation, sprite, space, True)
        self.acceleration = 0
        self.rotation = 0
        self.shape.parent = self
        self.shape.collision_type = 2
        self.flag = None
        self.max_speed = Tank.NORMAL_MAX_SPEED
        self.start_position = pymunk.Vec2d(x, y)
        self.start_orientation = self.body.angle
        self.tick = 0
        self.can_shoot = False
        self.recoil = 0
        self.recoil_change = 0
        self.has_respawned = False
        self.score = 0
        self.direction = 0
        self.is_protected = False
        self.protection_duration = 50
        self.protection_timer = 0
        self.is_ai = ai

    def accelerate(self):
        self.acceleration = 1

    def stop_moving(self):
        self.acceleration = 0
        self.body.velocity = pymunk.Vec2d.zero()

    def decelerate(self):
        self.acceleration = -1

    def turn_left(self):
        self.rotation = -1

    def turn_right(self):
        self.rotation = 1

    def stop_turning(self):
        self.rotation = 0
        self.body.angular_velocity = 0

    def change_recoil(self):
        RECOIL = -0.8
        if self.acceleration != RECOIL:
            self.direction = copy.deepcopy(self.acceleration)

        if self.recoil == 1:
            if self.direction < 0:
                self.acceleration = RECOIL * 20 + self.acceleration
                self.max_speed = 10
            self.acceleration = RECOIL
            self.recoil_change -= 1
            if self.recoil_change < 0:
                self.recoil = -1
                self.max_speed = self.NORMAL_MAX_SPEED
        elif self.recoil == -1:
            if self.direction == 0:
                self.stop_moving()
            elif self.direction > 0:
                self.accelerate()
            else:
                self.decelerate()
            self.recoil = 0

    def update(self):
        acceleration_vector = pymunk.Vec2d(0, self.ACCELERATION * self.acceleration).rotated(self.body.angle)
        self.body.velocity += acceleration_vector

        if self.is_ai:
            velocity = clamp((self.max_speed * self.AI_VEL_MUL), self.body.velocity.length)
        else:
            velocity = clamp(self.max_speed, self.body.velocity.length)
        self.body.velocity = pymunk.Vec2d(velocity, 0).rotated(self.body.velocity.angle)

        self.body.angular_velocity += self.rotation * self.ACCELERATION
        if self.is_ai:
            self.body.angular_velocity = clamp((self.max_speed * self.AI_VEL_MUL), self.body.angular_velocity)
        else:
            self.body.angular_velocity = clamp(self.max_speed, self.body.angular_velocity)

        if self.is_protected:
            self.protection_timer -= 1
            if self.protection_timer <= 0:
                self.is_protected = False

    def post_update(self):
        if not self.can_shoot:
            self.tick += 1
        if self.tick > 30:
            self.can_shoot = True
            self.tick = 0

        if self.flag is not None:
            self.flag.x = self.body.position[0]
            self.flag.y = self.body.position[1]
            self.flag.orientation = -math.degrees(self.body.angle)
        else:
            self.max_speed = Tank.NORMAL_MAX_SPEED

    def try_grab_flag(self, flag):
        if not flag.is_on_tank:
            flag_pos = pymunk.Vec2d(flag.x, flag.y)
            if (flag_pos - self.body.position).length < 0.5:
                self.flag = flag
                flag.is_on_tank = True
                self.max_speed = Tank.FLAG_MAX_SPEED

    def has_won(self, tanks_list):
        if self.flag is not None and (self.start_position - self.body.position).length < 0.2:
            self.score += 1

            for i, tank in enumerate(tanks_list):
                print(f"Player {i + 1}: {tank.score}")
            print("-----------")
            return True
        else:
            return False

    def shoot(self, space):
        self.recoil = 1
        self.recoil_change = 3
        return Bullet(self, space)

    def respawn(self, flag):
        if flag.is_on_tank:
            self.flag = None
            flag.is_on_tank = False
            flag.respawn()
        self.body.position = self.start_position
        self.body.angle = self.start_orientation
        self.has_respawned = True
        self.is_protected = True
        self.protection_timer = self.protection_duration


class Bullet(GamePhysicsObject):
    """ Handles bullet object. """
    ACCELERATION = 1
    acceleration = 1
    max_speed = 1
    AI_BULLET_MUL = 1.5

    def __init__(self, tank: Tank, space):
        super().__init__(tank.body.position[0], tank.body.position[1], math.degrees(tank.body.angle), images.bullet, space, True)
        self.angle = tank.body.angle
        self.shooter = tank
        self.parrent_is_ai = tank.is_ai
        self.shape.collision_type = 1

    def update(self):
        if self.parrent_is_ai:
            self.body.velocity = (pymunk.Vec2d(5 * self.AI_BULLET_MUL, 0).rotated(self.angle + math.radians(90)))
        else:
            self.body.velocity = (pymunk.Vec2d(5, 0).rotated(self.angle + math.radians(90)))


class Box(GamePhysicsObject):
    """ This class extends the GamePhysicsObject to handle box objects. """

    def __init__(self, x, y, sprite, movable, space, destructable):
        """ It takes as arguments the coordinate of the starting position of the box (x,y) and the box model (boxmodel). """
        super().__init__(x, y, 0, sprite, space, movable)
        self.destructable = destructable
        self.shape.collision_type = 3
        self.movable = movable


def get_box_with_type(x, y, type, space):
    """ Create a box with the correct type at coordinate x, y.
        - type == 1 create a rock box
        - type == 2 create a wood box
        - type == 3 create a metal box
        Other values of type are invalid
    """
    (x, y) = (x + 0.5, y + 0.5)  # Offsets the coordinate to the center of the tile
    if type == 1:  # Creates a non-movable non-destructable rockbox
        return Box(x, y, images.rockbox, False, space, False)
    if type == 2:  # Creates a movable destructable woodbox
        return Box(x, y, images.woodbox, True, space, True)
    if type == 3:  # Creates a , (self.width,movable non-destructable metalbox
        return Box(x, y, images.metalbox, True, space, False)


class GameVisibleObject(GameObject):
    """ This class extends GameObject for object that are visible on screen but have no physical representation (bases and flag) """

    def __init__(self, x, y, sprite):
        """ It takes argument the coordinates (x,y) and the sprite. """
        self.x = x
        self.y = y
        self.orientation = 0
        super().__init__(sprite)

    def screen_position(self):
        """ Overwrite from GameObject """
        return physics_to_display(pymunk.Vec2d(self.x, self.y))

    def screen_orientation(self):
        """ Overwrite from GameObject """
        return self.orientation


class Explosion(GameVisibleObject):
    def __init__(self, x, y):
        super().__init__(x, y, images.explosion)
        self.tick = 0
        self.disappear = False

    def post_update(self):
        if self.tick > 10:
            self.tick = 0
            self.disappear = True
        else:
            self.tick += 1


class Flag(GameVisibleObject):
    """ This class extends GameVisibleObject for representing flags."""

    def __init__(self, x, y):
        self.is_on_tank = False
        self.start_position = pymunk.Vec2d(x, y)
        super().__init__(x, y, images.flag)

    def respawn(self):
        self.x = self.start_position[0]
        self.y = self.start_position[1]
        self.orientation = 0
