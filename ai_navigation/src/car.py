"""Car physics and control module with realistic drift mechanics.

This module implements a 2D racing car with physics simulation including:
- Acceleration and velocity with air resistance
- Drift mechanics with angular momentum
- Vision sensors for environment detection
- Collision detection with track boundaries
- Fitness checkpoint crossing detection
"""

import math
from enum import Enum

import pygame

from ai_navigation.src.constants import (
    ACCELERATION_RATE,
    ANGLE_RESET_THRESHOLD,
    CAR_IMG,
    DEFAULT_SIGHT_DISTANCE,
    DRIFT_DECAY,
    DRIFT_INFLUENCE,
    DRIFT_LERP_SPEED,
    IMG,
    MAX_DRIFT_ANGLE,
    MAX_SPEED,
    MAX_SPEED_THRESHOLD,
    MIN_SPEED_THRESHOLD,
    SPEED_DECAY,
    VELOCITY_AIR_RESISTANCE,
    VELOCITY_DECAY,
)


def scalar(vect1, vect2):
    """Calculate 2D cross product (scalar) of two vectors.

    Args:
        vect1 (tuple): First vector (x, y)
        vect2 (tuple): Second vector (x, y)

    Returns:
        float: Cross product magnitude

    """
    return (vect1[0] * vect2[1]) - (vect1[1] * vect2[0])


def sub(p1, p2):
    """Subtract two 2D points/vectors.

    Args:
        p1 (tuple): First point (x, y)
        p2 (tuple): Second point (x, y)

    Returns:
        tuple: Resulting vector (x, y)

    """
    return (p1[0] - p2[0], p1[1] - p2[1])


def div(p1, p2):
    """Element-wise division of two 2D vectors with zero handling.

    Args:
        p1 (tuple): Numerator vector (x, y)
        p2 (tuple): Denominator vector (x, y)

    Returns:
        tuple: Result of element-wise division, 0 where denominator is 0

    """
    if p2[0] == 0 and p2[1] == 0:
        return (0, 0)
    if p2[0] == 0:
        return (0, p1[1] / p2[1])
    if p2[1] == 0:
        return (p1[0] / p2[0], 0)
    return (p1[0] / p2[0], p1[1] / p2[1])


def mult(p1, p2):
    """Element-wise multiplication of two 2D vectors.

    Args:
        p1 (tuple): First vector (x, y)
        p2 (tuple): Second vector (x, y)

    Returns:
        tuple: Element-wise product (x1*x2, y1*y2)

    """
    return (p1[0] * p2[0], p1[1] * p2[1])


def add(p1, p2):
    """Add two 2D points/vectors.

    Args:
        p1 (tuple): First point (x, y)
        p2 (tuple): Second point (x, y)

    Returns:
        tuple: Sum vector (x1+x2, y1+y2)

    """
    return (p1[0] + p2[0], p1[1] + p2[1])


def norm(x):
    """Calculate Euclidean length/magnitude of a 2D vector.

    Args:
        x (tuple): Vector (x, y)

    Returns:
        float: Length of the vector

    """
    return math.sqrt(x[0] ** 2 + x[1] ** 2)


def normalize(x, scale):
    """Normalize a 2D vector and scale to specified length.

    Args:
        x (tuple): Vector to normalize (x, y)
        scale (float): Desired length of output vector

    Returns:
        tuple: Normalized and scaled vector, (0, 0) if input is zero vector

    """
    n = norm(x)
    if n == 0:
        return (0, 0)
    return (x[0] / n * scale, x[1] / n * scale)


def lerp(a, b, p):
    """Linear interpolation between two values.

    Args:
        a (float): Start value
        b (float): End value
        p (float): Interpolation parameter (0.0 to 1.0)

    Returns:
        float: Interpolated value

    """
    return a + p * (b - a)


RotatingState = Enum("RotatingState", "calm left right")
"""Enum representing the car's current steering state.

Values:
    calm: No rotation input
    left: Turning left
    right: Turning right
"""


class Car:
    """2D racing car with realistic physics and drift mechanics.

    Implements a car with:
    - Position and velocity-based movement
    - Drift angle for realistic turning behavior
    - 8-directional vision sensors for environment detection
    - Collision detection with polygonal boundaries
    - Fitness checkpoint crossing detection

    The car uses a velocity-based physics system with air resistance,
    and drift mechanics that allow for realistic racing behavior.

    Attributes:
        speed (float): Current forward/backward speed
        acc (int): Acceleration input (-1, 0, or 1)
        drift_angle (float): Current drift/turning angle
        angle (float): Car's facing direction in degrees
        x_vel (float): Velocity in x direction
        y_vel (float): Velocity in y direction
        rotating_state (RotatingState): Current steering state

    """

    def __init__(self, x, y, angle) -> None:
        """Initialize a car at specified position and angle.

        Args:
            x (float): Initial x coordinate
            y (float): Initial y coordinate
            angle (float): Initial facing angle in degrees

        """
        self._width = CAR_IMG.get_size()[0] / 2
        self._height = CAR_IMG.get_size()[1] / 2
        self._x = int(x) - self._width / 2
        self._y = int(y) - self._height / 2
        self.speed = 0
        self.acc = 0
        self.drift_angle = 0
        self.__angle = angle
        self._crashed = False
        self.rotating_state = RotatingState.calm

        diag_radius = math.atan(self._height / self._width)  # in radians
        self._diag_sin = math.sin(diag_radius)
        self._diag_cos = math.cos(diag_radius)

        self.diagonal = norm((self._width, self._height))

        self._sight = DEFAULT_SIGHT_DISTANCE
        self._center = None
        self._fit_distance = self._height
        self._fitness_point = None

        self.x_vel = 0
        self.y_vel = 0

    @property
    def sight(self):
        """Get vision sensor range distance.

        Returns:
            float: Maximum distance for vision sensors

        """
        return self._sight

    @property
    def center(self):
        """Get current center position of the car.

        Returns:
            tuple or None: (x, y) center coordinates, or None if not yet calculated

        """
        return self._center

    @property
    def angle(self):
        """Get car's current facing angle.

        Returns:
            float: Angle in degrees

        """
        return self.__angle

    @angle.setter
    def angle(self, angl) -> None:
        """Set car's facing angle with automatic wrapping.

        Args:
            angl (float): New angle in degrees

        Note:
            Automatically resets to 0 if angle exceeds threshold to prevent overflow.

        """
        self.__angle = angl
        if abs(self.__angle) >= ANGLE_RESET_THRESHOLD:
            self.__angle = 0

    def draw_shadow(self, win, color) -> None:
        """Draw the car with a colored overlay (shadow effect).

        Renders the car sprite rotated to current angle with a color tint applied.
        Useful for highlighting specific cars (e.g., best performer, user car).

        Args:
            win (pygame.Surface): Surface to draw on
            color (tuple): RGB color (r, g, b) to tint the car

        """
        # rotate the img
        rotated_image = pygame.transform.rotate(IMG, -self.__angle)
        # create img frame
        new_rect = rotated_image.get_rect(
            center=IMG.get_rect(topleft=(self._x, self._y)).center,
        )
        # shadow the image
        r, g, b = color

        w, h = rotated_image.get_size()
        for x in range(w):
            for y in range(h):
                a = rotated_image.get_at((x, y))[3]
                rotated_image.set_at((x, y), pygame.Color(r, g, b, a))

        win.blit(rotated_image, new_rect.topleft)

    def draw(self, win) -> None:
        """Draw the car sprite at current position and angle.

        Args:
            win (pygame.Surface): Surface to draw on

        """
        # rotate the img
        rotated_image = pygame.transform.rotate(IMG, -self.__angle)
        new_rect = rotated_image.get_rect(
            center=IMG.get_rect(topleft=(self._x, self._y)).center,
        )
        win.blit(rotated_image, new_rect.topleft)

    def move(self) -> None:
        """Update car position based on physics simulation.

        Applies:
        - Acceleration to speed based on acc input
        - Velocity changes based on speed and angle
        - Drift angle influence on car rotation
        - Position updates from velocity
        - Air resistance and decay to velocity and speed
        - Drift decay over time

        The car's movement combines direct acceleration in the facing direction
        with drift mechanics that allow the car to slide sideways while turning.
        """
        if abs(self.acc) == 1:
            if abs(self.speed) < MAX_SPEED_THRESHOLD:
                self.speed += (
                    self.acc * -ACCELERATION_RATE
                )  # i say minus because i wanna flip direction
            if abs(self.speed) < MIN_SPEED_THRESHOLD:
                self.speed = 0
                return
        self.x_vel += (
            math.cos(math.radians(self.angle + 90)) * MAX_SPEED * -self.acc * 2
        )
        self.y_vel += (
            math.sin(math.radians(self.angle + 90)) * MAX_SPEED * -self.acc * 2
        )  # acc => dopredu|dozadu

        if self.drift_angle == 0 or self.drift_angle > 0:
            pass
        else:
            pass
        self.angle += (
            self.drift_angle * self.speed * -0.1 * DRIFT_INFLUENCE
        )  # * self.speed * -0.1 * 2.5 * dir

        self._x += self.x_vel * VELOCITY_DECAY
        self._y += self.y_vel * VELOCITY_DECAY
        self.drift_angle *= DRIFT_DECAY  ######
        self.x_vel *= VELOCITY_AIR_RESISTANCE
        self.y_vel *= VELOCITY_AIR_RESISTANCE
        self.speed *= SPEED_DECAY

    def rotate_by(self, angl) -> None:
        """Apply steering input to adjust drift angle.

        Interpolates the drift angle toward the target based on input direction.
        Positive angle rotates right, negative rotates left, zero straightens out.

        Args:
            angl (float): Steering input (typically -5, 0, or 5)

        """
        if abs(self.drift_angle) < MAX_DRIFT_ANGLE - angl / 5:
            pass
            # self.drift_angle += angl/5

        if angl > 1:
            self.drift_angle = lerp(self.drift_angle, MAX_DRIFT_ANGLE, DRIFT_LERP_SPEED)
        elif angl < -1:
            self.drift_angle = lerp(
                self.drift_angle,
                -MAX_DRIFT_ANGLE,
                DRIFT_LERP_SPEED,
            )
        elif angl == 0:
            self.drift_angle = lerp(self.drift_angle, 0, DRIFT_LERP_SPEED)
            # self.drift_angle = 0

    def get_vision(self, road) -> list:
        """Calculate vision sensor intersection points with track boundaries.

        Casts 8 rays from the car's center in different directions:
        - Front, back, left, right (cardinal directions)
        - Front-right, front-left, back-right, back-left (45° angles)

        Each ray extends to sight distance and finds the nearest intersection
        with track boundaries.

        Args:
            road (list): Track boundary polygon data

        Returns:
            list: 8 intersection points (x, y) where vision rays hit track edges

        """
        sin = math.sin(math.radians(self.angle))
        cos = math.cos(math.radians(self.angle))
        self._center = (
            self._x + self._diag_cos * self.diagonal,
            self._y + self._diag_sin * self.diagonal,
        )
        center = self._center

        sin_front = math.sin(math.radians(self.angle - 90))
        cos_front = math.cos(math.radians(self.angle - 90))
        sin_mid_right = math.sin(math.radians(self.angle - 45))
        cos_mid_right = math.cos(math.radians(self.angle - 45))
        sin_mid_left = math.sin(math.radians(self.angle + 45))
        cos_mid_left = math.cos(math.radians(self.angle + 45))
        sin_mid_mid_right = math.sin(math.radians(self.angle - 67.5))
        cos_mid_mid_right = math.cos(math.radians(self.angle - 67.5))
        sin_mid_mid_left = math.sin(math.radians(self.angle + 67.5))
        cos_mid_mid_left = math.cos(math.radians(self.angle + 67.5))

        front_point = (
            center[0] + self._sight * cos_front,
            center[1] + self._sight * sin_front,
        )
        back_point = (
            center[0] - self._sight * cos_front,
            center[1] - self._sight * sin_front,
        )
        right_point = (center[0] + self._sight * cos, center[1] + self._sight * sin)
        left_point = (center[0] - self._sight * cos, center[1] - self._sight * sin)
        mid_right_point = (
            center[0] + self._sight * cos_mid_right,
            center[1] + self._sight * sin_mid_right,
        )
        mid_left_point = (
            center[0] - self._sight * cos_mid_left,
            center[1] - self._sight * sin_mid_left,
        )
        mid_mid_right_point = (
            center[0] + self._sight * cos_mid_mid_right,
            center[1] + self._sight * sin_mid_mid_right,
        )
        mid_mid_left_point = (
            center[0] - self._sight * cos_mid_mid_left,
            center[1] - self._sight * sin_mid_mid_left,
        )

        vision = [
            front_point,
            right_point,
            back_point,
            left_point,
            mid_right_point,
            mid_left_point,
            mid_mid_right_point,
            mid_mid_left_point,
        ]

        for points in road:  # 2 sets of points...inner,outter
            for i in range(len(points)):
                for x, v in enumerate(vision):
                    intersect_point = self._cross(points[i - 1], points[i], center, v)
                    if intersect_point:
                        vision[x] = intersect_point

        return vision

    def vision_distance(self, road):
        """Get distances to track boundaries in all vision directions.

        Args:
            road (list): Track boundary polygon data

        Returns:
            list: 8 distances (in pixels) to nearest obstacles in each direction

        """
        vision = self.get_vision(road)
        sin_front = math.sin(math.radians(self.angle - 90))
        cos_front = math.cos(math.radians(self.angle - 90))

        # get point that is middle in the front of the car
        self._fitness_point = (
            self._center[0] + self._fit_distance * cos_front,
            self._center[1] + self._fit_distance * sin_front,
        )

        distances = []
        for p in vision:
            vect = sub(self._center, p)
            d = norm(vect)
            distances.append(round(d))
        return distances

    def getVertices(self):
        """Calculate current collision box vertices of the car.

        Computes the four corners of the car's rectangular collision box,
        rotated according to the car's current angle.

        Returns:
            tuple: Four vertices (top_left, top_right, bottom_right, bottom_left)
                  as (x, y) coordinate tuples

        """
        center = (
            self._x + self._diag_cos * self.diagonal,
            self._y + self._diag_sin * self.diagonal,
        )

        vect = sub(center, (self._x, self._y))  # vector from top left to center

        vect_tl = sub(
            (self._x, self._y),
            center,
        )  # vect from center to Top Left not rotated
        vect_tr = (vect[0], -vect[1])
        vect_bl = (-vect[0], vect[1])
        vect_br = vect

        # current COS & SIN
        s = math.sin(math.radians(self.__angle))
        c = math.cos(math.radians(self.__angle))

        # rotate vector
        new_tl = (vect_tl[0] * c - vect_tl[1] * s, vect_tl[0] * s + vect_tl[1] * c)
        new_tr = (vect_tr[0] * c - vect_tr[1] * s, vect_tr[0] * s + vect_tr[1] * c)
        new_bl = (vect_bl[0] * c - vect_bl[1] * s, vect_bl[0] * s + vect_bl[1] * c)
        new_br = (vect_br[0] * c - vect_br[1] * s, vect_br[0] * s + vect_br[1] * c)

        # add the vector to center
        top_left = add(new_tl, center)
        top_right = add(new_tr, center)
        bottom_left = add(new_bl, center)
        bottom_right = add(new_br, center)

        return (top_left, top_right, bottom_right, bottom_left)

    def collide_fitness(self, a1, a2):
        """Check if car crosses a fitness checkpoint line.

        Uses a point slightly ahead of the car's center to detect checkpoint crossings.

        Args:
            a1 (tuple): First endpoint of fitness line (x, y)
            a2 (tuple): Second endpoint of fitness line (x, y)

        Returns:
            tuple or False: Intersection point (x, y) if crossing, False otherwise

        """
        return self._cross(a1, a2, self._center, self._fitness_point)

    def _cross(self, a1, a2, b1, b2):
        """Calculate line segment intersection using parametric equations.

        Determines if two line segments intersect and returns the intersection point.
        Uses the cross product method to solve for intersection parameters.

        Args:
            a1 (tuple): First endpoint of line A (x, y)
            a2 (tuple): Second endpoint of line A (x, y)
            b1 (tuple): First endpoint of line B (x, y)
            b2 (tuple): Second endpoint of line B (x, y)

        Returns:
            tuple or False: Intersection point (x, y) if segments intersect,
                          False if they don't intersect or are parallel

        """
        # vectA = a2 - a1
        r = a2[0] - a1[0], a2[1] - a1[1]
        s = b2[0] - b1[0], b2[1] - b1[1]

        """
        a2 = a1 + r
        a1 + t*r = b1 + u*s ... / scalar s
        (a1 x s) + t*(r x s) = (b1 x s) + u*(s x s) ... # s x s = 0
        (a1 x s) + t*(r x s) = (b1 x s) ... / (a1 x s)
        t*(r x s) = ((b1 - a1) x s) ... / (r x s)
        t = ((b1 - a1) x s) / (r x s)
        """
        t = u = None
        if scalar(r, s) != 0:
            t = scalar(sub(b1, a1), s) / scalar(r, s)
        if scalar(s, r) != 0:
            u = scalar(sub(a1, b1), r) / scalar(s, r)

        if t is not None and 0 <= t <= 1 and u is not None and 0 <= u <= 1:
            x = a1[0] + r[0] * t
            y = a1[1] + r[1] * t
            return (x, y)
        return False

    def collides(self, road, experimental_collision_physics=False) -> bool:
        """Check if car collides with track boundaries.

        Tests each edge of the car's collision box against all track boundary
        segments to detect collisions.

        Args:
            road (list): Track boundary polygon data (inner and outer boundaries)
            experimental_collision_physics (bool): If True, applies bounce-back
                physics on collision (default: False)

        Returns:
            bool: True if car collides with track, False otherwise

        """
        vertices = self.getVertices()
        for points in road:
            for i in range(len(points)):
                for k in range(len(vertices)):
                    if self._cross(
                        points[i - 1],
                        points[i],
                        vertices[k - 1],
                        vertices[k],
                    ):
                        if experimental_collision_physics:
                            self.speed /= -0.8
                            self.x_vel /= -0.93
                            self.y_vel /= -0.93
                            self._x += self.x_vel
                            self._y += self.y_vel
                        return True
        return False
