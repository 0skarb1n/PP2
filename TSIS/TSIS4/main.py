import pygame
import sys
import json
import os
from game import SnakeGame
from db import DBManager
from config import WIDTH, HEIGHT, CELL, FPS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont("Consolas", 22)
big_font = pygame.font.SysFont("Consolas", 44, bold=True)
clock = pygame.time.Clock()

try:
    db = DBManager()
except:
    print("DB Error! Check config.py")
    sys.exit()

def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json") as f:
            return json.load(f)
    return {"snake_color": [0, 255, 0], "grid": False, "sound": True}

def save_settings(s):
    with open("settings.json", "w") as f:
        json.dump(s, f)

settings = load_settings()

def draw_btn(text, x, y, w=200, h=45, col=(80,80,80)):
    pygame.draw.rect(screen, col, (x, y, w, h), border_radius=8)
    t = font.render(text, True, (255,255,255))
    screen.blit(t, (x + w//2 - t.get_width()//2, y + h//2 - t.get_height()//2))
    return pygame.Rect(x, y, w, h)

def screen_menu():
    username = ""
    while True:
        screen.fill((20, 20, 25))
        title = big_font.render("SNAKE", True, (0, 255, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        nl = font.render("Enter name:", True, (200,200,200))
        screen.blit(nl, (WIDTH//2 - 100, 130))
        pygame.draw.rect(screen, (255,255,255), (WIDTH//2-100, 158, 200, 35), border_radius=5)
        nt = font.render(username + "|", True, (0,0,0))
        screen.blit(nt, (WIDTH//2 - 90, 165))

        play_btn = draw_btn("Play",        WIDTH//2-100, 220, 200, 45, (60,180,60))
        lb_btn   = draw_btn("Leaderboard", WIDTH//2-100, 280, 200, 45, (60,100,200))
        set_btn  = draw_btn("Settings",    WIDTH//2-100, 340, 200, 45, (100,100,100))
        quit_btn = draw_btn("Quit",        WIDTH//2-100, 400, 200, 45, (180,60,60))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN and username:
                    return username, "play"
                elif event.unicode and len(username) < 12:
                    username += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos) and username:
                    return username, "play"
                if lb_btn.collidepoint(event.pos):
                    return username, "leaderboard"
                if set_btn.collidepoint(event.pos):
                    return username, "settings"
                if quit_btn.collidepoint(event.pos):
                    pygame.quit(); sys.exit()

def screen_leaderboard():
    board = db.get_top_10()
    while True:
        screen.fill((20,20,25))
        t = big_font.render("TOP 10", True, (255,215,0))
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 20))
        screen.blit(font.render("#  Name         Score  Lvl", True, (150,150,150)), (30, 80))
        for i, row in enumerate(board):
            col = (255,215,0) if i == 0 else (255,255,255)
            date = str(row[3])[:10] if row[3] else ""
            line = f"{i+1:<3}{row[0]:<15}{row[1]:<7}{row[2]}"
            screen.blit(font.render(line, True, col), (30, 115 + i*36))
        back_btn = draw_btn("Back", WIDTH//2-100, 530, 200, 45)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return

def screen_settings():
    colors = [(0,255,0),(0,100,255),(255,50,50),(255,200,0),(200,0,200)]
    while True:
        screen.fill((20,20,25))
        t = big_font.render("Settings", True, (255,255,255))
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 30))

        screen.blit(font.render("Snake color:", True, (200,200,200)), (30, 120))
        color_rects = []
        for i, c in enumerate(colors):
            rx = 30 + i * 106
            pygame.draw.rect(screen, c, (rx, 148, 80, 35), border_radius=5)
            if tuple(settings["snake_color"]) == c:
                pygame.draw.rect(screen, (255,255,255), (rx, 148, 80, 35), 3, border_radius=5)
            color_rects.append((pygame.Rect(rx, 148, 80, 35), c))

        gcol = (60,180,60) if settings["grid"] else (100,100,100)
        grid_btn = draw_btn("Grid: " + ("ON" if settings["grid"] else "OFF"), WIDTH//2-100, 220, 200, 45, gcol)
        scol = (60,180,60) if settings["sound"] else (100,100,100)
        snd_btn  = draw_btn("Sound: " + ("ON" if settings["sound"] else "OFF"), WIDTH//2-100, 285, 200, 45, scol)
        save_btn = draw_btn("Save & Back", WIDTH//2-100, 380, 200, 45, (60,100,200))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, c in color_rects:
                    if rect.collidepoint(event.pos):
                        settings["snake_color"] = list(c)
                if grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]
                if snd_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                if save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return

def screen_gameover(score, level, best):
    while True:
        screen.fill((20,20,25))
        t = big_font.render("GAME OVER", True, (220,60,60))
        screen.blit(t, (WIDTH//2 - t.get_width()//2, 80))
        screen.blit(font.render(f"Score: {score}",        True, (255,255,255)), (WIDTH//2-80, 200))
        screen.blit(font.render(f"Level: {level}",        True, (255,255,255)), (WIDTH//2-80, 235))
        screen.blit(font.render(f"Personal best: {best}", True, (255,215,0)),   (WIDTH//2-80, 270))
        retry_btn = draw_btn("Retry",     WIDTH//2-160, 350, 140, 45, (60,180,60))
        menu_btn  = draw_btn("Main Menu", WIDTH//2+20,  350, 140, 45, (60,100,200))
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos): return "retry"
                if menu_btn.collidepoint(event.pos):  return "menu"

def play_game(user_id, personal_best):
    game = SnakeGame()
    snake_color = tuple(settings.get("snake_color", [0,255,0]))
    show_grid = settings.get("grid", False)

    while True:
        clock.tick(FPS + game.level + game.speed_mod)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu", game.score, game.level
                if event.key == pygame.K_UP    and game.direction != [0, CELL]:   game.direction = [0, -CELL]
                if event.key == pygame.K_DOWN  and game.direction != [0, -CELL]:  game.direction = [0, CELL]
                if event.key == pygame.K_LEFT  and game.direction != [CELL, 0]:   game.direction = [-CELL, 0]
                if event.key == pygame.K_RIGHT and game.direction != [-CELL, 0]:  game.direction = [CELL, 0]

        game.update()

        if game.is_over:
            return "gameover", game.score, game.level

        screen.fill((20,20,25))

        if show_grid:
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(screen, (35,35,35), (x,0), (x,HEIGHT))
            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(screen, (35,35,35), (0,y), (WIDTH,y))

        for i, seg in enumerate(game.snake):
            col = snake_color if i > 0 else (255,255,255)
            if game.shield and i == 0:
                col = (100,200,255)
            pygame.draw.rect(screen, col, (*seg, CELL-1, CELL-1))

        pygame.draw.rect(screen, (255, 50, 50),  (*game.food,   CELL-1, CELL-1))
        pygame.draw.rect(screen, (120,  0,  0),  (*game.poison, CELL-1, CELL-1))

        for obs in game.obstacles:
            pygame.draw.rect(screen, (150,100,50), (*obs, CELL-1, CELL-1))

        if game.powerup:
            pcol = (0,200,255) if game.powerup_kind=="speed" else (200,100,255) if game.powerup_kind=="slow" else (255,200,0)
            pygame.draw.rect(screen, pcol, (*game.powerup, CELL-1, CELL-1))
            pl = font.render(game.powerup_kind[0].upper(), True, (0,0,0))
            screen.blit(pl, (game.powerup[0]+3, game.powerup[1]+2))

        screen.blit(font.render(f"Score: {game.score}  Lvl: {game.level}", True, (200,200,200)), (10, 10))
        screen.blit(font.render(f"Best: {personal_best}", True, (255,215,0)), (WIDTH-130, 10))

        if game.active_effect:
            now = pygame.time.get_ticks()
            secs = max(0, (game.effect_end - now)//1000)
            ecol = (0,200,255) if game.active_effect=="speed" else (200,100,255) if game.active_effect=="slow" else (255,200,0)
            screen.blit(font.render(f"{game.active_effect.upper()} {secs}s", True, ecol), (10, HEIGHT-30))

        pygame.display.flip()

username = ""
state     = "menu"
user_id   = None
best      = 0

while True:
    if state == "menu":
        username, action = screen_menu()
        if action == "play":
            user_id = db.get_user_id(username)
            best    = db.get_personal_best(user_id)
            state   = "game"
        elif action == "leaderboard":
            screen_leaderboard()
        elif action == "settings":
            screen_settings()

    elif state == "game":
        result, score, level = play_game(user_id, best)
        if result == "gameover":
            db.save_session(user_id, score, level)
            best = db.get_personal_best(user_id)
            action = screen_gameover(score, level, best)
            state = "game" if action == "retry" else "menu"
        else:
            state = "menu"