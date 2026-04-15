import pygame
import datetime

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# Используем 'r' перед строкой, чтобы бэкслеши не ломали код
bg = pygame.image.load(r'main_clock.png.jpg')
hand1 = pygame.image.load(r'mickey_hand1.png.jpg')
hand2 = pygame.image.load(r'mickey_hand2.png.jpg')

def rotate_hand(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=(400, 400))
    return rotated_image, new_rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    now = datetime.datetime.now()
    
    
    sec_angle = -(now.second * 6) + 90
    min_angle = -(now.minute * 6) + 90

    
    screen.fill((255, 255, 255))
    screen.blit(bg, (0, 0))

    
    img_min, rect_min = rotate_hand(hand1, min_angle)
    screen.blit(img_min, rect_min)

    img_sec, rect_sec = rotate_hand(hand2, sec_angle)
    screen.blit(img_sec, rect_sec)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()