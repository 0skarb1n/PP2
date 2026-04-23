import pygame, sys

pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

current_tool = "brush"
brush_size = 10

r, g, b = 255, 0, 0
current_color = (r, g, b)

screen.fill((255, 255, 255))

while True:
    r %= 256
    g %= 256
    b %= 256
    current_color = (r, g, b)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tool = "brush"
            if event.key == pygame.K_2:
                current_tool = "rect"
            if event.key == pygame.K_3:
                current_tool = "circle"
            if event.key == pygame.K_4:
                current_tool = "eraser"
            if event.key == pygame.K_r:
                r += 15
            if event.key == pygame.K_g:  
                g += 15
            if event.key == pygame.K_b: 
                b += 15
            if event.key == pygame.K_o: 
                brush_size += 5
            if event.key == pygame.K_p: 
                brush_size = max(5, brush_size - 5)
            if event.key == pygame.K_c:
                r, g, b = 0, 0, 0
                brush_size = 10

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if current_tool == "rect":
                    pygame.draw.rect(screen, current_color, (mouse_pos[0]-25, mouse_pos[1]-25, 50, 50))
                elif current_tool == "circle":
                    pygame.draw.circle(screen, current_color, mouse_pos, 25)

    if pygame.mouse.get_pressed()[0]: 
        mouse_pos = pygame.mouse.get_pos() 
        if current_tool == "brush": 
            pygame.draw.circle(screen, current_color, mouse_pos, brush_size) 
        elif current_tool == "eraser": 
            pygame.draw.circle(screen, (255, 255, 255), mouse_pos, 20) 

    pygame.display.flip()
    clock.tick(120)