import hsv
import universe as uni
import pygame
from pygame.locals import *

window_w = 1280
window_h = 720
steps_per_frame_normal = 1


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

    # Create the universe of particles
    universe = uni.Universe(9, 400, window_w, window_h)
    universe.re_seed(-0.02, 0.06, 0.0, 20.0, 20.0, 70.0, 0.05, False)

    # Camera settings
    cam_x = window_w / 2
    cam_y = window_h / 2
    cam_zoom = 1.0
    cam_x_dest = cam_x
    cam_y_dest = cam_y
    cam_zoom_dest = cam_zoom
    last_scroll_time = 0
    track_index = -1
    steps_per_frame = steps_per_frame_normal

    # Create the windows
    pygame.init()
    screen = pygame.display.set_mode([window_w, window_h], vsync = 1)
    pygame.display.set_caption("Particles")
    surface = pygame.surface.Surface([400, 300])
    clock = pygame.time.Clock()

    # Main Loop
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
                    universe.set_population(6, 600)
                    universe.re_seed(-0.005, 0.01, 10.0, 10.0, 20.0, 50.0, 0.01, False)
                elif event.key == pygame.K_w:
                    universe.toggle_wrap()
                elif event.key == pygame.K_RETURN:
                    universe.set_random_particles()
                elif event.key == pygame.K_TAB:
                    universe.print_params()
                elif event.key == pygame.K_SPACE:
                    steps_per_frame = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    steps_per_frame = steps_per_frame_normal
            elif event.type == pygame.MOUSEWHEEL:
                cam_zoom_dest *= pow(1.1, event.y)
                cam_zoom_dest = max(min(cam_zoom_dest, 10.0), 1.0)
                cur_time = clock.get_time()
                if cur_time - last_scroll_time > 300:
                    # Only update position if scroll just started
                    (x, y) = pygame.mouse.get_pos()
                    universe.to_center(x, y)
                last_scroll_time = cur_time
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    track_index = universe.get_index(event.pos[0], event.pos[1])
                elif event.button == 3:
                    track_index = -1

        # Apply Zoom
        if track_index >= 0:
            cam_x_dest = universe.get_particle_x(track_index)
            cam_y_dest = universe.get_particle_y(track_index)
        cam_x = cam_x * 0.9 + cam_x_dest * 0.1
        cam_y = cam_y * 0.9 + cam_y_dest * 0.1
        cam_zoom = cam_zoom*0.8 + cam_zoom_dest*0.2
        universe.set_zoom(cam_x, cam_y, cam_zoom)

        # Apply physics and draw
        # surface.fill((0,0,0,0)) # Clear screen
        for i in range(steps_per_frame):
            opacity = float(i + 1) / float(steps_per_frame)
            universe.step()
            universe.draw(surface, opacity)
        screen.blit(pygame.transform.scale(surface, screen.get_rect().size), (0,0))

        # Flip the screen buffer
        pygame.display.flip()
        clock.tick(60)

