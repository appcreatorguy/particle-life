import random

from numpy import WRAP

import particles
from universe import *

WINDOW_H = 720
WINDOW_W = 1280
STEPS_PER_FRAME_NORMAL = 1

def main():
    print("=========================================================")
    print("\n")
    print("               Welcome to Particle Life")
    print("\n")
    print("  This is a particle-based game of life simulation based")
    print("on random attraction and repulsion between all particle")
    print("classes.")
    print("\n")
    print("=========================================================")
    print("\n")
    print("Controls:")
    print("         'B' - Randomize (Balanced)")
    print("         'C' - Randomize (Chaos)")
    print("         'D' - Randomize (Diversity)")
    print("         'F' - Randomize (Frictionless)")
    print("         'G' - Randomize (Gliders)")
    print("         'H' - Randomize (Homogeneity)")
    print("         'M' - Randomize (Medium Clusters)")
    print("         'Q' - Randomize (Quiescence)")
    print("         'S' - Randomize (Small Clusters)")
    print("         'W' - Toggle Wrap-Around")
    print("       Enter - Keep rules, but re-seed particles")
    print("       Space - Hold for slow-motion")
    print("         Tab - Print current parameters to console")
    print("  Left Click - Click a particle to follow it")
    print(" Right Click - Click anywhere to unfollow particle")
    print("Scroll Wheel - Zoom in/out")
    print("\n")
    input()

    # Create a universe of particles
    universe = Universe(9, 400, WINDOW_W, WINDOW_H)
    universe.re_seed(-0.32, 0.06, 0.0, 20.0, 20.0, 70.0, 0.05, False)

    # Camera Settings
    cam_x = float(WINDOW_W/2)
    cam_y = float(WINDOW_H/2)
    cam_zoom = 1.0
    cam_x_dest = cam_x
    cam_y_dest = cam_y
    cam_zoom_dest = cam_zoom
    last_scroll_time = 0
    track_index = -1
    steps_per_frame = STEPS_PER_FRAME_NORMAL

    # Create the window
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_W, WINDOW_H], vsync=1)
    pygame.display.set_caption("Particles")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_b: # Balanced
                    universe.set_population(9, 400)
                    universe.re_seed(-0.02, 0.06, 0.0, 20.0, 20.0, 70.0, 0.05, False)
                elif event.key == pygame.K_c: # Chaos
                    universe.set_population(6, 400)
                    universe.re_seed(0.02, 0.04, 0.0, 30.0, 30.0, 100.0, 0.01, False)
                elif event.key == pygame.K_d: # Diversity
                    universe.set_population(12, 400)
                    universe.re_seed(-0.01, 0.04, 0.0, 20.0, 10.0, 60.0, 0.05, True)
                elif event.key == pygame.K_f: # Frictionless
                    universe.set_population(6, 300)
                    universe.re_seed(0.01, 0.005, 10.0, 10.0, 10.0, 60.0, 0.0, True)
                elif event.key == pygame.K_g: # Gliders
                    universe.set_population(6, 400)
                    universe.re_seed(0.0, 0.06, 0.0, 20.0, 10.0, 50.0, 0.1, True)
                elif event.key == pygame.K_h: # Homogenity
                    universe.set_population(4, 400)
                    universe.re_seed(0.0,  0.04, 10.0, 10.0, 10.0, 80.0, 0.05, True)
                elif event.key == pygame.K_l: # Large Clusters
                    universe.set_population(6, 400)
                    universe.re_seed(0.025, 0.02, 0.0, 30.0, 20.0, 50.0, 0.05, False)
                elif event.key == pygame.K_m: # Medium Clusters
                    universe.set_population(6, 400)
                    universe.re_seed(0.02, 0.05, 0.0, 20.0, 20.0, 50.0, 0.05, False)
                elif event.key == pygame.K_q: # Quiescence
                    universe.set_population(6, 300)
                    universe.re_seed(-0.02, 0.1, 10.0, 20.0, 20.0, 60.0, 0.2, False)
                elif event.key == pygame.K_s: # Small Clusters
                    universe.set_population(6, 150)
                    universe.re_seed(-0.005, 0.01, 10.0, 10.0, 20.0, 50.0, 0.01, False)
                if event.key == pygame.K_w:
                    universe.toggle_wrap()
                if event.key == pygame.K_RETURN:
                    universe.set_random_particles()
                if event.key == pygame.K_SPACE:
                    steps_per_frame = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    steps_per_frame = STEPS_PER_FRAME_NORMAL

        screen.fill((0, 0, 0))
        for i in range(steps_per_frame):
            opacity = float(i + 1)
            universe.step()
            universe.draw(screen, opacity)

        pygame.display.flip()
        clock.tick(30)
