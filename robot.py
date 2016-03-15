from math import cos, sin, sqrt, pi
from constants import *
from line import Line

# ROBOT #


class Robot:
    def __init__(self, game, surface, position, visor_angle):
        self.game = game
        self.surface = surface
        self.position = position
        self.visor_angle = visor_angle
        self.angle = 0
        self.tail_long = sqrt(DISPLAY_RES[0] ** 2 + DISPLAY_RES[1] ** 2) / 2
        self.tail = [0, 0]

    def update(self, da):
        self.visor_angle += da
        self.tail[0] = self.position[0] + self.tail_long * cos(self.visor_angle)
        self.tail[1] = self.position[1] + self.tail_long * sin(self.visor_angle)

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def get_distance(self, figures):
        def how_far(p1, p2):
            return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

        vision_line = Line(self.position, self.tail)

        min_dist = 10000
        min_point = []
        find_intersect_point = False
        storage = []
        for figure in figures:
            vertices_count = len(figure.vertices)
            for i in range(vertices_count):
                line_segment = Line(figure.vertices[i], figure.vertices[(i + 1) % vertices_count])

                intersect_point = vision_line.intersect(line_segment)

                if intersect_point:
                    find_intersect_point = True
                    dist = how_far(self.position, intersect_point) # BAD

                    if dist < min_dist:
                        min_dist = dist
                        min_point = intersect_point
                    else:
                        storage.append(intersect_point)

        if find_intersect_point:
            return min_point

        return False

    def draw_vision(self, surface, figures):
        x, y = self.position
        self.game.draw.circle(surface, black, (int(x), int(y)), 10, 1)
        intersect_point = self.get_distance(figures)
        if intersect_point:
            self.game.draw.line(self.surface, red, self.position, intersect_point, 1)
        else:
            self.game.draw.line(surface, green, self.position, self.tail, 1)