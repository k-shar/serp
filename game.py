import pygame
from constants import *
from window_sizing import *
import random
from pygame import freetype
from colour import Color

red = Color("red")
colors = list(red.range_to(Color("green"), 10000))


class Dot(pygame.sprite.Sprite):
    def __init__(self, loc):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]


class Node(pygame.sprite.Sprite):
    def __init__(self, spawn, color, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.color = color
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = spawn[0]*500, spawn[1]*500

        self.held = False

    def update(self):
        self.image.fill(self.color)

        if self.held:
            mouse = pygame.mouse.get_pos()
            self.rect.centerx = mouse[0]
            self.rect.centery = mouse[1]
            self.image.fill(WHITE)


def game(screen):
    run = False
    stepB = False
    clock = pygame.time.Clock()
    pygame.display.set_caption("Game Screen")

    head = Node((0.5, 0.5), BLACK, 20)

    left = Node((0.5, 0.8), BLUE, 20)
    right = Node((0.8, 0.4), BLUE, 20)
    top = Node((0.2, 0.2), BLUE, 20)

    stop = TextWindow(RED, (3, 1), (0.2, 0.1), 0.2, "Stop")
    start = TextWindow(GREEN, (3, 1), (0.8, 0.1), 0.2, "Start")
    step = TextWindow(BLUE, (3, 1), (0.5, 0.1), 0.2, "Step")
    total = TextWindow(PINK, (5,1), (0.3, 0.9), 0.3, "total= ")
    count = 0

    nodes = pygame.sprite.Group()
    nodes.add(left)
    nodes.add(right)
    nodes.add(top)

    dots = pygame.sprite.Group()

    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': 500, 'h': 500}))
    while True:
        screen.fill("#A5C2DC")
        nodes.update()
        head.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return screen
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                stop.resize(screen)
                start.resize(screen)
                step.resize(screen)
                total.resize(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in nodes.sprites():
                    if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        sprite.held = True

                if head.rect.collidepoint(pygame.mouse.get_pos()):
                    head.held = True

            if event.type == pygame.MOUSEBUTTONUP:

                for sprite in nodes.sprites():
                    sprite.held = False
                head.held = False

                if start.rect.collidepoint(pygame.mouse.get_pos()):
                    run = True
                if stop.rect.collidepoint(pygame.mouse.get_pos()):
                    run = False
                if step.rect.collidepoint(pygame.mouse.get_pos()):
                    stepB = True

        if run or stepB:
            count += 1
            total.text = f"total= {count}"
            total.resize(screen)

            stepB = False

            point = nodes.sprites()[random.randint(0,2)].rect
            point = (point[0], point[1])

            loc = (point[0] - head.rect.x, point[1] - head.rect.y)
            scalar = 0.5
            loc = (scalar * loc[0], scalar * loc[1])
            loc = (loc[0] + head.rect.x, loc[1] + head.rect.y)
            dots.add(Dot(loc))

            head.rect.x = loc[0]
            head.rect.y = loc[1]

        screen.blit(stop.image, stop.rect)
        screen.blit(start.image, start.rect)
        screen.blit(step.image, step.rect)
        screen.blit(total.image, total.rect)

        screen.blit(head.image, head.rect)
        nodes.draw(screen)
        dots.draw(screen)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    pygame.display.init()
    pygame.freetype.init()
    main_screen = pygame.display.set_mode((300, 200), pygame.RESIZABLE)
    game(main_screen)
    pygame.quit()