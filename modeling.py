import pygame
from solver import Solution
import time
from copy import deepcopy
import numpy as np

FPS = 30 # just fps
WIDTH = 1000
HEIGHT = 1000

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class PhysicalSystem:
    def __init__(self, m, c, b, q0):
        self.solver = Solution(m, c, b)
        self.solver.solve(q0)
        self.start_value = np.array([np.pi / 2, 0.0, -np.pi/2, np.pi])

    def set_diplay_valirables(self, screen, center, r, main_circle_widht=3):
        self.screen = screen
        self.center = center
        self.r = r
        self.main_circle_widht = main_circle_widht
        
    def update_state(self, t_new):
        self.q = np.real(self.solver.q(t_new))

    def draw_body(self, i):
        current_angle = self.start_value[i] - self.q[i]
        current_center = (
            int(self.center[0] + self.r * np.cos(current_angle)), 
            int(self.center[1] + self.r * np.sin(current_angle))
        )

        pygame.draw.circle(
            self.screen,
            WHITE,
            current_center,
            10,
        )
        

    def draw(self):
        pygame.draw.circle(
            self.screen, 
            WHITE, 
            self.center, 
            int(self.r), 
            self.main_circle_widht
        )

        for i in range(self.q.shape[0]):
            self.draw_body(i)

class Model:
    def __init__(self, m, c, b, timedelta, q0, r):
        self.ps = PhysicalSystem(m, c, b, q0)
        self.r = r
        self.timedelta = timedelta

    def must_exit(self):
        for event in pygame.event.get():
            # check for window close
            if event.type == pygame.QUIT:
                return True
        return False

    def run(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Analytic Mechanics")
        self.clock = pygame.time.Clock()

        self.ps.set_diplay_valirables(self.screen, (int(WIDTH / 2), int(HEIGHT / 2)), self.r)
        time_start = time.time()

        counter = 0
        while counter < 100:
            counter += 1

            self.clock.tick(FPS)
            if self.must_exit():
                break

            self.screen.fill(BLACK)

            t = (time.time() - time_start) * self.timedelta
            self.ps.update_state(t)
            self.ps.draw()
            time.sleep(0.5)

            pygame.display.flip()
        

        pygame.quit()
