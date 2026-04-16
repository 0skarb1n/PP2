import pygame
import datetime

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

bg = pygame.image.load('main_clock.png.jpg')
hand_min = pygame.image.load('OIP.png')
hand_sec = pygame.image.load('OIP2.png')

def draw_hand(image, angle):
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect(center=(400, 400))
    screen.blit(rotated, rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    
    sec_angle = -now.second * 6
    min_angle = -now.minute * 6

    screen.blit(bg, (0, 0))
    draw_hand(hand_min, min_angle)
    draw_hand(hand_sec, sec_angle)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()