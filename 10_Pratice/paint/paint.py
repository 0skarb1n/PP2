import pygame, sys

pygame.init()

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

current_color = (0, 0, 255)
current_tool = "brush"
brush_size = 10

screen.fill((255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tool = "brush"
            elif event.key == pygame.K_2:
                current_tool = "rect"
            elif event.key == pygame.K_3:
                current_tool = "circle"
            elif event.key == pygame.K_4:
                current_tool = "eraser"

            if event.key == pygame.K_r:
                current_color = (255, 0, 0)
            elif event.key == pygame.K_g:
                current_color = (0, 255, 0)
            elif event.key == pygame.K_b:
                current_color = (0, 0, 255)

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