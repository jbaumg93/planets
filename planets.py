import random
import pygame
import pygame.gfxdraw
import numpy as np
import copy
from recordtype import recordtype

Planet = recordtype('Planet', 'c v m')

G = 10
MAX_INIT_V = 20
PLANETS = 5

SCREEN_X = 500
SCREEN_Y = 500

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption('Planets')
clock = pygame.time.Clock()

random_screen_x = lambda: random.uniform(0, SCREEN_X / 2) + SCREEN_X / 4
random_screen_y = lambda: random.uniform(0, SCREEN_Y / 2) + SCREEN_Y / 4

planets = [
    Planet(c=np.array([random_screen_x(), random_screen_y()]), v=np.random.rand(2) * MAX_INIT_V - (MAX_INIT_V / 2), m=int(random.uniform(5, 10))) for _ in range(PLANETS)
]

ADD_PLANET_WEIGHT = 10
sum_vm = np.sum([p.m * p.v for p in planets], axis=0)
p = Planet(c=np.array([random_screen_x(), random_screen_y()]), v=-sum_vm/ADD_PLANET_WEIGHT, m=ADD_PLANET_WEIGHT)
planets.append(p)

def draw(p, surface):
    x = int(p.c[0])
    y = int(p.c[1])
    if -100 < x < SCREEN_X + 100 and -100 < y < SCREEN_Y + 100:
        pygame.gfxdraw.aacircle(screen, x, y, p.m, (255, 0, 0))
        pygame.gfxdraw.filled_circle(screen, x, y, p.m, (255, 0, 0))

def update_planets():
    planets_copy = copy.deepcopy(planets)
    for p, Q_i in zip(planets, planets_copy):
        q_i = Q_i.c
        d2q_i = 0
        for Q_j in planets_copy:
            if Q_j is not Q_i:
                q_j = Q_j.c
                d2q_i += G * Q_j.m * (q_j - q_i) / (np.hypot(q_j, q_i) ** 2)

        p.v = Q_i.v + d2q_i
        p.c = Q_i.c + p.v


pygame.init()
clock = pygame.time.Clock()

last_time = pygame.time.get_ticks() - 1
fps_output = 0
panning = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            panning = True
        if event.type == pygame.MOUSEBUTTONUP:
            panning = False
        if event.type == pygame.MOUSEMOTION and panning:
            for p in planets:
                p.c = p.c + event.rel
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    current_time = pygame.time.get_ticks()
    fps = 1 / ((current_time - last_time) / 1000)
    fps_output += current_time - last_time
    last_time = current_time
    if fps_output > 1000:
        fps_output = 0
        print('FPS: %d   m*v sum: %s' % (int(fps), str(np.sum([p.m * p.v for p in planets], axis=0))))

    update_planets()

    screen.fill((0, 0, 0))
    [draw(p, screen) for p in planets]
    pygame.display.update()

    clock.tick(60)