import pygame
import random
from config import WIDTH, HEIGHT, CELL

class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.obstacles = []
        self.direction = [CELL, 0]
        self.score = 0
        self.level = 1
        self.is_over = False

        self.food = self.generate_pos()
        self.poison = self.generate_pos()

        self.powerup = None
        self.powerup_kind = None
        self.powerup_timer = 0
        self.active_effect = None
        self.effect_end = 0
        self.shield = False
        self.speed_mod = 0

    def generate_pos(self):
        while True:
            pos = [random.randrange(0, WIDTH//CELL)*CELL, random.randrange(0, HEIGHT//CELL)*CELL]
            if pos not in self.snake and pos not in self.obstacles:
                return pos

    def update(self):
        now = pygame.time.get_ticks()

        if self.active_effect and now > self.effect_end:
            self.active_effect = None
            self.speed_mod = 0

        if self.powerup is None and random.random() < 0.005:
            self.powerup = self.generate_pos()
            self.powerup_kind = random.choice(["speed", "slow", "shield"])
            self.powerup_timer = now

        if self.powerup and now - self.powerup_timer > 8000:
            self.powerup = None
            self.powerup_kind = None

        new_head = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]

        hit_wall = not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT)
        hit_self = new_head in self.snake
        hit_obs  = new_head in self.obstacles

        if hit_wall or hit_self or hit_obs:
            if self.shield:
                self.shield = False
                return
            self.is_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.generate_pos()
            if self.score % 3 == 0:
                self.level += 1
                if self.level >= 3:
                    self.obstacles.append(self.generate_pos())
        elif new_head == self.poison:
            if len(self.snake) <= 2:
                self.is_over = True
            else:
                self.snake.pop()
                self.snake.pop()
                self.poison = self.generate_pos()
        elif self.powerup and new_head == self.powerup:
            self.active_effect = self.powerup_kind
            self.effect_end = now + 5000
            if self.powerup_kind == "speed":
                self.speed_mod = 4
            elif self.powerup_kind == "slow":
                self.speed_mod = -4
            elif self.powerup_kind == "shield":
                self.shield = True
                self.speed_mod = 0
            self.powerup = None
            self.powerup_kind = None
        else:
            self.snake.pop()