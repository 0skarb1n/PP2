import pygame
import sys
from datetime import datetime
from tools import draw_pencil, draw_line, draw_rectangle, draw_circle
from tools import draw_right_triangle, draw_rhombus, flood_fill

pygame.init()

WIDTH = 900
HEIGHT = 600
TOOLBAR_W = 140

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

canvas = pygame.Surface((WIDTH - TOOLBAR_W, HEIGHT))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 13)
text_font = pygame.font.SysFont("Arial", 20)

current_tool = "Pencil"
current_color = (0, 0, 0)
brush_index = 0
brush_sizes = [2, 5, 10]

drawing = False
start_pos = None
prev_pos = None
canvas_backup = None

text_mode = False
text_pos = None
text_buffer = ""

tools_list = ["Pencil", "Line", "Rect", "Circle", "R.Tri", "Rhombus", "Fill", "Text", "Eraser"]

colors_list = [
    (0, 0, 0),
    (255, 255, 255),
    (255, 0, 0),
    (0, 200, 0),
    (0, 0, 255),
    (255, 255, 0),
    (200, 0, 200),
    (255, 140, 0),
    (0, 200, 200),
    (150, 75, 0),
    (255, 192, 203),
    (128, 128, 128)
]

clock = pygame.time.Clock()

while True:
    brush_size = brush_sizes[brush_index]

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                brush_index = 0
            elif event.key == pygame.K_2:
                brush_index = 1
            elif event.key == pygame.K_3:
                brush_index = 2

            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                filename = "canvas_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
                pygame.image.save(canvas, filename)
                pygame.display.set_caption("Saved: " + filename)

            if text_mode == True:
                if event.key == pygame.K_RETURN:
                    rendered = text_font.render(text_buffer, True, current_color)
                    canvas.blit(rendered, text_pos)
                    text_mode = False
                    text_buffer = ""
                    text_pos = None
                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_buffer = ""
                    text_pos = None
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    if event.unicode:
                        text_buffer = text_buffer + event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx = event.pos[0]
            my = event.pos[1]

            if mx < TOOLBAR_W:
                for i in range(len(tools_list)):
                    ty = 40 + i * 30
                    if my >= ty and my <= ty + 24:
                        current_tool = tools_list[i]
                        text_mode = False
                        text_buffer = ""

                if mx >= 10 and mx <= 50 and my >= HEIGHT - 100 and my <= HEIGHT - 76:
                    brush_index = 0
                elif mx >= 55 and mx <= 85 and my >= HEIGHT - 100 and my <= HEIGHT - 76:
                    brush_index = 1
                elif mx >= 90 and mx <= 130 and my >= HEIGHT - 100 and my <= HEIGHT - 76:
                    brush_index = 2

                for i in range(len(colors_list)):
                    row = i // 2
                    col = i % 2
                    cx2 = 10 + col * 55
                    cy2 = HEIGHT - 95 + 30 + row * 22
                    if mx >= cx2 and mx <= cx2 + 20 and my >= cy2 and my <= cy2 + 18:
                        current_color = colors_list[i]

            else:
                cx = mx - TOOLBAR_W
                cy = my

                if current_tool == "Fill":
                    flood_fill(canvas, (cx, cy), current_color)
                elif current_tool == "Text":
                    text_mode = True
                    text_pos = (cx, cy)
                    text_buffer = ""
                else:
                    drawing = True
                    start_pos = (cx, cy)
                    prev_pos = (cx, cy)
                    canvas_backup = canvas.copy()

        if event.type == pygame.MOUSEMOTION:
            if drawing == True:
                mx = event.pos[0]
                my = event.pos[1]
                if mx >= TOOLBAR_W:
                    cx = mx - TOOLBAR_W
                    cy = my
                    if current_tool == "Pencil":
                        draw_pencil(canvas, prev_pos, (cx, cy), current_color, brush_size)
                        prev_pos = (cx, cy)
                    elif current_tool == "Eraser":
                        draw_pencil(canvas, prev_pos, (cx, cy), (255, 255, 255), brush_size * 4)
                        prev_pos = (cx, cy)

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing == True:
                mx = event.pos[0]
                my = event.pos[1]
                cx = mx - TOOLBAR_W
                cy = my
                drawing = False

                if current_tool == "Line":
                    draw_line(canvas, start_pos, (cx, cy), current_color, brush_size)
                elif current_tool == "Rect":
                    draw_rectangle(canvas, start_pos, (cx, cy), current_color, brush_size)
                elif current_tool == "Circle":
                    draw_circle(canvas, start_pos, (cx, cy), current_color, brush_size)
                elif current_tool == "R.Tri":
                    draw_right_triangle(canvas, start_pos, (cx, cy), current_color, brush_size)
                elif current_tool == "Rhombus":
                    draw_rhombus(canvas, start_pos, (cx, cy), current_color, brush_size)

                canvas_backup = None

    screen.fill((60, 60, 60))
    pygame.draw.rect(screen, (40, 40, 40), (0, 0, TOOLBAR_W, HEIGHT))

    title = font.render("Tools:", True, (255, 255, 255))
    screen.blit(title, (5, 20))

    for i in range(len(tools_list)):
        ty = 40 + i * 30
        if tools_list[i] == current_tool:
            pygame.draw.rect(screen, (100, 160, 255), (5, ty, TOOLBAR_W - 10, 24))
        else:
            pygame.draw.rect(screen, (80, 80, 80), (5, ty, TOOLBAR_W - 10, 24))
        label = font.render(tools_list[i], True, (255, 255, 255))
        screen.blit(label, (8, ty + 5))

    size_label = font.render("Size:", True, (255, 255, 255))
    screen.blit(size_label, (5, HEIGHT - 105))

    for i in range(3):
        bx = 10 + i * 40
        if i == brush_index:
            pygame.draw.rect(screen, (100, 160, 255), (bx, HEIGHT - 90, 34, 20))
        else:
            pygame.draw.rect(screen, (80, 80, 80), (bx, HEIGHT - 90, 34, 20))
        sl = font.render(str(i + 1), True, (255, 255, 255))
        screen.blit(sl, (bx + 12, HEIGHT - 88))

    col_label = font.render("Color:", True, (255, 255, 255))
    screen.blit(col_label, (5, HEIGHT - 68))

    for i in range(len(colors_list)):
        row = i // 2
        col = i % 2
        cx2 = 10 + col * 55
        cy2 = HEIGHT - 55 + row * 22
        pygame.draw.rect(screen, colors_list[i], (cx2, cy2, 20, 18))
        if colors_list[i] == current_color:
            pygame.draw.rect(screen, (255, 255, 0), (cx2, cy2, 20, 18), 2)

    if drawing == True and canvas_backup != None and current_tool != "Pencil" and current_tool != "Eraser":
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]
        cx = mx - TOOLBAR_W
        cy = my
        temp = canvas_backup.copy()
        if current_tool == "Line":
            draw_line(temp, start_pos, (cx, cy), current_color, brush_size)
        elif current_tool == "Rect":
            draw_rectangle(temp, start_pos, (cx, cy), current_color, brush_size)
        elif current_tool == "Circle":
            draw_circle(temp, start_pos, (cx, cy), current_color, brush_size)
        elif current_tool == "R.Tri":
            draw_right_triangle(temp, start_pos, (cx, cy), current_color, brush_size)
        elif current_tool == "Rhombus":
            draw_rhombus(temp, start_pos, (cx, cy), current_color, brush_size)
        screen.blit(temp, (TOOLBAR_W, 0))
    else:
        screen.blit(canvas, (TOOLBAR_W, 0))

    if text_mode == True and text_pos != None:
        preview = text_font.render(text_buffer + "|", True, current_color)
        screen.blit(preview, (text_pos[0] + TOOLBAR_W, text_pos[1]))

    pygame.display.flip()
    clock.tick(60)