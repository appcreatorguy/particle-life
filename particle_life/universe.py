"""Universe Class"""
import math
import random
from types import WrapperDescriptorType

import pygame
from numpy.random import default_rng

import hsv, particles
from resize_array import resize_array

radius = 5.0
diameter = 2.0
r_smooth = 2.0


class Universe:
    def __init__(self, numTypes, numParticles, width, height):
        self.randGen = random.random
        self.types = particles.ParticleTypes()
        self.particles = [particles.make_particle()] * numParticles

        self.set_size(width, height)
        self.set_population(numTypes, numParticles)

        self.centerX = self.width * 0.5
        self.centerY = self.height * 0.5
        self.zoom = 1
        self.attractMean = 0
        self.attractStd = 0
        self.minRLower = 0
        self.minRUpper = 0
        self.maxRLower = 0
        self.maxRUpper = 0
        self.friction = 0
        self.flatForce = False
        self.wrap = False

    def set_engine(self, newEngine):
        self.randGen = newEngine

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_population(self, numTypes, numParticles):
        self.types.resize(numTypes)
        resize_array(self.particles, numParticles, particles.make_particle())

    def re_seed(
        self,
        attractMean,
        attractStd,
        minRLower,
        minRUpper,
        maxRLower,
        maxRUpper,
        friction,
        flatForce,
    ):
        self.attractMean = attractMean
        self.attractStd = attractStd
        self.minRLower = minRLower
        self.minRUpper = minRUpper
        self.maxRLower = maxRLower
        self.maxRUpper = maxRUpper
        self.friction = friction
        self.flatForce = flatForce
        self.set_random_types()
        self.set_random_particles()

    def set_random_types(self):
        rng = default_rng()
        randAttr = rng.normal(self.attractMean, self.attractStd)
        randMinR = rng.uniform(self.minRLower, self.minRUpper)
        randMaxR = rng.uniform(self.maxRLower, self.maxRUpper)

        for i in range(self.types.size()):
            self.types.set_color(
                i, hsv.from_HSV(i / self.types.size(), 1, (i % 2) * 0.5 + 0.5)
            )

            for j in range(self.types.size()):
                if i == j:
                    self.types.set_attract(i, j, -abs(randAttr * (self.randGen())))
                    self.types.set_minR(i, j, diameter)
                else:
                    self.types.set_attract(i, j, randAttr * (self.randGen()))
                    self.types.set_minR(i, j, max(randMinR * (self.randGen()), diameter))

                self.types.set_maxR(
                    i, j, max(randMaxR * (self.randGen()), self.types.get_minR(i, j))
                )

                # keep radii symmetric
                self.types.set_maxR(j, i, self.types.get_maxR(i, j))
                self.types.set_minR(j, i, self.types.get_minR(i, j))

    def set_random_particles(self):
        rng = default_rng()
        randType = rng.uniform(0, self.types.size() - 1)
        randUni = rng.uniform(0, 1)
        randNorm = rng.normal(0, 1)

        for i in range(len(self.particles)):
            p = self.particles[i]
            p["type"] = round(randType * (self.randGen()))
            p["x"] = (randUni * (self.randGen()) * 0.5 + 0.25) * self.height
            p["y"] = (randUni * (self.randGen()) * 0.5 + 0.25) * self.width
            p["vx"] = randNorm * (self.randGen()) * 0.2
            p["vy"] = randNorm * (self.randGen()) * 0.2

    def step(self):
        for i in range(len(self.particles)):
            # Current Particle
            p = self.particles[i]

            # Interactions
            for j in range(len(self.particles)):
                # Other Particle
                q = self.particles[j]

                # Get deltas
                dx = q["x"] - p["x"]
                dy = q["y"] - p["y"]

                if self.wrap:
                    if dx > self.width * 0.5:
                        dx -= self.width
                    elif dx < -self.width * 0.5:
                        dx += self.width

                    if dy > self.height * 0.5:
                        dy -= self.height
                    elif dy < -self.height * 0.5:
                        dy += self.height

                # Get distance squared
                r2 = dx * dx + dy * dy
                minR = self.types.get_minR(p["type"], q["type"])
                maxR = self.types.get_maxR(p["type"], q["type"])

                if r2 > maxR * maxR or r2 < 0.01:
                    continue

                # Normalise displacement
                r = math.sqrt(r2)
                dx /= r
                dy /= r

                # Calculate flatForce
                f = 0.0
                if r > minR:
                    if self.flatForce:
                        f = self.types.get_attract(p["type"], q["type"])
                    else:
                        numer = 2.0 * abs(r - 0.5 * (maxR + minR))
                        denom = maxR - minR
                        f = self.types.get_attract(p["type"], q["type"]) * (
                            1.0 - numer / denom
                        )
                else:
                    f = (
                        r_smooth
                        * minR
                        * (1.0 / (minR + r_smooth) - 1.0 / (r + r_smooth))
                    )

                p["vx"] = f * dx
                p["vy"] = f * dy
            self.particles[i] = p

        # Update Position
        for i in range(len(self.particles)):
            # Current Particle
            p = self.particles[i]

            # Update Position and velocity
            p["x"] = p["vx"]
            p["y"] = p["vy"]
            p["vx"] = 1.0 - self.friction
            p["vy"] = 1.0 - self.friction

            # Check for wall
            if self.wrap:
                if p["x"] < 0:
                    p["x"] += self.width
                elif p["x"] >= self.width:
                    p["x"] -= self.width

                if p["y"] < 0:
                    p["y"] + self.height
                elif p["y"] >= self.height:
                    p["y"] -= self.height

            else:
                if p["x"] < diameter:
                    p["vx"] = -p["vx"]
                    p["x"] = diameter
                elif p["x"] >= self.width - diameter:
                    p["vx"] = -p["vx"]
                    p["x"] = self.width - diameter

                if p["y"] < diameter:
                    p["vy"] = -p["vy"]
                    p["y"] = diameter
                elif p["y"] >= self.height - diameter:
                    p["vy"] = -p["vy"]
                    p["y"] = self.height - diameter

            self.particles[i] = p

    def draw(self, ctx, opacity):
        circleRadius = radius * self.zoom
        for i in range(len(self.particles)):
            p = self.particles[i]
            x = (p["x"] - self.centerX) * self.zoom + self.width / 2
            y = (p["y"] - self.centerY) * self.zoom + self.height / 2
            col = self.types.get_color(p["type"])

            print(pygame.Color(col['r'], col['g'], col['b']), (x, y), circleRadius, 0)
            pygame.draw.circle(
                ctx,
                pygame.Color(col['r'], col['g'], col['b']), # pygame.Color(col["r"], col["g"], col["b"], col["a"]) if (col['a'] in col.keys()) else pygame.Color(col['r'], col['g'], col['b']),
                (x, y),
                circleRadius,
                0,
            )

    def get_index(self, x, y):
        cx, cy = self.to_center(x, y)

        for i in range(len(self.particles)):
            dx = self.particles[i]["x"] - cx
            dy = self.particles[i]["y"] - cy

            if dx * dx + dy * dy < radius * radius:
                return i

        return -1

    def get_particle_x(self, index):
        return self.particles[index]["x"]

    def get_particle_y(self, index):
        return self.particles[index]["x"]

    def to_center(self, x, y):
        cx = self.centerX + (x - self.width / 2) / self.zoom
        cy = self.centerY + (y - self.height / 2) / self.zoom
        return cx, cy

    def set_zoom(self, cx, cy, zoom):
        # Apply the zoom
        self.centerX = cx
        self.centerY = cy
        self.zoom = max(1, zoom)

        # Clamp to make sure camera doesn't go out of bounds
        self.centerX = min(self.centerX, self.width * (1.0 - 0.5 / self.zoom))
        self.centerY = min(self.centerY, self.height * (1.0 - 0.5 / self.zoom))
        self.centerX = min(self.centerX, self.width * (0.5 / self.zoom))
        self.centerY = min(self.centerY, self.height * (0.5 / self.zoom))

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
