import pygame, sys, random, time
from persistence import load_leaderboard, add_score, load_settings, save_settings

pygame.init()

W, H = 400, 600
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

f = pygame.font.SysFont("Arial", 20)
f_big = pygame.font.SysFont("Arial", 48, bold=True)

bg = pygame.image.load("road.jpg")
bg = pygame.transform.rotate(bg, 90)
bg = pygame.transform.scale(bg, (W, H))

p_img = pygame.image.load("player.png")
p_img = pygame.transform.scale(p_img, (60, 100))
e_img = pygame.image.load("Enemy.png")
e_img = pygame.transform.scale(e_img, (60, 100))

try:
    sound_crash = pygame.mixer.Sound("crush.mp3")
    sound_money = pygame.mixer.Sound("money.mp3")
except:
    sound_crash = None
    sound_money = None

settings = load_settings()

def draw_btn(text, x, y, w=200, h=45, col=(80,80,80)):
    pygame.draw.rect(sc, col, (x, y, w, h), border_radius=8)
    t = f.render(text, True, (255,255,255))
    sc.blit(t, (x + w//2 - t.get_width()//2, y + h//2 - t.get_height()//2))
    return pygame.Rect(x, y, w, h)

state = "menu"
username = ""
typing_name = False

while True:

    if state == "menu":
        sc.blit(bg, (0, 0))
        title = f_big.render("RACER", True, (255,220,0))
        sc.blit(title, (W//2 - title.get_width()//2, 60))
        play_btn = draw_btn("Play",        100, 160, 200, 45, (60,180,60))
        lb_btn   = draw_btn("Leaderboard", 100, 220, 200, 45, (60,100,200))
        set_btn  = draw_btn("Settings",    100, 280, 200, 45, (100,100,100))
        quit_btn = draw_btn("Quit",        100, 340, 200, 45, (180,60,60))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):  state = "username"
                if lb_btn.collidepoint(event.pos):    state = "leaderboard"
                if set_btn.collidepoint(event.pos):   state = "settings"
                if quit_btn.collidepoint(event.pos):  pygame.quit(); sys.exit()

    elif state == "username":
        sc.fill((20,20,20))
        sc.blit(f.render("Enter name:", True, (255,255,255)), (130, 220))
        pygame.draw.rect(sc, (255,255,255), (80, 250, 240, 35), border_radius=5)
        sc.blit(f.render(username + "|", True, (0,0,0)), (90, 258))
        sc.blit(f.render("Press Enter to start", True, (150,150,150)), (90, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(username) > 0:
                    state = "game"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.unicode and len(username) < 14:
                    username += event.unicode

    elif state == "leaderboard":
        sc.fill((20,20,20))
        sc.blit(f_big.render("TOP 10", True, (255,220,0)), (120, 20))
        board = load_leaderboard()
        for i, e in enumerate(board):
            col = (255,220,0) if i == 0 else (255,255,255)
            sc.blit(f.render(f"{i+1}. {e['name']}  {e['score']}pts  {e['distance']}m", True, col), (20, 80 + i*40))
        back = draw_btn("Back", 100, 530, 200, 45)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(event.pos): state = "menu"

    elif state == "settings":
        sc.fill((20,20,20))
        sc.blit(f_big.render("Settings", True, (255,255,255)), (100, 30))
        snd_col = (60,180,60) if settings["sound"] else (180,60,60)
        snd_btn = draw_btn("Sound: ON" if settings["sound"] else "Sound: OFF", 100, 130, 200, 45, snd_col)
        sc.blit(f.render("Difficulty:", True, (200,200,200)), (30, 210))
        easy_btn = draw_btn("Easy",   20,  240, 100, 40, (60,180,60) if settings["difficulty"]=="easy" else (80,80,80))
        norm_btn = draw_btn("Normal", 145, 240, 110, 40, (60,100,200) if settings["difficulty"]=="normal" else (80,80,80))
        hard_btn = draw_btn("Hard",   275, 240, 100, 40, (180,60,60) if settings["difficulty"]=="hard" else (80,80,80))
        back_btn = draw_btn("Back", 100, 520, 200, 45)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if snd_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)
                if easy_btn.collidepoint(event.pos):
                    settings["difficulty"] = "easy"; save_settings(settings)
                if norm_btn.collidepoint(event.pos):
                    settings["difficulty"] = "normal"; save_settings(settings)
                if hard_btn.collidepoint(event.pos):
                    settings["difficulty"] = "hard"; save_settings(settings)
                if back_btn.collidepoint(event.pos):
                    state = "menu"

    elif state == "game":
        if settings["difficulty"] == "easy":   speed = 3; spawn_every = 100
        elif settings["difficulty"] == "hard": speed = 7; spawn_every = 40
        else:                                  speed = 5; spawn_every = 60

        p_rect = p_img.get_rect(center=(W//2, 500))
        e_rect = e_img.get_rect(center=(random.randint(40,360), -60))
        obs_rect = pygame.Rect(random.randint(40,350), -200, 50, 25)
        c_rect = pygame.Rect(random.randint(40,360), -100, 28, 28)
        pu_rect = pygame.Rect(random.randint(40,360), -400, 36, 36)
        pu_kind = random.choice(["nitro","shield","repair"])

        coins = 0
        distance = 0
        frame = 0
        bg_y1 = 0
        bg_y2 = -H
        shield_on = False
        nitro_on = False
        nitro_frames = 0
        active_pu = None
        pu_timer = 0

        running = True
        while running:
            clock.tick(60)
            frame += 1
            distance += 1
            score = coins * 10 + distance // 10

            if frame % 400 == 0:
                speed += 0.5

            if nitro_on:
                nitro_frames -= 1
                if nitro_frames <= 0:
                    nitro_on = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False; state = "menu"

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]  and p_rect.left > 0:   p_rect.x -= 12
            if keys[pygame.K_RIGHT] and p_rect.right < W:  p_rect.x += 12
            if keys[pygame.K_UP]    and p_rect.top > 0:    p_rect.y -= 12
            if keys[pygame.K_DOWN]  and p_rect.bottom < H: p_rect.y += 12

            cur_speed = speed * (1.5 if nitro_on else 1)
            bg_y1 += cur_speed; bg_y2 += cur_speed
            if bg_y1 >= H: bg_y1 = -H
            if bg_y2 >= H: bg_y2 = -H

            e_rect.y += cur_speed
            obs_rect.y += cur_speed
            c_rect.y += cur_speed
            pu_rect.y += cur_speed

            if e_rect.top > H:   e_rect.center = (random.randint(40,360), -60)
            if obs_rect.top > H: obs_rect = pygame.Rect(random.randint(40,350), -30, 50, 25)
            if c_rect.top > H:   c_rect = pygame.Rect(random.randint(40,360), -20, 28, 28)
            if pu_rect.top > H:
                pu_rect = pygame.Rect(random.randint(40,360), -30, 36, 36)
                pu_kind = random.choice(["nitro","shield","repair"])

            if p_rect.colliderect(e_rect):
                if shield_on:
                    shield_on = False
                    e_rect.center = (random.randint(40,360), -60)
                else:
                    if sound_crash: sound_crash.play()
                    running = False; state = "gameover"

            if p_rect.colliderect(obs_rect):
                if shield_on:
                    shield_on = False
                    obs_rect = pygame.Rect(random.randint(40,350), -200, 50, 25)
                else:
                    if sound_crash: sound_crash.play()
                    running = False; state = "gameover"

            if p_rect.colliderect(c_rect):
                if sound_money: sound_money.play()
                coins += 1
                c_rect = pygame.Rect(random.randint(40,360), -20, 28, 28)

            if p_rect.colliderect(pu_rect):
                active_pu = pu_kind
                pu_timer = 180
                if pu_kind == "nitro":   nitro_on = True; nitro_frames = 180
                elif pu_kind == "shield": shield_on = True
                pu_rect = pygame.Rect(random.randint(40,360), -400, 36, 36)

            if active_pu and pu_timer > 0:
                pu_timer -= 1
                if pu_timer == 0: active_pu = None

            sc.blit(bg, (0, bg_y1))
            sc.blit(bg, (0, bg_y2))
            sc.blit(e_img, e_rect)
            pygame.draw.rect(sc, (200,50,50), obs_rect, border_radius=4)
            pygame.draw.circle(sc, (255,215,0), c_rect.center, 14)

            pu_col = (255,140,0) if pu_kind=="nitro" else (100,200,255) if pu_kind=="shield" else (60,200,60)
            pygame.draw.rect(sc, pu_col, pu_rect, border_radius=6)
            sc.blit(f.render(pu_kind[0].upper(), True, (255,255,255)), (pu_rect.x+10, pu_rect.y+8))

            sc.blit(p_img, p_rect)
            if shield_on:
                pygame.draw.ellipse(sc, (100,200,255), p_rect.inflate(16,16), 3)

            sc.blit(f.render(f"Score: {score}", True, (0,0,0)), (10, 10))
            sc.blit(f.render(f"Coins: {coins}", True, (0,0,0)), (W-100, 10))
            sc.blit(f.render(f"Dist: {distance}m", True, (0,0,0)), (10, 35))
            if active_pu:
                sc.blit(f.render(f"{active_pu} active", True, (255,220,0)), (10, 60))

            pygame.display.update()

    elif state == "gameover":
        add_score(username, score, distance)
        sc.fill((20,20,20))
        sc.blit(f_big.render("GAME OVER", True, (220,60,60)), (60, 80))
        sc.blit(f.render(f"Score: {score}", True, (255,255,255)), (120, 200))
        sc.blit(f.render(f"Distance: {distance}m", True, (255,255,255)), (120, 235))
        sc.blit(f.render(f"Coins: {coins}", True, (255,220,0)), (120, 270))
        retry_btn = draw_btn("Retry",     60,  350, 130, 45, (60,180,60))
        menu_btn  = draw_btn("Main Menu", 210, 350, 130, 45, (60,100,200))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos): state = "game"
                if menu_btn.collidepoint(event.pos):  state = "menu"

    clock.tick(60)