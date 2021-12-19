import math
import random

import pygame
from resize_array import resize_2d_array, resize_array


class Particle:
    def __init__(self, x=0, y=0, vx=0, vy=0, particle_type=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.type = particle_type


class ParticleTypes:
    def __init__(self, size=0):
        self.col = [
            pygame.Color(0, 0, 0, 0)
        ] * size  # Color of particles to indicate type
        self.attract = [
            [0] * size
        ] * size  # Attraction, minimum and maximum force radii between particles in 2d matrix
        self.min_r = [[0] * size] * size
        self.max_r = [[0] * size] * size

    def resize(self, size):
        self.col = resize_array(self.col, size, pygame.Color(0, 0, 0, 0))
        self.attract = resize_2d_array(self.attract, size, 0)
        self.min_r = resize_2d_array(self.min_r, size, 0)
        self.max_r = resize_2d_array(self.max_r, size, 0)

    def size(self):
        return len(self.col)

    def get_color(self, i):
        return self.col[i]

    def set_color(self, i, value):
        self.col[i] = value

    def get_attract(self, i, j):
        return self.attract[i][j]

    def set_attract(self, i, j, value):
        self.attract[i][j] = value

    def get_min_r(self, i, j):
        return self.min_r[i][j]

    def set_min_r(self, i, j, value):
        self.min_r[i][j] = value

    def get_max_r(self, i, j):
        return self.max_r[i][j]

    def set_max_r(self, i, j, value):
        self.max_r[i][j] = value
