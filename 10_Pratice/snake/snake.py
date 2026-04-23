import pygame, sys, random, time

pygame.init()

W, H = 600, 400
sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
f = pygame.font.SysFont("Arial", 25)

x, y = 300, 200
dx, dy = 0, 0
snake_body = [[x, y]]
length = 1

food_x = round(random.randrange(0, W - 10) / 10.0) * 10.0
food_y = round(random.randrange(0, H - 10) / 10.0) * 10.0

score = 0
level = 1
speed = 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -10
                dy = 0
            elif event.key == pygame.K_RIGHT:
                dx = 10
                dy = 0
            elif event.key == pygame.K_UP:
                dy = -10
                dx = 0
            elif event.key == pygame.K_DOWN:
                dy = 10
                dx = 0

    x += dx
    y += dy

    if x >= W or x < 0 or y >= H or y < 0:
        time.sleep(0.5)
        pygame.quit()
        sys.exit()

    head = [x, y]
    snake_body.append(head)

    if len(snake_body) > length:
        del snake_body[0]

    for part in snake_body[:-1]:
        if part == head:
            time.sleep(0.5)
            pygame.quit()
            sys.exit()

    if x == food_x and y == food_y:
        food_x = round(random.randrange(0, W - 10) / 10.0) * 10.0
        food_y = round(random.randrange(0, H - 10) / 10.0) * 10.0
        
        length += 1
        score += 1
        
        if score % 3 == 0:
            level += 1
            speed += 2

    sc.fill((255, 255, 255))
    
    pygame.draw.rect(sc, (213, 50, 80), [food_x, food_y, 10, 10])
    
    for part in snake_body:
        pygame.draw.rect(sc, (0, 0, 0), [part[0], part[1], 10, 10])

    score_txt = f.render("Score: " + str(score), True, (0, 0, 0))
    level_txt = f.render("Level: " + str(level), True, (0, 0, 0))
    sc.blit(score_txt, (10, 10))
    sc.blit(level_txt, (W - 100, 10))

    clock.tick(120)
    pygame.display.update()
    clock.tick(speed)