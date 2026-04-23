import pygame, sys, random, time

pygame.init()

W, H = 400, 600
sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

f = pygame.font.SysFont("Arial", 20)
f_big = pygame.font.SysFont("Arial", 60)

bg = pygame.image.load("road.jpg")
bg = pygame.transform.rotate(bg, 90)
bg = pygame.transform.scale(bg, (W, H))

p_img = pygame.image.load("player.png")
e_img = pygame.image.load("Enemy.png")

p_rect = p_img.get_rect(center=(200, 500))
e_rect = e_img.get_rect(center=(random.randint(50, 350), -50))
c_rect = pygame.Rect(random.randint(50, 350), -50, 30, 30)

sound_crash = pygame.mixer.Sound("crush.mp3")
sound_money = pygame.mixer.Sound("money.mp3")

speed = 5
score = 0
coins = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and p_rect.left > 0: 
        p_rect.x -= 5
    elif keys[pygame.K_RIGHT] and p_rect.right < W: 
        p_rect.x += 5

    e_rect.y += speed
    c_rect.y += speed

    if e_rect.top > H:
        e_rect.center = (random.randint(50, 350), -50)
        score += 1
        speed += 0.1

    if c_rect.top > H:
        c_rect.center = (random.randint(50, 350), -50)

    if p_rect.colliderect(e_rect):
        sound_crash.play()
        
        sc.fill((255, 0, 0))
        txt = f_big.render("GAME OVER", True, (255, 255, 255))
        sc.blit(txt, (40, 250))
        pygame.display.update()
        
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if p_rect.colliderect(c_rect):
        sound_money.play()
        coins += 1
        c_rect.center = (random.randint(50, 350), -50)

    sc.blit(bg, (0, 0))
    sc.blit(p_img, p_rect)
    sc.blit(e_img, e_rect)
    pygame.draw.circle(sc, (255, 215, 0), c_rect.center, 15)

    sc.blit(f.render(f"Score: {score}", True, (0,0,0)), (10, 10))
    sc.blit(f.render(f"Coins: {coins}", True, (0,0,0)), (300, 10))

    pygame.display.update()
    clock.tick(60)