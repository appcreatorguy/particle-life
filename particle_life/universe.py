"""Universe Class"""

import math
import random

import pygame
from hsv import *
from numpy.random import default_rng
from resize_array import *
from particles import *

RADIUS = 5.0
DIAMETER = 2.0
R_SMOOTH = 2.0


class Universe:
    def __init__(self, numTypes, numParticles, width, height):
        self.types = ParticleTypes()
        self.particles = []
        for i in range(numParticles):
            self.particles.append(Particle())

        self.set_size(width, height)
        self.set_population(numTypes, numParticles)
        
        self.centerX = self.width * 0.5
        self.centerY = self.height * 0.5
        self.zoom = 1
        self.attractMean = 0
        self.attractStd = 0
        self.min_r_lower = 0
        self.min_r_upper = 0
        self.max_r_lower = 0
        self.max_r_upper = 0
        self.friction = 0
        self.flat_force = False
        self.wrap = True

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_population(self, numTypes, numParticles):
        self.types.resize(numTypes)
        self.particles = make_particles(self.particles, numParticles,)

    def re_seed(
        self,
        attractMean,
        attractStd,
        min_r_lower,
        min_r_upper,
        max_r_lower,
        max_r_upper,
        friction,
        flat_force,
    ):
        self.attractMean = attractMean
        self.attractStd = attractStd
        self.min_r_lower = min_r_lower
        self.min_r_upper = min_r_upper
        self.max_r_lower = max_r_lower
        self.max_r_upper = max_r_upper
        self.friction = friction
        self.flat_force = flat_force
        self.set_random_types()
        self.set_random_particles()

    def set_random_types(self):
        rng = default_rng()
        rand_attr = lambda: rng.normal(self.attractMean, self.attractStd)
        rand_min_r = lambda: rng.uniform(self.min_r_lower, self.min_r_upper)
        rand_max_r = lambda: rng.uniform(self.max_r_lower, self.max_r_upper)

        for i in range(self.types.size()):
            self.types.set_color(
                i,
                from_HSV(
                    float(i) / self.types.size(), float(1.0), float(i % 2) * 0.5 + 0.5
                ),
            )
            for j in range(self.types.size()):
                if i == j:
                    self.types.set_attract(
                        i, j, -abs(rand_attr())
                    )  # Same particles should always be attracted to each other
                    self.types.set_min_r(i, j, DIAMETER)
                else:
                    self.types.set_attract(i, j, rand_attr())
                    self.types.set_min_r(
                        i, j, max(rand_min_r(), DIAMETER)
                    )  # Keep min radius above diameter
                self.types.set_max_r(
                    i, j, max(rand_max_r(), self.types.get_min_r(i, j))
                )  # Keep max radius above min

                # Keep radii symmetric
                self.types.set_max_r(j, i, self.types.get_max_r(i, j))
                self.types.set_min_r(j, i, self.types.get_min_r(i, j))

    def set_random_particles(self):
        rng = default_rng()
        rand_type = lambda: rng.uniform(0, (self.types.size() - 1))
        rand_uni = lambda: rng.uniform(0.0, 1.0)
        rand_norm = lambda: rng.normal(0.0, 1.0)

        for i in range(len(self.particles)):
            p = self.particles[i]
            p.type = round(rand_type())
            p.x = (rand_uni() * 0.5 + 0.25) * self.height
            p.y = (rand_uni() * 0.5 + 0.25) * self.width
            p.vx = rand_norm() * 0.2
            p.vy = rand_norm() * 0.2

    def step(self):
        # print("Stepping")
        for i in range(len(self.particles)):
            # Current Particle
            p = self.particles[i]

            # Interactions
            for j in range(len(self.particles)):
                # Other Particle
                q = self.particles[j]

                # Get deltas
                dx = q.x - p.x
                dy = q.y - p.y
                if self.wrap:
                    if dx > self.width * 0.5:
                        dx -= self.width
                    elif dx < -self.width*0.5:
                        dx += self.width
                    if dy > self.height * 0.5:
                        dy -= self.height
                    elif dy < -self.height * 0.5:
                        dy += self.height

                # Get distance using pythag
                r2 = dx * dx + dy * dy
                min_r = self.types.get_min_r(p.type, q.type)
                max_r = self.types.get_max_r(p.type, q.type)

                if r2 > max_r * max_r or r2 < 0.01:# or math.sqrt(r2) <= DIAMETER:
                    # check for distance cutoff
                    continue

                # Normalise displacement
                r = math.sqrt(r2)
                dx /= r
                dy /= r

                # calculate force
                f = 0.0
                if r > min_r:
                    if self.flat_force:
                        f = self.types.get_attract(p.type, q.type)
                    else:
                        numer = 2.0 * abs(r - 0.5 * (max_r + min_r))
                        denom = max_r - min_r
                        f = self.types.get_attract(p.type, q.type) * (1.0 - numer / denom)
                else:
                    f = R_SMOOTH*min_r*(1.0/(min_r+R_SMOOTH)-1.0/(r+R_SMOOTH))

                p.vx += f * dx
                p.vy += f * dy
            self.particles[i] = p

        # Update Position
        for i in range(len(self.particles)):
            # Current Particle
            p = self.particles[i]

            # Update Position and velocity
            p.x += p.vx
            p.y += p.vy
            p.vx *= 1.0 - self.friction
            p.vy *= 1.0 - self.friction

            # Check for wall
            if self.wrap:
                if p.x < 0:
                    p.x += self.width
                elif p.x >= self.width:
                    p.x -= self.width

                if p.y < 0:
                    p.y + self.height
                elif p.y >= self.height:
                    p.y -= self.height

            else:
                if p.x < DIAMETER:
                    p.vx = -p.vx
                    p.x = DIAMETER
                elif p.x >= self.width - DIAMETER:
                    p.vx = -p.vx
                    p.x = self.width - DIAMETER

                if p.y < DIAMETER:
                    p.vy = -p.vy
                    p.y = DIAMETER
                elif p.y >= self.height - DIAMETER:
                    p.vy = -p.vy
                    p.y = self.height - DIAMETER

            self.particles[i] = p

    def draw(self, ctx, opacity):
        circleRadius = RADIUS * self.zoom
        for i in range(len(self.particles)):
            p = self.particles[i]
            x = (p.x - self.centerX) * self.zoom + float(self.width / 2)
            y = (p.y - self.centerY) * self.zoom + float(self.height / 2)
            # x = p.x + (self.width / 2)
            # y = p.y + (self.height / 2)
            col = self.types.get_color(p.type)
            col.a = int(opacity * 25.5)

            # print(x, y)
            pygame.draw.circle(ctx, col, (x, y), circleRadius, 0)

    def get_index(self, x, y):
            cx, cy = self.to_center(x, y)

            for i in range(len(self.particles)):
                dx = self.particles[i].x - cx
                dy = self.particles[i].y - cy

                if dx * dx + dy * dy < RADIUS * RADIUS:
                    return int(i)

            return -1

    def get_particle_x(self, index):
        return self.particles[index].x

    def get_particle_y(self, index):
        return self.particles[index].y

    def to_center(self, x, y):
        cx = self.centerX + (x - self.width / 2) / self.zoom
        cy = self.centerY + (y - self.height / 2) / self.zoom
        return cx, cy

    def set_zoom(self, cx, cy, zoom):
        # Apply the zoom
        self.centerX = cx
        self.centerY = cy
        self.zoom = max(1.0, zoom)

        # Clamp to make sure camera doesn't go out of bounds
        self.centerX = min(self.centerX, float(self.width)* (1.0 - 0.5 / self.zoom))
        self.centerY = min(self.centerY, float(self.height) * (1.0 - 0.5 / self.zoom))
        self.centerX = min(self.centerX, float(self.width)* (0.5 / self.zoom))
        self.centerY = min(self.centerY, float(self.height) * (0.5 / self.zoom))

    def print_params(self):
        print("Attract: ")
        for i in range(self.types.size()):
            for j in range(self.types.size()):
                print(self.types.get_attract(i, j))
            print("")

        print("MinR: ")
        for i in range(self.types.size()):
            for j in range(self.types.size()):
                print(self.types.get_minR(i, j))
            print("")

        print("MaxR: ")
        for i in range(self.types.size()):
            for j in range(self.types.size()):
                print(self.types.get_maxR(i, j))
            print("")

    def toggle_wrap(self):
        self.wrap = not self.wrap
