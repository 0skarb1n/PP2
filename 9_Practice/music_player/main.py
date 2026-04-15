import pygame

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont("Arial", 24)

songs = ["music.mp3", "Music2.mp3"]
current_idx = 0
status = "Stopped"

running = True
while running:
    screen.fill((30, 30, 30))
    
    text_surface = font.render(f"Track: {songs[current_idx]}", True, (255, 255, 255))
    status_surface = font.render(f"Status: {status}", True, (200, 200, 200))
    
    screen.blit(text_surface, (50, 50))
    screen.blit(status_surface, (50, 100))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.mixer.music.load(songs[current_idx])
                pygame.mixer.music.play()
                status = "Playing"
            
            if event.key == pygame.K_s:
                pygame.mixer.music.stop()
                status = "Stopped"
            
            if event.key == pygame.K_n:
                current_idx = (current_idx + 1) % len(songs)
                pygame.mixer.music.load(songs[current_idx])
                pygame.mixer.music.play()
                status = "Playing"

    pygame.display.flip()

pygame.quit()