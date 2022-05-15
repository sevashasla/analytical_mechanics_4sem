import pygame
from solver import Solution
import time
from copy import deepcopy
import numpy as np

FPS = 30
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
        '''
            m - mass
            c - stiffness coefficient
            b - dissipative coefficient
            q0 - initial state
        '''
        # create solver and solve equation
        self.solver = Solution(m, c, b)
        self.solver.solve(q0)

        # initial state
        self.start_value = np.array([np.pi / 2, 0.0, -np.pi/2, -np.pi])
        self.coords = None

    def set_diplay_valirables(
            self, 
            screen, 
            center, 
            main_r, 
            main_circle_widht=3,
            body_r=15,
            spring_n_turns = 15,
            spring_radius = 10,
        ):
        '''
            screen - surface from pygame
            center - coords of center
            main_r - radius of the main circle
            main_circle_width - width of the main circle
            body_r - radius of the bodies
            spring_n_turns - number of spring turns
            spring_radius - radius of the springs
        '''
        self.screen = screen
        self.center = center
        self.main_r = main_r
        self.main_circle_widht = main_circle_widht
        self.body_r = body_r
        self.spring_n_turns = spring_n_turns
        self.spring_radius = spring_radius
        
    def update_state(self, t_new):
        '''
            update the state of physical system
            in new moment of time
        '''
        self.q = np.real(self.solver.q(t_new))
        self.angles = self.start_value - self.q
        self.coords = np.vstack(( # many points, so I can't use __find_point here
            self.center[0] + self.main_r * np.cos(self.angles), 
            self.center[1] + self.main_r * np.sin(self.angles)
        )).astype(dtype=int)

    def is_end(self):
        pass


    def __draw_body(self, i):
        c = WHITE
        if i == 0:
            c = RED # with dissipative

        pygame.draw.circle(
            self.screen,
            c,
            self.coords[:, i],
            self.body_r,
        )

    def __draw_spring(
            self, 
            idx, 
        ):
        '''
            draw springs between elements idx and idx + 1
            spring : spring_n_turns it is broken line. Each segment
            goes after delta phi and their radiueses are changing
        '''
    
        idx_start = idx
        idx_end = (idx + 1) % self.q.shape[0]

        # extreme case!
        extreme_case_add = 0
        if idx + 1 == self.q.shape[0]:
            extreme_case_add = 2 * np.pi

        delta_phi = (self.angles[idx_end] - extreme_case_add - self.angles[idx_start]) \
            / self.spring_n_turns
        delta_r = self.spring_radius
        
        # initial angle, will be changed
        current_angle = self.angles[idx_start]

        points = []
        # start point
        points.append(self.__find_point(current_angle, self.main_r))

        for i in range(self.spring_n_turns):
            current_angle += delta_phi
            points.append(self.__find_point(current_angle, self.main_r + delta_r))
            delta_r *= -1.0

        # end point
        points.append(self.__find_point(current_angle, self.main_r))

        # than draw
        pygame.draw.lines(self.screen, WHITE, False, points)


    def draw(self):
        # draw the main cycle
        pygame.draw.circle(
            self.screen, 
            WHITE, 
            self.center, 
            int(self.main_r), 
            self.main_circle_widht
        )

        for i in range(self.q.shape[0]):
                self.__draw_spring(i)

        for i in range(self.q.shape[0]):
            self.__draw_body(i)


    def __find_point(self, angle, radius):
        '''
            find position (like x, y) of point
            on circle with center = self.center and 
            angled by angle
        '''
        return (
            int(self.center[0] + radius * np.cos(angle)), 
            int(self.center[1] + radius * np.sin(angle))
        )


class Model:
    def __init__(self, m, c, b, timedelta, q0, r):
        '''
            m - mass
            c - stiffness coefficient
            b - dissipative coefficient
            timedelta - how fast time in system is going
            q0 - initial state
            r - radius of the main circle
        '''
        self.ps = PhysicalSystem(m, c, b, q0)
        self.r = r
        self.timedelta = timedelta

        self.params = [
            f"m: {m}", 
            f"c: {c}",
            f"b: {b}",
            f"q0: {q0[0]:.2}, {q0[1]:.2}, {q0[2]:.2}, {q0[3]:.2}",
        ]

    def must_exit(self):
        for event in pygame.event.get():
            # check for window close
            if event.type == pygame.QUIT:
                return True
        return False

    def __draw_params(self, t):
        '''
            draws time in system
            and params : m, c, b, q0
        '''
        font = pygame.font.SysFont(None, 40)

        curr_coords = np.array([20, 20])
        img = font.render(f"time: {np.round(t, 2)}", True, WHITE)
        self.screen.blit(img, curr_coords)

        for param in self.params:
            curr_coords[1] += 22 # TODO
            img = font.render(param, True, WHITE)
            self.screen.blit(img, curr_coords)

    def run(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Analytic Mechanics")
        self.clock = pygame.time.Clock()

        self.ps.set_diplay_valirables(self.screen, (int(WIDTH / 2), int(HEIGHT / 2)), self.r)
        time_start = time.time()

        while True:
            self.clock.tick(FPS)
            if self.must_exit():
                break

            self.screen.fill(BLACK)

            t = (time.time() - time_start) * self.timedelta
            self.ps.update_state(t)
            self.ps.draw()
            self.__draw_params(t)

            pygame.display.flip()
            time.sleep(0.1) # TODO
        
        pygame.quit()
