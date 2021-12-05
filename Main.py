import math
import random

import pygame

pygame.init()

WINDOW_WIDTH = pygame.display.Info().current_w
WINDOW_HEIGHT = pygame.display.Info().current_h
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
FPS = 60
G = 9.81 / 2 / 250
DEAD_ANGLE = 70


class ExplodedItem:
    def __init__(self, fw, color, vx, vy, twinkle_coef, twinkle_period, do_twinkle):
        self.xStart = fw.x
        self.yStart = fw.y
        self.x = fw.x
        self.y = fw.y
        self.prevX = fw.x
        self.prevY = fw.y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.t = 0
        self.life = random.randint(FPS * 1, FPS * 5)
        self.ended = False
        self.twinkle_coef = twinkle_coef
        self.twinkle_period_red = twinkle_period * random.uniform(0.5, 1.3)
        self.twinkle_period_green = twinkle_period * random.uniform(0.5, 1.3)
        self.twinkle_period_blue = twinkle_period * random.uniform(0.5, 1.3)
        if do_twinkle > 0:
            self.do_twinkle = True
        else:
            self.do_twinkle = False

    def move(self):
        self.prevX = self.x
        self.prevY = self.y
        self.t += 1
        self.x = self.xStart + self.vx * self.t
        self.y = self.yStart - self.vy * self.t + G * self.t * self.t
        if self.x < 0 or self.x > WINDOW_WIDTH or self.y > WINDOW_HEIGHT or self.t > self.life:
            self.ended = True

    def draw(self):
        a = [self.prevX, self.prevY]
        b = [self.x, self.y]

        color = self.color
        if self.do_twinkle:
            coef_red = self.twinkle_coef + (1 - self.twinkle_coef) * (
                        (1 + math.cos(self.t / self.twinkle_period_red * math.pi)) / 2)
            coef_green = self.twinkle_coef + (1 - self.twinkle_coef) * (
                        (1 + math.cos(self.t / self.twinkle_period_green * math.pi)) / 2)
            coef_blue = self.twinkle_coef + (1 - self.twinkle_coef) * (
                        (1 + math.cos(self.t / self.twinkle_period_blue * math.pi)) / 2)
            color = (int(self.color[0] * coef_red),
                     int(self.color[1] * coef_green),
                     int(self.color[2] * coef_blue))

        pygame.draw.line(window, color, a, b, 2)


class Firework:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = WINDOW_HEIGHT
        self.velocity = random.uniform(3.5, 9)
        self.velocityX = random.uniform(-1, 1)
        self.color = (random.randint(10, 255), random.randint(10, 255), random.randint(10, 255))
        self.end_y = random.uniform(10, WINDOW_HEIGHT / 2)
        self.ended = False

    def move(self):
        self.x += self.velocityX
        self.y -= self.velocity
        if self.y <= self.end_y or self.x < 0 or self.x > WINDOW_WIDTH:
            self.ended = True

    def draw(self):
        a = [int(self.x - self.velocityX / 2), int(self.y + self.velocity / 2)]
        b = [int(self.x + self.velocityX / 2), int(self.y - self.velocity / 2)]
        pygame.draw.line(window, self.color, a, b, 2)


def game():
    fireworks = [Firework()]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

        if random.uniform(0, 1) <= 1 / FPS:
            fireworks.append(Firework())

        window.fill((0, 0, 0))

        for firework in fireworks:
            firework.move()
            firework.draw()
            if firework.ended:
                fireworks.remove(firework)
                if firework.__class__.__name__ == 'Firework':
                    do_twinkle = random.randint(0, 1)
                    for i in range(1, random.randint(20, 100)):
                        angle = random.randint(270 + DEAD_ANGLE - 360, 270 - DEAD_ANGLE)
                        angle2 = random.randint(0, 180)
                        velocity = random.uniform(1.5, 5)
                        fireworks.append(ExplodedItem(firework,
                                                      firework.color,
                                                      velocity * math.cos(angle / 180 * math.pi) * math.cos(
                                                          angle2 / 180 * math.pi),
                                                      velocity * math.sin(angle / 180 * math.pi),
                                                      random.uniform(0.0, 0.2),
                                                      random.randint(int(FPS / 30), int(FPS / 5)),
                                                      do_twinkle))

        pygame.display.update()
        clock.tick(FPS)


game()
pygame.quit()
