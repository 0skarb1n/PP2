import pygame

import random


pygame.init()

screen = pygame.display.set_mode((800,800))

pygame.mixer.music.load('music.mp3')

running = True

clock = pygame.time.Clock()

x = 200
y = 150
z = 50

x1=random.randint(50,750)
y1=random.randint(50,750)
 

stop=False

while running:

    screen.fill((0,255,255))

    pygame.draw.circle(screen, (255, 255, 0), (x1, y1), 25)
    pygame.draw.circle(screen, (200, 200, 0), (x1, y1), 20)



    
    distance = ((x - x1)**2 + (y - y1)**2)**0.5

    if distance < (z + 25): 
        x1 = random.randint(50, 750)
        y1 = random.randint(50, 750)
        z += 5

    pygame.draw.circle(screen, (255, 0, 0), (x, y), z)

    keys = pygame.key.get_pressed()
    
    
    if keys[pygame.K_RIGHT] and x < 800 - z:
        x += 5
    if keys[pygame.K_LEFT] and x > z:
        x -= 5
    if keys[pygame.K_UP] and y >z:
            y-=5
    if keys[pygame.K_DOWN]and y <800-z:
            y+=5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                print("Нажали Play")
                pygame.mixer.music.play(-1)
            if event.key == pygame.K_s:
                print("Нажали Stop")
                pygame.mixer.music.stop()
       
    pygame.display.flip()
    clock.tick(60)